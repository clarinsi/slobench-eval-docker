from sklearn.metrics import *
from os import listdir

def get_full_filename_paths(path):
    """
    Only one file should be in a folder!
    """
    filenames = sorted([f"{path}/{filename}" for filename in listdir(path)])
    
    return filenames

def read_files(files):
    """
    Read all files from a given list
    """
    return [line.strip().split('\t')[1] 
        for file in files 
        for line in open(file, encoding = 'unicode_escape').readlines() 
        if len(line.strip().split('\t')) > 1]

def evaluate_scores(data_submission_path, data_reference_path):
    """
    Open and read files sequentially
    """
    submission_files = get_full_filename_paths(data_submission_path)
    reference_files = get_full_filename_paths(data_reference_path)

    if len(submission_files) != len(reference_files):
        raise Exception(f'Folders do not contain same number of files. ' + 
            f'Submission folder: {len(submission_files)}, Reference folder: {len(reference_files)}.')

    submission_labels = read_files(submission_files)
    reference_labels = read_files(reference_files)

    if len(submission_labels) != len(reference_labels):
        raise ValueError("Submission and reference labels have different lengths!")
    
    
    precision = precision_score(reference_labels, submission_labels, average = 'weighted')
    recall = recall_score(reference_labels, submission_labels, average = 'weighted')
    f1 = f1_score(reference_labels, submission_labels, average = 'weighted')

    results = {}
    results['Precision'] = precision
    results['Recall'] = recall
    results['F1 score'] = f1
    
    return results
