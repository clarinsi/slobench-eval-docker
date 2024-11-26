from ke_wsc_eval import *
import os

def evaluate_scores(true_file, pred_file):
    # Files in tsv format
    y_true = pd.read_csv(true_file, sep='\t')
    y_pred = pd.read_csv(pred_file, sep='\t')

    results = main(y_true, y_pred)

    return results


def evaluate(reference_dataset_path, data_submission_path):
     pred_file = list(os.scandir(data_submission_path))[0].path
     true_file = list(os.scandir(reference_dataset_path))[0].path

     # Calculate metrics
     try:
          results = evaluate_scores(true_file, pred_file)
          return results
     except Exception as e:
          raise Exception(f'Exception in metric calculation: {e}')
