import json

def evaluate(data_ground_truth_path, data_submission_path):
     # Open ground truth file
     ground_truth = {}
     try:
          with open('./'+data_ground_truth_path+'/submission.json') as json_file:
               ground_truth = json.load(json_file)
     except Exception as e:
          raise Exception(f'Exception in opening ground truth file: {e}')

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
          shared_items = {k: ground_truth[k] for k in ground_truth if k in submission and ground_truth[k] == submission[k]}
          metrics = {
               'overall': float(len(shared_items) / len(ground_truth)) * 100,
               'metric1': 11.0,
               'metric2': 12.0,
               'metric3': 13.0
          }
          return metrics
     except Exception as e:
          raise Exception(f'Exception in metric calculation: {e}')