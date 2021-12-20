from qa_eval import *
import numpy as np
import os

def evaluate_tasks(tasks, pred_folder, true_folder):
    results = {}
    for task in tasks:
        # Check if a task was submitted
        file_exists = os.path.isfile(os.path.join(pred_folder, task + '.jsonl'))
        if file_exists:
            y_pred = os.path.join(pred_folder, task + '.jsonl')
        else:
            raise Exception(f'Submission task "{task}" was not submitted.')            

        # Load true labels
        y_true = os.path.join(true_folder, task + '.jsonl')

        # Calculate metrics
        if task == 'BoolQ':
            try: 
               acc = BoolQ(y_true, y_pred)
               results['BoolQ Accuracy'] = acc
            except Exception as e:
               raise Exception(f'Exception evaluating task "{task}." Error: "{e}."')
        elif task == 'CB':
            try: 
               acc, f1 = CB(y_true, y_pred)
               results['CB Accuracy'] = acc
               results['CB F1 Score'] = f1
               results['CB Average'] = np.mean([acc, f1])               
            except Exception as e:
               raise Exception(f'Exception evaluating task "{task}." Error: "{e}."')
        elif task == 'COPA':
            try: 
               acc = COPA(y_true, y_pred)
               results['COPA Accuracy'] = acc
            except Exception as e:
               raise Exception(f'Exception evaluating task "{task}." Error: "{e}."')
        elif task == 'MultiRC':
            try: 
               f1_a, em = MultiRC(y_true, y_pred)
               # f1_a izračuna 0, če model napove večinski razred 0 in ne 1 pri binarnih rešitvah (tukaj bi po mojem moral biti kakšen warning s strani sklearna). 
               # To je bilo tudi narobe izračunano tudi v izvirnem članku iz SuperGLUE. Dobiti 0.4 EM in 0.0 f1_a je nemogoče glede definicije obeh metrik. 
               results['MultiRC F1a Score'] = f1_a
               results['MultiRC EM'] = em
               results['MultiRC Average'] = np.mean([f1_a, em])
            except Exception as e:
               raise Exception(f'Exception evaluating task "{task}." Error: "{e}."')
        elif task == 'RTE':
            try: 
               acc = RTE(y_true, y_pred)
               results['RTE Accuracy'] = acc
            except Exception as e:
               raise Exception(f'Exception evaluating task "{task}." Error: "{e}."')
        elif task == 'WSC':
            try: 
               acc = WSC(y_true, y_pred)
               results['WSC Accuracy'] = acc
            except Exception as e:
               raise Exception(f'Exception evaluating task "{task}." Error: "{e}."')

               

    total = results['BoolQ Accuracy'] + \
               results['CB Average'] + \
               results['COPA Accuracy'] + \
               results['MultiRC Average'] + \
               results['RTE Accuracy'] + \
               results['WSC Accuracy']
    results['Average'] = total / 6
    

    return results


def evaluate(reference_dataset_path, data_submission_path):
     pred_folder = data_submission_path
     true_folder = reference_dataset_path

     # Define tasks
     tasks = ['BoolQ', 'CB', 'COPA', 'MultiRC', 'RTE', 'WSC']

     # Calculate metrics
     try:
          results = evaluate_tasks(tasks, pred_folder, true_folder)
          return results
     except Exception as e:
          raise Exception(f'Exception in metric calculation: {e}')

     