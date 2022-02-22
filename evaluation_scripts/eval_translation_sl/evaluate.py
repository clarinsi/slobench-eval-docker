from translation_eval import evaluate_scores
import os

def evaluate(reference_dataset_path, data_submission_path):
     pred_folder = data_submission_path
     true_folder = reference_dataset_path

     # Calculate metrics
     try:
          results = evaluate_scores(pred_folder, true_folder)
          return results
     except Exception as e:
          raise Exception(f'Exception in metric calculation: {e}')

     