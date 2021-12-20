import json

def evaluate(reference_dataset_path, data_submission_path):
     # Open reference dataset file
     reference_dataset = {}
     try:
          with open('./'+reference_dataset_path+'/submission.json') as json_file:
               reference_dataset = json.load(json_file)
     except Exception as e:
          raise Exception(f'Exception in opening reference dataset file: {e}')

     # Open Submission File
     submission = {}
     try:
          with open('./'+data_submission_path+'/submission.json') as json_file:
               submission = json.load(json_file)
               if not submission:
                    raise Exception(f'Submission file is empty or contains the wrong filename.')
     except Exception as e:
          raise Exception(f'Exception in opening submission file: {e}')

     # Calculate metrics
     try:
          shared_items = {k: reference_dataset[k] for k in reference_dataset if k in submission and reference_dataset[k] == submission[k]}
          metrics = {
               'overall': float(len(shared_items) / len(reference_dataset)) * 100,
               'metric1': 11.0,
               'metric2': 12.0,
               'metric3': 13.0
          }
          return metrics
     except Exception as e:
          raise Exception(f'Exception in metric calculation: {e}')