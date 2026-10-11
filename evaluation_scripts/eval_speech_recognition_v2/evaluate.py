import re
from pathlib import Path

import jiwer
import polars as pl

preprocess = jiwer.Compose(
    [
        jiwer.SubstituteRegexes(
            {r"\(\)|\[[^\]]*\]": ""}
        ),  # this takes care of [zvok and such], as well as lengthen sign (), as in po()
        jiwer.ToLowerCase(),
        jiwer.RemoveWhiteSpace(replace_by_space=True),
        jiwer.RemoveMultipleSpaces(),
        jiwer.Strip(),
        jiwer.SubstituteRegexes({r"^ {0,1}$": "EMPTYSTRING"}),
    ]
)

postprocess = jiwer.Compose(
    [
        jiwer.SubstituteRegexes({r"\(\)|\[[^\]]*\]": " "}),
        jiwer.RemovePunctuation(),
        jiwer.ToLowerCase(),
        jiwer.RemoveWhiteSpace(replace_by_space=True),
        jiwer.RemoveMultipleSpaces(),
        jiwer.Strip(),
        jiwer.SubstituteRegexes({r"^ {0,1}$": "EMPTYSTRING"}),
    ]
)


def generate_optimal_transcript(
    norm: str, colloq: str, text: str, tier: str = "cross", metric=jiwer.wer
) -> str:
    """Optimises the transcript:

    >>> generate_optimal_transcript("Živijo, prijatelji dobre {eem} kave", "Žijo, prjatli duobre {eem} kave", "Žijo, prijatelji dobre eem kave")
    'žijo, prijatelji dobre  {eem}  kave'

    :param str norm: Norm transcription
    :param str colloq: Colloq transcription
    :param str text: hypothesis
    :param str tier: tier to take in account, defaults to "cross", can be also norm or colloq
    :param Callable metric: Error rate (higher means worse), defaults to jiwer.wer
    :return str: Optimised reference string
    """
    norm, colloq, text = preprocess(norm), preprocess(colloq), preprocess(text)
    if tier == "norm":
        gold = norm
    if tier == "colloq":
        gold = colloq
    if tier == "cross":
        norm_parts, colloq_parts = norm.split(), colloq.split()
        assert len(norm_parts) == len(colloq_parts), (
            "Word count missmatch between norm and colloq"
        )
        cross_parts = norm_parts
        score = metric(
            postprocess(" ".join(cross_parts)),
            postprocess(text),
        )
        for i, part in enumerate(colloq_parts):
            new_cross_parts = cross_parts.copy()
            new_cross_parts[i] = part
            new_score = metric(
                postprocess(" ".join(new_cross_parts)),
                postprocess(text),
            )
            # print(f"Word: {part}, new score: {new_score}, to beat: {score}")
            if new_score < score:
                # print("Will swap the word ", part)
                score = new_score
                cross_parts = new_cross_parts
        gold = " ".join(cross_parts)
    # Now deletable elements:
    gold_parts = re.split(r"(\{[^}]*\})", gold)
    score = metric(
        postprocess(" ".join(gold_parts)),
        postprocess(text),
    )
    for i, part in enumerate(gold_parts):
        new_gold_parts = gold_parts.copy()
        new_gold_parts[i] = ""
        new_score = metric(postprocess(" ".join(new_gold_parts)), postprocess(text))
        if new_score < score:
            # print("Will inhibit deletable ", part)
            score = new_score
            gold_parts = new_gold_parts
    gold = " ".join(gold_parts)
    return gold


def compute_metrics(df: pl.DataFrame) -> dict:
    """Compute all benchmark metrics for an already-joined dataframe.

    The dataframe is expected to contain the columns ``id``, ``norm``, ``colloq``
    and ``text``.
    """
    df = df.with_columns(
        pl.struct(["norm", "colloq", "text"])
        .map_elements(
            lambda row: generate_optimal_transcript(
                row["norm"], row["colloq"], row["text"]
            ),
            return_dtype=pl.String,
        )
        .alias("crossd_wer"),
        pl.struct(["norm", "colloq", "text"])
        .map_elements(
            lambda row: generate_optimal_transcript(
                row["norm"], row["colloq"], row["text"], metric=jiwer.cer
            ),
            return_dtype=pl.String,
        )
        .alias("crossd_cer"),
        pl.struct(["norm", "colloq", "text"])
        .map_elements(
            lambda row: generate_optimal_transcript(
                row["norm"], row["colloq"], row["text"], tier="colloq"
            ),
            return_dtype=pl.String,
        )
        .alias("colloqd_wer"),
        pl.struct(["norm", "colloq", "text"])
        .map_elements(
            lambda row: generate_optimal_transcript(
                row["norm"], row["colloq"], row["text"], tier="norm"
            ),
            return_dtype=pl.String,
        )
        .alias("normd_wer"),
    )

    text = df["text"].to_list()
    crossd_wer = df["crossd_wer"].to_list()
    crossd_cer = df["crossd_cer"].to_list()
    colloqd_wer = df["colloqd_wer"].to_list()
    normd_wer = df["normd_wer"].to_list()

    total_deletables = df.select(
        pl.col("norm").str.count_matches("{", literal=True).sum()
    ).item()
    preserved_deletables = df.select(
        pl.col("normd_wer").str.count_matches("{", literal=True).sum()
    ).item()
    preserved_deletables_ratio = (
        preserved_deletables / total_deletables if total_deletables else 0.0
    )

    wer_score = jiwer.wer(
        truth=postprocess(crossd_wer),
        hypothesis=postprocess(text),
    )
    cer_score = jiwer.cer(
        truth=postprocess(crossd_cer),
        hypothesis=postprocess(text),
    )
    mer_score = jiwer.mer(
        truth=postprocess(crossd_wer),
        hypothesis=postprocess(text),
    )
    wil_score = jiwer.wil(
        truth=postprocess(crossd_wer),
        hypothesis=postprocess(text),
    )
    wip_score = jiwer.wip(
        truth=postprocess(crossd_wer),
        hypothesis=postprocess(text),
    )
    colloqd_wer_score = jiwer.wer(
        truth=postprocess(colloqd_wer),
        hypothesis=postprocess(text),
    )
    normd_wer_score = jiwer.wer(
        truth=postprocess(normd_wer),
        hypothesis=postprocess(text),
    )
    normalisation_factor = (
        (colloqd_wer_score - normd_wer_score) / colloqd_wer_score
        if colloqd_wer_score
        else 0.0
    )

    return {
        "CER": round(cer_score, 4),
        "WER": round(wer_score, 4),
        # "1-WER": round(1 - wer_score, 4),
        "MER": round(mer_score, 4),
        "WIL": round(wil_score, 4),
        # "WIP": round(wip_score, 4),
        "NORM": round(normalisation_factor, 4),
        "VERB": round(preserved_deletables_ratio, 4),
    }


# (id prefix, output suffix): 1 = SloBench, 2 = GSO.
GROUP_SUFFIXES = (("SloBench", "1"), ("GSO", "2"))
ID_PREFIXES = tuple(prefix for prefix, _ in GROUP_SUFFIXES)


def _require_columns(df: pl.DataFrame, name: str, required: list) -> None:
    """Raise if ``df`` is missing any of the ``required`` columns."""
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise Exception(
            f"The {name} file is missing required columns: {', '.join(missing)}"
        )


def _require_no_nulls(df: pl.DataFrame, name: str, columns: list) -> None:
    """Raise if any of the ``columns`` contain null values."""
    null_columns = [col for col in columns if df[col].null_count() > 0]
    if null_columns:
        raise Exception(
            f"The {name} file contains null values in columns: {', '.join(null_columns)}"
        )


def evaluate(reference_dataset_path, data_submission_path):
    reference_path = Path(".", reference_dataset_path, "asr_sample_reference.jsonl")
    if not reference_path.exists():
        raise FileNotFoundError(f"Reference file does not exist: {reference_path}")
    reference_df = pl.read_ndjson(reference_path)

    submission_path = Path(".", data_submission_path, "asr_sample_submission.jsonl")
    if not submission_path.exists():
        raise FileNotFoundError(f"Submission file does not exist: {submission_path}")
    submission_df = pl.read_ndjson(submission_path)

    _require_columns(reference_df, "reference", ["id", "norm", "colloq"])
    _require_columns(submission_df, "submission", ["id", "text"])
    _require_no_nulls(reference_df, "reference", ["id", "norm", "colloq"])
    _require_no_nulls(submission_df, "submission", ["id", "text"])
    submission_df = submission_df.select(["id", "text"])

    for name, data in (("reference", reference_df), ("submission", submission_df)):
        duplicates = data.filter(pl.col("id").is_duplicated())
        if duplicates.height:
            sample = ", ".join(duplicates["id"].unique().head(5).to_list())
            raise Exception(
                f"The {name} file contains duplicate 'id' entries: {sample}"
            )

    missing = reference_df.join(submission_df, on="id", how="anti").height
    if missing:
        raise Exception(f"The submission is missing {missing} reference entries.")

    extra = submission_df.join(reference_df, on="id", how="anti").height
    if extra:
        raise Exception(
            f"The submission contains {extra} entries that are not present "
            "in the reference."
        )

    df = reference_df.join(submission_df, on="id", how="inner").fill_null("")

    matches_prefix = pl.col("id").str.starts_with(ID_PREFIXES[0])
    for prefix in ID_PREFIXES[1:]:
        matches_prefix = matches_prefix | pl.col("id").str.starts_with(prefix)
    unmatched = df.filter(~matches_prefix)
    if unmatched.height:
        sample = ", ".join(unmatched["id"].head(5).to_list())
        prefixes = " or ".join(f"'{prefix}'" for prefix in ID_PREFIXES)
        raise Exception(
            f"Found {unmatched.height} entries whose 'id' does not start with "
            f"{prefixes}: {sample}"
        )

    metrics = {}
    for prefix, suffix in GROUP_SUFFIXES:
        group_df = df.filter(pl.col("id").str.starts_with(prefix))
        if group_df.height == 0:
            raise Exception(
                f"No entries found for the '{prefix}' id prefix; cannot compute metrics."
            )
        group_metrics = compute_metrics(group_df)
        for metric, value in group_metrics.items():
            metrics[f"{metric}{suffix}"] = value

    return metrics
