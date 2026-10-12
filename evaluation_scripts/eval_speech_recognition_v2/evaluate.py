import json
import re
from pathlib import Path

import jiwer

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


def _read_ndjson(path: Path) -> list:
    """Read a newline-delimited JSON file into a list of dictionaries."""
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def compute_metrics(rows: list) -> dict:
    """Compute all benchmark metrics for already-joined rows.

    Each row is a mapping expected to contain the keys ``id``, ``norm``,
    ``colloq`` and ``text``.
    """
    text = []
    crossd_wer = []
    crossd_cer = []
    colloqd_wer = []
    normd_wer = []
    for row in rows:
        norm, colloq = row["norm"], row["colloq"]
        hypothesis = row["text"]
        text.append(hypothesis)
        crossd_wer.append(generate_optimal_transcript(norm, colloq, hypothesis))
        crossd_cer.append(
            generate_optimal_transcript(norm, colloq, hypothesis, metric=jiwer.cer)
        )
        colloqd_wer.append(
            generate_optimal_transcript(norm, colloq, hypothesis, tier="colloq")
        )
        normd_wer.append(
            generate_optimal_transcript(norm, colloq, hypothesis, tier="norm")
        )

    total_deletables = sum(row["norm"].count("{") for row in rows)
    preserved_deletables = sum(gold.count("{") for gold in normd_wer)
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


def _require_columns(rows: list, name: str, required: list) -> None:
    """Raise if ``rows`` is missing any of the ``required`` columns."""
    present = set()
    for row in rows:
        present.update(row.keys())
    missing = [col for col in required if col not in present]
    if missing:
        raise Exception(
            f"The {name} file is missing required columns: {', '.join(missing)}"
        )


def _require_no_nulls(rows: list, name: str, columns: list) -> None:
    """Raise if any of the ``columns`` contain null values."""
    null_columns = [
        col for col in columns if any(row.get(col) is None for row in rows)
    ]
    if null_columns:
        raise Exception(
            f"The {name} file contains null values in columns: {', '.join(null_columns)}"
        )


def _duplicate_ids(rows: list) -> list:
    """Return the unique ``id`` values that occur more than once, in order."""
    counts = {}
    for row in rows:
        key = row["id"]
        counts[key] = counts.get(key, 0) + 1
    return [key for key, count in counts.items() if count > 1]


def evaluate(reference_dataset_path, data_submission_path):
    reference_path = Path(".", reference_dataset_path, "asr_sample_reference.jsonl")
    if not reference_path.exists():
        raise FileNotFoundError(f"Reference file does not exist: {reference_path}")
    reference_rows = _read_ndjson(reference_path)

    submission_path = Path(".", data_submission_path, "asr_sample_submission.jsonl")
    if not submission_path.exists():
        raise FileNotFoundError(f"Submission file does not exist: {submission_path}")
    submission_rows = _read_ndjson(submission_path)

    _require_columns(reference_rows, "reference", ["id", "norm", "colloq"])
    _require_columns(submission_rows, "submission", ["id", "text"])
    _require_no_nulls(reference_rows, "reference", ["id", "norm", "colloq"])
    _require_no_nulls(submission_rows, "submission", ["id", "text"])
    submission_rows = [
        {"id": row["id"], "text": row["text"]} for row in submission_rows
    ]

    for name, data in (("reference", reference_rows), ("submission", submission_rows)):
        duplicates = _duplicate_ids(data)
        if duplicates:
            sample = ", ".join(duplicates[:5])
            raise Exception(
                f"The {name} file contains duplicate 'id' entries: {sample}"
            )

    reference_ids = {row["id"] for row in reference_rows}
    submission_ids = {row["id"] for row in submission_rows}

    missing = len(reference_ids - submission_ids)
    if missing:
        raise Exception(f"The submission is missing {missing} reference entries.")

    extra = len(submission_ids - reference_ids)
    if extra:
        raise Exception(
            f"The submission contains {extra} entries that are not present "
            "in the reference."
        )

    text_by_id = {row["id"]: row["text"] for row in submission_rows}
    df = []
    for row in reference_rows:
        norm = row["norm"]
        colloq = row["colloq"]
        text = text_by_id[row["id"]]
        df.append(
            {
                "id": row["id"],
                "norm": "" if norm is None else norm,
                "colloq": "" if colloq is None else colloq,
                "text": "" if text is None else text,
            }
        )

    unmatched = [row for row in df if not row["id"].startswith(ID_PREFIXES)]
    if unmatched:
        sample = ", ".join(row["id"] for row in unmatched[:5])
        prefixes = " or ".join(f"'{prefix}'" for prefix in ID_PREFIXES)
        raise Exception(
            f"Found {len(unmatched)} entries whose 'id' does not start with "
            f"{prefixes}: {sample}"
        )

    metrics = {}
    for prefix, suffix in GROUP_SUFFIXES:
        group_rows = [row for row in df if row["id"].startswith(prefix)]
        if not group_rows:
            raise Exception(
                f"No entries found for the '{prefix}' id prefix; cannot compute metrics."
            )
        group_metrics = compute_metrics(group_rows)
        for metric, value in group_metrics.items():
            metrics[f"{metric}{suffix}"] = value

    return metrics
