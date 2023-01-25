import conll18_ud_eval 
import os

def get_full_filename_path(path):
    """
    Only one file should be in a folder!
    """    
    files = [filename for filename in os.listdir(path)]
    if len(files) != 1:
        raise Exception(f'Folder {path} does not contain only one file. Contents: {files}.')
    return f"{path}/{files[0]}"

def evaluate_scores(submission_folder, reference_folder):
     gold_ud = conll18_ud_eval.load_conllu_file(get_full_filename_path(reference_folder))
     system_ud = conll18_ud_eval.load_conllu_file(get_full_filename_path(submission_folder))
     evaluation = conll18_ud_eval.evaluate(gold_ud, system_ud)


     results = {}

     for eval_dimension in ["Sentences", "Tokens", "Lemmas", "XPOS", "UPOS", "UFeats", "LAS", "UAS"]:
          results[f"{eval_dimension} Precision"] = evaluation[eval_dimension].precision
          results[f"{eval_dimension} Recall"] = evaluation[eval_dimension].recall
          results[f"{eval_dimension} F1 Score"] = evaluation[eval_dimension].f1

     return results

def evaluate(reference_dataset_path, data_submission_path):
     pred_folder = data_submission_path
     true_folder = reference_dataset_path

     # Calculate metrics
     try:
          results = evaluate_scores(pred_folder, true_folder)
          return results
     except Exception as e:
          raise Exception(f'Exception in metric calculation: {e}')

     