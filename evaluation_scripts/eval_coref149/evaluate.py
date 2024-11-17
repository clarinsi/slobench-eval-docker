import os

from evaluate_corefud import call_scorer


def evaluate(data_ground_truth_path, data_submission_path):
	try:
		# The script is just glue code around ufal/corefud-scorer
		metrics = call_scorer(os.path.join(".", data_ground_truth_path, "coref149.conllu"),
							  os.path.join(".", data_submission_path, "submission.conllu"))
		return metrics
	except Exception as e:
		raise Exception(f'Exception in metric calculation: {e}')
