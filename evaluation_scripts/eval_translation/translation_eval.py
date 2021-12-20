import nltk.translate.bleu_score as nltk_bleu_score
import nltk.translate.meteor_score as nltk_meteor_score
import nltk.translate.chrf_score as nltk_chrf_score
from os import listdir
import warnings
import nltk

chancherry = nltk_bleu_score.SmoothingFunction()
warnings.filterwarnings("ignore")

def get_full_filename_path(path):
    """
    Only one file should be in a folder!
    """
    files = [filename for filename in listdir(path)]
    if len(files) != 1:
        raise Exception(f'Folder {path} does not contain only one file. Contents: {files}.')
    return f"{path}/{files[0]}"

def read_files(submission_filename, reference_filename):
    """
    Open and read both files sequentially
    """
    submission_lines = list(map(lambda line: line.split(), open(submission_filename).readlines()))
    reference_lines = list(map(lambda line: line.split(), open(reference_filename).readlines()))

    if len(submission_lines) != len(reference_lines):
        raise ValueError("Submission and reference files have different lengths!")
    
    return (submission_lines, reference_lines)

def evaluate_scores(data_submission_path, reference_dataset_path):
    # DATA IMPORT
    submission_filename = get_full_filename_path(data_submission_path)
    reference_filename = get_full_filename_path(reference_dataset_path)
    (submission_lines, reference_lines) = read_files(submission_filename, reference_filename)

    # EVALUATION LINE METRICS
    bleu_score = 0
    meteor_score = 0
    chrf_score = 0
    for (submission_token_line, reference_token_line) in zip(submission_lines, reference_lines):    
        bleu_score += nltk_bleu_score.sentence_bleu([reference_token_line], submission_token_line, smoothing_function=chancherry.method1)
        meteor_score += nltk_meteor_score.meteor_score([reference_token_line], submission_token_line)
        chrf_score += nltk_chrf_score.sentence_chrf(reference_token_line, submission_token_line)
    bleu_score = bleu_score/len(submission_lines)    
    meteor_score = meteor_score/len(submission_lines)    
    chrf_score = chrf_score/len(submission_lines)
    


    # EVALUATION CORPUS METRICS
    reference_lines_lists = list(map(lambda line: [line], reference_lines)) 
    corpus_bleu_score = nltk_bleu_score.corpus_bleu(reference_lines_lists, submission_lines, smoothing_function=chancherry.method1)
    corpus_chrf_score = nltk_chrf_score.corpus_chrf(reference_lines, submission_lines)
    
    results = {}
    results["BLEU (avg)"] = bleu_score
    results["METEOR (avg)"] = meteor_score
    results["CHRF (avg)"] = chrf_score
    results["BLEU (corpus)"] = corpus_bleu_score
    results["CHRF (corpus)"] = corpus_chrf_score
    return results

