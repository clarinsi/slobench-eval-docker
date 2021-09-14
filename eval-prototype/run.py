from os import EX_CANTCREAT
import sys
from zipfile import ZipFile
import json
from evaluate import evaluate
from datetime import datetime
from time import sleep


def open_json_inside_zip_file(file):
     '''Opens a single .json inside a .zip file'''
     try:
          with ZipFile(file, 'r') as z:
               filename = z.namelist()[0]
               with z.open(filename) as f:
                    return json.load(f)
     except Exception as e:
          raise Exception(f'Error accessing {file} contents')


def run_evaluation():
     '''Runs the evaluation procedure'''
     test_dataset = open_json_inside_zip_file(sys.argv[1])
     submission_data = open_json_inside_zip_file(sys.argv[2])
     metrics = evaluate(test_dataset, submission_data)
     return metrics


def print_tseo_success(metrics, elapsed_time):
     '''Send the Successful Task Submission Evaluation Object (TSEO) back to the server'''
     tseo = {
               "status": "S",
               "metrics": metrics,
               "evaluation_time": elapsed_time.total_seconds(),
               "error_report": ""
          }
     json_formatted_str = json.dumps(tseo, indent=2)
     print(json_formatted_str)


def print_tseo_failure(error, elapsed_time):
     '''Send the Failed Task Submission Evaluation Object (TSEO) back to the server'''
     tseo = {
               "status": "F",
               "metrics": {},
               "evaluation_time": elapsed_time.total_seconds(),
               "error_report": f"{error}"
          }
     json_formatted_str = json.dumps(tseo, indent=2)
     print(json_formatted_str)


if __name__ == '__main__':
     start_time = datetime.now()
     try:
          metrics = run_evaluation()
          elapsed_time = datetime.now() - start_time
          print_tseo_success(metrics, elapsed_time)
     except Exception as e:
          elapsed_time = datetime.now() - start_time
          print_tseo_failure(str(e), elapsed_time)