__author__ = "Ales Zagar"
__version__ = "1.0"
__maintainer__ = "Slavko Zitnik"
__email__ = "slavko.zitnik@fri.uni-lj.si"

import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, accuracy_score


def report_error(task):
    raise Exception(f'Evaluating task "{task}" resulted in an error: Submitted and test indices do not match')


def BoolQ(y_true, y_pred):
    # load data
    y_true = pd.read_json(y_true, lines=True, dtype={'label': bool})
    y_true.rename(columns={'label': 'y_true'}, inplace=True)

    y_pred = pd.read_json(y_pred, lines=True)
    y_pred.rename(columns={'label': 'y_pred'}, inplace=True)

    # reformat y_pred from boolq predicted (they do not get recognized as boolean automatically)
    mapping = {
        'true': True,
        'false': False
    }
    y_pred['y_pred'] = y_pred['y_pred'].map(mapping)

    # merge data on indices from y_true
    merged = pd.merge(y_true, y_pred, how='inner', on='idx')
    if len(merged) != len(y_true):
        report_error('BoolQ')

    # calculate metrics
    acc = accuracy_score(merged['y_true'], merged['y_pred'])

    return acc


def CB(y_true, y_pred):
    # load data
    y_true = pd.read_json(y_true, lines=True)
    y_true.rename(columns={'label': 'y_true'}, inplace=True)

    y_pred = pd.read_json(y_pred, lines=True)
    y_pred.rename(columns={'label': 'y_pred'}, inplace=True)

    # transform labels
    mapping = {
        'neutral': 0,
        'contradiction': 1,
        'entailment': 2
    }
    y_true['y_true'] = y_true['y_true'].map(mapping)
    y_pred['y_pred'] = y_pred['y_pred'].map(mapping)

    # merge data on indices from y_true
    merged = pd.merge(y_true, y_pred, how='inner', on='idx')
    if len(merged) != len(y_true):
        report_error('CB')

    # calculate metrics
    acc = accuracy_score(merged['y_true'], merged['y_pred'])
    f1 = f1_score(merged['y_true'], merged['y_pred'], average='macro')

    return acc, f1


def COPA(y_true, y_pred):
    # load data
    y_true = pd.read_json(y_true, lines=True)
    y_true.rename(columns={'label': 'y_true'}, inplace=True)

    y_pred = pd.read_json(y_pred, lines=True)
    y_pred.rename(columns={'label': 'y_pred'}, inplace=True)

    # merge data on indices from y_true
    merged = pd.merge(y_true, y_pred, how='inner', on='idx')
    if len(merged) != len(y_true):
        report_error('COPA')

    # calculate metric
    acc = accuracy_score(merged['y_true'], merged['y_pred'])

    return acc


def MultiRC(y_true, y_pred):
    def parse_answer_level(y_true, y_pred):
        y_true_answers = []
        for sample in y_true['passage']:
            for question in sample['questions']:
                for answer in question['answers']:
                    y_true_answers.append(answer)

        y_pred_answers = []
        for sample in y_pred['passage']:
            for question in sample['questions']:
                for answer in question['answers']:
                    y_pred_answers.append(answer)

        return y_true_answers, y_pred_answers

    def parse_question_level(y_true, y_pred):
        y_true_questions = []
        for sample in y_true['passage']:
            for question in sample['questions']:
                answers = []
                for answer in sorted(question['answers'], key=lambda x: x['idx']):  # sort answers by idx
                    answers.append(answer['label'])
                seq = "".join([str(i) for i in answers])
                y_true_questions.append({
                    'idx': question['idx'],
                    'label': seq
                })

        y_pred_questions = []
        for sample in y_pred['passage']:
            for question in sample['questions']:
                answers = []
                for answer in sorted(question['answers'], key=lambda x: x['idx']):  # sort answers by idx
                    answers.append(answer['label'])
                seq = "".join([str(i) for i in answers])
                y_pred_questions.append({
                    'idx': question['idx'],
                    'label': seq
                })

        return y_true_questions, y_pred_questions

    # load data
    y_true = pd.read_json(y_true, lines=True)
    y_pred = pd.read_json(y_pred, lines=True)

    # calculate score on ANSWER level
    y_true_answers, y_pred_answers = parse_answer_level(y_true, y_pred)
    y_true_answers, y_pred_answers = pd.DataFrame(y_true_answers), pd.DataFrame(y_pred_answers)

    y_true_answers.rename(columns={'label': 'y_true'}, inplace=True)
    y_pred_answers.rename(columns={'label': 'y_pred'}, inplace=True)

    # merge data on indices from y_true
    merged = pd.merge(y_true_answers, y_pred_answers, how='inner', on='idx')
    if len(merged) != len(y_true_answers):
        report_error('MultiRC')
    f1_a = f1_score(merged['y_true'], merged['y_pred'])

    # calculate score on QUESTION level
    y_true_questions, y_pred_questions = parse_question_level(y_true, y_pred)
    y_true_questions, y_pred_questions = pd.DataFrame(y_true_questions), pd.DataFrame(y_pred_questions)

    y_true_questions.rename(columns={'label': 'y_true'}, inplace=True)
    y_pred_questions.rename(columns={'label': 'y_pred'}, inplace=True)

    # merge data on indices from y_true
    merged = pd.merge(y_true_questions, y_pred_questions, how='inner', on='idx')
    if len(merged) != len(y_true_questions):
        report_error('MultiRC')
    if merged['y_true'].apply(len).values.sum() != merged['y_pred'].apply(len).values.sum():
        report_error('MultiRC')

    merged['em'] = merged['y_true'] == merged['y_pred']
    em = merged['em'].sum() / len(merged)

    return f1_a, em


def RTE(y_true, y_pred):
    # load data
    y_true = pd.read_json(y_true, lines=True)
    y_true.rename(columns={'label': 'y_true'}, inplace=True)

    y_pred = pd.read_json(y_pred, lines=True)
    y_pred.rename(columns={'label': 'y_pred'}, inplace=True)

    # transform labels
    mapping = {
        'entailment': 0,
        'not_entailment': 1
    }
    y_true['y_true'] = y_true['y_true'].map(mapping)
    y_pred['y_pred'] = y_pred['y_pred'].map(mapping)

    # merge data on indices from y_true
    merged = pd.merge(y_true, y_pred, how='inner', on='idx')
    if len(merged) != len(y_true):
        report_error('RTE')

    # calculate metrics
    acc = accuracy_score(merged['y_true'], merged['y_pred'])

    return acc


def WSC(y_true, y_pred):
    # load data
    y_true = pd.read_json(y_true, lines=True, dtype={'label': bool})
    y_true.rename(columns={'label': 'y_true'}, inplace=True)

    y_pred = pd.read_json(y_pred, lines=True)
    y_pred.rename(columns={'label': 'y_pred'}, inplace=True)

    # reformat y_pred from wsc predicted (they do not get recognized as boolean automatically)
    mapping = {
        'True': True,
        'False': False
    }
    y_pred['y_pred'] = y_pred['y_pred'].map(mapping)

    # merge data on indices from y_true
    merged = pd.merge(y_true, y_pred, how='inner', on='idx')
    if len(merged) != len(y_true):
        report_error('WSC')

    # calculate metrics
    acc = accuracy_score(merged['y_true'], merged['y_pred'])

    return acc