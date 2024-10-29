import json
import jiwer
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
    data = dict()

    try:
        for file in files:
            for line in open(file, encoding = 'unicode_escape').readlines():
                if len(line.strip()) > 1:
                    example_data = json.loads(line)
                    data[example_data["audio_filepath"]] = example_data["text"]
    except Exception as e: 
        raise Exception(f'Error reading file "{file}" - Exception: {e}.')

    return data

def evaluate_scores(data_submission_path, data_reference_path):
    """
    Open and read files sequentially
    """
    submission_files = get_full_filename_paths(data_submission_path)
    reference_files = get_full_filename_paths(data_reference_path)

    if len(submission_files) != len(reference_files):
        raise Exception(f'Folders do not contain same number of files. ' + 
            f'Submission folder: {len(submission_files)}, Reference folder: {len(reference_files)}.')

    submission_data = read_files(submission_files)
    reference_data = read_files(reference_files)

    if len(submission_data) != len(reference_data):
        raise ValueError("Submission and reference texts have different lengths!")

    reference_texts = []
    submission_texts = []
    for recording in reference_data.keys():
        reference_texts.append(reference_data[recording])
        submission_texts.append(submission_data[recording])


    # Calculate
    transformation = jiwer.Compose([
        jiwer.SubstituteRegexes({r"(^|\s)([<\[][^\s]+[\]>])(\s*([<\[][^\s]+[\]>]))*(\s|$)":" "}), # since we match ' <...> ' must replace with ' '
        jiwer.RemovePunctuation(),
        jiwer.ToLowerCase(),
        jiwer.RemoveWhiteSpace(replace_by_space=True),
        jiwer.RemoveMultipleSpaces(),
        jiwer.Strip(), # remove whitespace at start or end of utterance that may have arised by removing special tokens '<...>'
        jiwer.SubstituteRegexes({r"^ {0,1}$":"X"}) # If empty strings removed, submission and reference sets might not match!
    ]) 

    measures = jiwer.compute_measures(
        transformation(reference_texts),
        transformation(submission_texts))

    wer = measures['wer']
    mer = measures['mer']
    wil = measures['wil']
    wip = measures['wip']
    cer = jiwer.cer(
        transformation(reference_texts),
        transformation(submission_texts))

    results = {}
    results['CER'] = cer
    results['WER'] = wer
    results['1 - WER'] = 1-wer
    results['MER'] = mer
    results['WIL'] = wil
    results['WIP'] = wip
        
    return results
