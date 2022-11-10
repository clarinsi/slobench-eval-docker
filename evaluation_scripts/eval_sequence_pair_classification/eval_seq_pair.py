from typing import List
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def calculate_nli(predictions: List[str], correct: List[str]):
	RECOGNIZED_CLASSES = ["entailment", "neutral", "contradiction"]
	CLASS2IDX = {_class: _i for _i, _class in enumerate(RECOGNIZED_CLASSES)}

	encoded_preds = []
	for _idx_row, _pred in enumerate(predictions):
		_enc = CLASS2IDX.get(_pred, None)
		if _enc is None:
			raise Exception(f"Unrecognized predicted class in row {_idx_row}: '{_pred}'."
							f"Recognized classes are: {RECOGNIZED_CLASSES}")

		encoded_preds.append(_enc)

	encoded_correct = []
	for _idx_row, _gt in enumerate(correct):
		_enc = CLASS2IDX.get(_gt, None)
		if _enc is None:
			# Do not leak information about the correct classes, display a generic error
			raise Exception(f"Exception in encoding the ground truth data in row {_idx_row}. "
							f"Please contact the leaderboard authors.")

		encoded_correct.append(_enc)

	results = {
		'Accuracy': accuracy_score(y_true=encoded_correct, y_pred=encoded_preds)
	}

	for CLASS_STR in RECOGNIZED_CLASSES:
		CLASS_INT = CLASS2IDX[CLASS_STR]
		# Convert multi-class problem to binary (e.g., "is_entailment?") problem to calculate class-wise metrics
		bin_preds = list(map(lambda _int_pred: _int_pred == CLASS_INT, encoded_preds))
		bin_correct = list(map(lambda _int_gt: _int_gt == CLASS_INT, encoded_correct))

		results[f'Precision({CLASS_STR})'] = precision_score(y_true=bin_correct, y_pred=bin_preds, pos_label=1, average="binary")
		results[f'Recall({CLASS_STR})'] = recall_score(y_true=bin_correct, y_pred=bin_preds, pos_label=1, average="binary")
		results[f'F1({CLASS_STR})'] = f1_score(y_true=bin_correct, y_pred=bin_preds, pos_label=1, average="binary")

	return results
