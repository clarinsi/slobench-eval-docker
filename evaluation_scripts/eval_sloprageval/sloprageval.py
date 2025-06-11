import pandas as pd
from sklearn.metrics import accuracy_score

## report separately for Quantity, Quality, Manner, Relation


def main_eval(y_true,y_pred):
    # Check submission for column names
    y_pred_cols = y_pred.columns
    for col in ['answer']:
       if col not in y_pred_cols:
           raise Exception(f'Column "{col}" missing from the submitted data. Found columns are: {y_pred_cols}')
    # Initialize dictionary with results
    results = dict()
    # Get predictions per each maxim type (Quality, Quantity, Relation, Manner, Literal)
    maxim_indices = y_true.groupby('maxim').indices
    for maxim in ['Quality','Quantity','Relation','Manner','Literal']:
        ref_rows = y_true.iloc[maxim_indices[maxim]]['answer']
        pred_rows = y_pred.iloc[maxim_indices[maxim]]['answer'].fillna('empty')
        assert len(ref_rows) == len(pred_rows)
        results[f'{maxim} Accuracy'] = accuracy_score(ref_rows, pred_rows)

    results['Average Accuracy'] = sum(results.values())/len(results)
    # Return the dictionary
    return results



