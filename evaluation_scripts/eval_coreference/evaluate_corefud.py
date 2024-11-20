import importlib

from scorer.corefud.reader import CorefUDReader
from scorer.eval import evaluator
uascorer = importlib.import_module("ua-scorer")


def call_scorer(ref_file, pred_file):
	args = {
		"key_file": ref_file,
		"sys_file": pred_file,
		"metrics": ['muc', 'bcub', 'ceafe', 'ceafm', 'blanc', 'lea', 'mor'],
		"keep_singletons": False,
		"match": "head",
		"zero_match_method": "dependent",
		"format": "corefud",
		"keep_split_antecedents": False,
		"keep_zeros": True,
		"evaluate_discourse_deixis": False,
		"only_split_antecedent": False,
		"allow_boundary_crossing": False,
		"np_only": False,
		"remove_nested_mentions": False,
		"shared_task": None
	}
	uascorer.process_arguments(args)
	reader = CorefUDReader(**args)
	reader.get_coref_infos(args["key_file"], args["sys_file"])

	conll = 0
	conll_subparts_num = 0

	calculated_metrics = {}
	for name, metric in args["metrics"]:
		recall, precision, f1 = evaluator.evaluate_documents(
			reader.doc_discourse_deixis_infos if args['evaluate_discourse_deixis'] else reader.doc_coref_infos,
			metric,
			beta=1,
			only_split_antecedent=args['only_split_antecedent'])

		calculated_metrics[f"Precision({name})"] = precision
		calculated_metrics[f"Recall({name})"] = recall
		calculated_metrics[f"F1({name})"] = f1

		if name in ["muc", "bcub", "ceafe"]:
			conll += f1
			conll_subparts_num += 1

	if conll_subparts_num == 3:
		conll = (conll / 3)
		calculated_metrics["conll"] = conll

	return calculated_metrics
