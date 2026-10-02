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


def evaluate(reference_dataset_path, data_submission_path):
    reference_path = Path(".", reference_dataset_path, "asr_sample_reference.jsonl")
    assert reference_path.exists(), "Reference path does not exist!"
    reference_df = pl.read_ndjson(reference_path)
    submission_path = Path(".", data_submission_path, "asr_sample_submission.jsonl")
    assert submission_path.exists(), "submission path does not exist!"
    submission_df = pl.read_ndjson(submission_path).select(["id", "text"])

    df = reference_df.join(submission_df, on="id", how="inner").fill_null("")
    crossd_wer = [
        generate_optimal_transcript(row["norm"], row["colloq"], row["text"])
        for row in df.iter_rows(named=True)
    ]
    crossd_cer = [
        generate_optimal_transcript(
            row["norm"], row["colloq"], row["text"], metric=jiwer.cer
        )
        for row in df.iter_rows(named=True)
    ]
    colloqd_wer = [
        generate_optimal_transcript(
            row["norm"], row["colloq"], row["text"], tier="colloq"
        )
        for row in df.iter_rows(named=True)
    ]
    normd_wer = [
        generate_optimal_transcript(
            row["norm"], row["colloq"], row["text"], tier="norm"
        )
        for row in df.iter_rows(named=True)
    ]
    text = df["text"].to_list()
    total_deletables = df.select(
        pl.col("norm").str.count_matches("{", literal=True).sum()
    ).item()
    preserved_deletables = (
        pl.Series("normd_wer", normd_wer).str.count_matches("{", literal=True).sum()
    )
    try:
        preserved_deletables_ratio = preserved_deletables / total_deletables
    except ZeroDivisionError:
        preserved_deletables_ratio = 0.0
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
    normalisation_factor = (colloqd_wer_score - normd_wer_score) / colloqd_wer_score
    submission_coverage = submission_df.height / reference_df.height
    if submission_coverage < 1.0:
        raise Exception(
            f"The submission has {reference_df.height - submission_df.height} missing entries!"
        )

    return {
        "CER": round(cer_score, 4),
        "WER": round(wer_score, 4),
        "1-WER": round(1 - wer_score, 4),
        "MER": round(mer_score, 4),
        "WIL": round(wil_score, 4),
        "WIP": round(wip_score, 4),
        "NORM": round(normalisation_factor, 4),
        "VERB": round(preserved_deletables_ratio, 4),
    }
