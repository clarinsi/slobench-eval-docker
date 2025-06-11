from sloprageval import *
import os
import pandas as pd


def evaluate_scores(true_file, pred_file):
    # Files in tsv format
    # Answer format: A, B, C, D, E
    y_true = pd.read_csv(true_file, sep='\t')
    y_pred = pd.read_csv(pred_file, sep='\t')
    if len(y_true) != len(y_pred):
        raise Exception(f'Length mismatch: Submission contains {len(y_pred)} items, expected {len(y_true)}.')
    results = main_eval(y_true, y_pred)
    return results


def evaluate(reference_dataset_path, data_submission_path):
    #scan directory for first file
     pred_file = list(os.scandir(data_submission_path))[0].path
     true_file = list(os.scandir(reference_dataset_path))[0].path

     # Calculate metrics
     try:
          results = evaluate_scores(true_file, pred_file)
          return results
     except Exception as e:
          raise Exception(f'Exception in metric calculation: {e}')



