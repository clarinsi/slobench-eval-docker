import pandas as pd
from sklearn.metrics import f1_score, accuracy_score
from sklearn.preprocessing import MultiLabelBinarizer


def label_accuracy(y_true, y_pred):
    y_true = y_true['label']
    y_pred = y_pred['label']
    return accuracy_score(y_true, y_pred)


def f1_score_knowledge_type(y_true, y_pred):
    list_of_lists_of_true_labels = [entry.split(';') for entry in y_true['knowledge-type']]
    list_of_lists_of_pred_labels = [entry.split(';') for entry in y_pred['knowledge-type']]

    mlb = MultiLabelBinarizer()
    mlb.fit(list_of_lists_of_true_labels)

    y_true = mlb.transform(list_of_lists_of_true_labels)
    y_pred = mlb.transform(list_of_lists_of_pred_labels)

    return f1_score(y_true, y_pred, average='macro')


def f1_score_knowledge_subtype(y_true, y_pred):
    list_of_lists_of_true_labels = [entry.split(';') for entry in y_true['knowledge-subtype']]
    list_of_lists_of_pred_labels = [entry.split(';') for entry in y_pred['knowledge-subtype']]

    mlb = MultiLabelBinarizer()
    mlb.fit(list_of_lists_of_true_labels)

    y_true = mlb.transform(list_of_lists_of_true_labels)
    y_pred = mlb.transform(list_of_lists_of_pred_labels)

    return f1_score(y_true, y_pred, average='macro', zero_division=0)


def main(y_true, y_pred):
    # Initialize the dictionary with results
    y_pred_cols = y_pred.columns
    results = {
        'label_accuracy': label_accuracy(y_true, y_pred) if 'label' in y_pred_cols else '/',
        'f1_macro_knowledge_type': f1_score_knowledge_type(y_true, y_pred) if 'knowledge-type' in y_pred_cols else '/',
        'f1_macro_knowledge_subtype': f1_score_knowledge_subtype(y_true, y_pred) if 'knowledge-subtype' in y_pred_cols else '/'
    }

    # Print the dictionary
    return results