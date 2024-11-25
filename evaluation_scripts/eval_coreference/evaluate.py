import os

from evaluate_corefud import call_scorer


def evaluate(data_ground_truth_path, data_submission_path):
	gt_path = os.path.join(".", data_ground_truth_path, "ground_truth.conllu")
	submission_path = os.path.join(".", data_submission_path, "submission.conllu")

	with open(gt_path, "r") as f_gt:
		gt_lines = list(
			filter(lambda _ln_str: _ln_str.startswith("# newdoc"),
				   map(lambda _s: _s.strip(), f_gt.readlines()))
		)

	with open(submission_path, "r") as f_gt:
		submission_lines = list(
			filter(lambda _ln_str: _ln_str.startswith("# newdoc"),
				   map(lambda _s: _s.strip(), f_gt.readlines()))
		)

	if len(gt_lines) != len(submission_lines):
		raise Exception(f"Number of documents in submission file ({len(submission_lines)}) is not equal to "
						f"number of ground truth documents ({len(gt_lines)}) ")

	# Extract doc ID from # newdoc line (e.g., "123.tsv" from "newdoc id = 123.tsv")
	gt_ids = set(map(lambda _newdoc_ln: _newdoc_ln.split("=")[-1].strip(), gt_lines))
	submission_ids = set(map(lambda _newdoc_ln: _newdoc_ln.split("=")[-1].strip(), submission_lines))
	if len(submission_ids & gt_ids) != len(gt_ids):
		raise Exception(f"Mismatch in document IDs. The following documents are missing in submission: "
						f"{gt_ids - submission_ids}")

	try:
		# The script is just glue code around ufal/corefud-scorer
		metrics = call_scorer(gt_path, submission_path)
		return metrics
	except Exception as e:
		raise Exception(f'Exception in metric calculation: {e}')
