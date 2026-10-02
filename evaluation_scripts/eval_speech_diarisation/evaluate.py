import os
import json
from pathlib import Path
from pyannote.core import Segment, Annotation, Timeline
from pyannote.metrics.diarization import DiarizationErrorRate
import warnings

# ------------------------------------------------------------
# Inlined errata merging logic (originally from errata_merge.py)
# This avoids needing to copy the module into the Docker container.
# ------------------------------------------------------------
AUTO_ERRATA_BASENAME = "AUTO_DATASET_ERRATA.json"


def _load_json_dict(path):
    import json

    p = Path(path) if not isinstance(path, Path) else path
    if not p.is_file():
        return {}
    try:
        with p.open(encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}
    if not isinstance(data, dict):
        return {}
    return {str(k): v for k, v in data.items() if isinstance(v, dict)}


def _float_or_none(d, key):
    if key not in d or d[key] is None:
        return None
    try:
        return float(d[key])
    except (TypeError, ValueError):
        return None


def merge_errata_for_evaluation(manual, auto):
    out = {}
    all_ids = set(manual) | set(auto)
    for fid in sorted(all_ids):
        m = manual.get(fid, {}) if isinstance(manual.get(fid), dict) else {}
        a = auto.get(fid, {}) if isinstance(auto.get(fid), dict) else {}
        m_ts, a_ts = _float_or_none(m, "trim_start"), _float_or_none(a, "trim_start")
        m_te, a_te = _float_or_none(m, "trim_end"), _float_or_none(a, "trim_end")

        rec = {}
        if m_ts is not None and a_ts is not None:
            rec["trim_start"] = max(m_ts, a_ts)
        elif m_ts is not None:
            rec["trim_start"] = m_ts
        elif a_ts is not None:
            rec["trim_start"] = a_ts

        if m_te is not None and a_te is not None:
            rec["trim_end"] = min(m_te, a_te)
        elif m_te is not None:
            rec["trim_end"] = m_te
        elif a_te is not None:
            rec["trim_end"] = a_te

        if "trim_start" not in rec and "trim_end" not in rec:
            continue

        mr = str(m.get("reason", "")).strip()
        ar = str(a.get("reason", "")).strip()
        bits = []
        if mr:
            bits.append(f"manual: {mr}")
        if ar:
            bits.append(f"auto: {ar}")
        if bits:
            rec["reason"] = " | ".join(bits)
        else:
            rec["reason"] = "merged errata (trim bounds only)"

        out[fid] = rec
    return out


def load_merged_errata(gold_path, manual_errata_path, *, merge_auto=True):
    """
    Load manual errata (if path exists) and optional auto errata beside gold.
    Returns:
        eval_errata: merged dict for evaluation
        report_meta: metadata dict
    """
    manual = _load_json_dict(manual_errata_path) if manual_errata_path else {}
    gold_parent = Path(gold_path).resolve().parent
    auto_path = gold_parent / AUTO_ERRATA_BASENAME
    auto = {}
    if merge_auto:
        auto = _load_json_dict(auto_path)

    merged = merge_errata_for_evaluation(manual, auto) if (manual or auto) else {}

    report_meta = {
        "manual": manual,
        "auto": auto,
        "merged": merged,
        "auto_path": str(auto_path) if merge_auto else None,
        "manual_path": str(manual_errata_path) if manual_errata_path else None,
    }
    return merged, report_meta


# ------------------------------------------------------------

warnings.filterwarnings("ignore", category=UserWarning, module="pyannote.metrics.utils")


def load_rttm(file_path):
    """Load a single RTTM file and return annotations keyed by file ID."""
    annotations = {}
    if not os.path.isfile(file_path):
        print(f"WARNING: File not found: {file_path}", flush=True)
        return annotations

    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(";") or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) < 8:
                continue
            if parts[0].upper() != "SPEAKER":
                continue
            try:
                file_id = parts[1]
                start = float(parts[3])
                duration = float(parts[4])
            except (ValueError, IndexError):
                continue
            label = parts[7]

            if file_id not in annotations:
                annotations[file_id] = Annotation(uri=file_id)

            annotations[file_id][Segment(start, start + duration)] = label
    return annotations


def compute_metrics_per_file(
    ref, hyp, file_id, errata_dict, collar=0.0, skip_overlap=False
):
    """
    Compute DER metrics per file between reference and hypothesis annotations.
    Matches the logic from the official score.py.

    Parameters
    ----------
    ref : Annotation
        Gold standard annotation.
    hyp : Annotation
        Hypothesis annotation.
    file_id : str
        The file identifier for errata lookup.
    errata_dict : dict
        Merged errata dict with trim_start/trim_end for UEM trimming.
    collar : float
        Collar (forgiveness) in seconds.
    skip_overlap : bool
        Ignore overlapping speech.

    Returns
    -------
    dict with per-file metrics, or None if no reference timeline.
    """
    # UEM / errata (trim_start, trim_end); audio extent approximated by reference RTTM
    ref_tl = ref.get_timeline()
    ref_end = ref_tl.extent().end if not ref_tl.empty() else 0.0
    ed = (
        errata_dict.get(file_id, {})
        if isinstance(errata_dict.get(file_id), dict)
        else {}
    )
    eval_start = 0.0
    ts = ed.get("trim_start")
    if ts is not None:
        try:
            eval_start = max(0.0, float(ts))
        except (TypeError, ValueError):
            eval_start = 0.0
    eval_end = float(ref_end)
    te = ed.get("trim_end")
    if te is not None:
        try:
            eval_end = min(eval_end, float(te))
        except (TypeError, ValueError):
            pass
    eval_start = max(0.0, min(eval_start, eval_end))

    uem = None
    full_window = eval_start <= 0 and eval_end >= ref_end - 1e-6
    if file_id in errata_dict and not full_window:
        uem = Timeline([Segment(eval_start, eval_end)])

    metric = DiarizationErrorRate(collar=collar, skip_overlap=skip_overlap)
    stats = metric(ref, hyp, detailed=True, uem=uem)

    total_speech = stats.get("total", 0.0)

    fa = stats.get("false alarm", 0.0)
    miss = stats.get("missed detection", 0.0)
    conf = stats.get("confusion", 0.0)

    der_val = (fa + miss + conf) / total_speech if total_speech > 0 else 0.0

    return {
        "Total Speech (s)": total_speech,
        "False Alarm (s)": fa,
        "Missed (s)": miss,
        "Confusion (s)": conf,
        "DER (%)": der_val * 100,
        "Missed (%)": (miss / total_speech * 100) if total_speech > 0 else 0.0,
        "False Alarm (%)": (fa / total_speech * 100) if total_speech > 0 else 0.0,
        "Confusion (%)": (conf / total_speech * 100) if total_speech > 0 else 0.0,
        "Error Time (s)": fa + miss + conf,
    }


def evaluate(reference_dataset_path: Path, data_submission_path: Path) -> dict:
    """
    Evaluate diarization for ROG-Art and ROG-Dialog datasets.

    Uses the same errata merging logic (manual + auto) as the official
    evaluation script in /home/peter/diarisation-benchmark/evaluation/score.py.

    Parameters
    ----------
    reference_dataset_path : Path
        Path to the reference dataset directory.
    data_submission_path : Path
        Path to the submission data directory.

    Returns
    -------
    dict
        Dictionary with per-dataset metrics in the format:
        {
            "DER_ROG-Art": ...,
            "MISS_ROG-Art": ...,
            "FA_ROG-Art": ...,
            "CONF_ROG-Art": ...,
            "DER_ROG-Dialog": ...,
            "MISS_ROG-Dialog": ...,
            "FA_ROG-Dialog": ...,
            "CONF_ROG-Dialog": ...
        }
    """

    # Define file paths
    submission_art = Path(data_submission_path, "ROG-Art.rttm")
    submission_dialog = Path(data_submission_path, "ROG-Dialog.rttm")
    references_art_t = Path(reference_dataset_path, "ROG-Art-gold_trimmed.rttm")
    references_dialog_t = Path(reference_dataset_path, "ROG-Dialog-gold_trimmed.rttm")

    # Load manual and auto errata directly from the reference dataset path
    # (Both files are guaranteed to exist by the caller)
    manual_errata_path = Path(reference_dataset_path, "DATASET_ERRATA.json")
    auto_errata_path = Path(reference_dataset_path, "AUTO_DATASET_ERRATA.json")

    manual_errata = _load_json_dict(manual_errata_path)
    auto_errata = _load_json_dict(auto_errata_path)

    print(f"Loaded manual errata: {len(manual_errata)} entries", flush=True)
    print(f"Loaded auto errata: {len(auto_errata)} entries", flush=True)

    # Merge them using the official logic (max for trim_start, min for trim_end)
    # Same errata applies to both datasets
    errata_merged = merge_errata_for_evaluation(manual_errata, auto_errata)
    print(f"Merged errata: {len(errata_merged)} entries", flush=True)

    datasets = [
        {
            "name": "ROG-Art",
            "gold_path": references_art_t,
            "hyp_path": submission_art,
            "errata_dict": errata_merged,
        },
        {
            "name": "ROG-Dialog",
            "gold_path": references_dialog_t,
            "hyp_path": submission_dialog,
            "errata_dict": errata_merged,
        },
    ]

    collar = 0.25
    skip_overlap = False

    result_dict = {}

    for ds in datasets:
        name = ds["name"]
        errata_dict = ds["errata_dict"]

        refs = load_rttm(ds["gold_path"])
        hyps = load_rttm(ds["hyp_path"])

        if not refs or not hyps:
            print(f"WARNING: No annotations loaded for {name}")
            result_dict[f"DER_{name}"] = 0.0
            result_dict[f"MISS_{name}"] = 0.0
            result_dict[f"FA_{name}"] = 0.0
            result_dict[f"CONF_{name}"] = 0.0
            continue

        common_files = sorted(list(set(refs.keys()) & set(hyps.keys())))
        if not common_files:
            print(
                f"WARNING: No matching file IDs between gold and prediction for {name}!"
            )
            result_dict[f"DER_{name}"] = 0.0
            result_dict[f"MISS_{name}"] = 0.0
            result_dict[f"FA_{name}"] = 0.0
            result_dict[f"CONF_{name}"] = 0.0
            continue

        # Accumulate in seconds (matching official score.py logic)
        global_total_ref = 0.0
        global_false_alarm = 0.0
        global_missed = 0.0
        global_conf = 0.0

        for file_id in common_files:
            ref = refs[file_id]
            hyp = hyps[file_id]

            result = compute_metrics_per_file(
                ref,
                hyp,
                file_id,
                errata_dict,
                collar=collar,
                skip_overlap=skip_overlap,
            )

            if result is None:
                continue

            global_total_ref += result["Total Speech (s)"]
            global_false_alarm += result["False Alarm (s)"]
            global_missed += result["Missed (s)"]
            global_conf += result["Confusion (s)"]

        if global_total_ref > 0:
            g_miss_proc = (global_missed / global_total_ref) * 100
            g_fa_proc = (global_false_alarm / global_total_ref) * 100
            g_conf_proc = (global_conf / global_total_ref) * 100
            global_der_proc = g_miss_proc + g_fa_proc + g_conf_proc
        else:
            global_der_proc = g_miss_proc = g_fa_proc = g_conf_proc = 0.0

        result_dict[f"DER_{name}"] = global_der_proc
        result_dict[f"MISS_{name}"] = g_miss_proc
        result_dict[f"FA_{name}"] = g_fa_proc
        result_dict[f"CONF_{name}"] = g_conf_proc

        print(
            f"{name}: DER={global_der_proc:.4f}%, MISS={g_miss_proc:.4f}%, FA={g_fa_proc:.4f}%, CONF={g_conf_proc:.4f}%"
        )

    return result_dict
