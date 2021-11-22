from summarization_eval import *
import os

def evaluate_scores(pred_folder, true_folder):
    results = {}

    # pointer output pattern
    dec_pattern = r'(\d+)_decoded.txt'  # instructions: https://github.com/bheinzerling/pyrouge
    ref_pattern = r'#ID#_reference.txt'

    results = eval_rouge(pred_folder, true_folder, dec_pattern, ref_pattern)

    return results


def evaluate(data_ground_truth_path, data_submission_path):
     pred_folder = data_submission_path
     true_folder = data_ground_truth_path

     # Calculate metrics
     try:
          results = evaluate_scores(pred_folder, true_folder)
          return results
     except Exception as e:
          raise Exception(f'Exception in metric calculation: {e}')

     