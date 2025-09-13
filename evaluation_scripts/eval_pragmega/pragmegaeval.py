import pandas as pd
from sklearn.metrics import accuracy_score

## report separately for Metaphor, Irony, Humor

def main_eval(y_true,y_pred):
    # Check submission for column names
    y_pred_cols = y_pred.columns
    for col in ['Answer']:
       if col not in y_pred_cols:
           raise Exception(f'Column "{col}" missing from the submitted data. Found columns are: {y_pred_cols}')
    # Initialize dictionary with results
    results = dict()
    # Get predictions per each maxim type (Quality, Quantity, Relation, Manner, Literal)
    pragtype_indices = y_true.groupby('Type').indices
    for pragtype in ['Metaphor','Irony','Humour']:
        ref_rows = y_true.iloc[pragtype_indices[pragtype]]['CorrectAnswer']
        pred_rows = y_pred.iloc[pragtype_indices[pragtype]]['Answer'].fillna('empty')
        assert len(ref_rows) == len(pred_rows)
        results[f'{pragtype} Accuracy'] = accuracy_score(ref_rows, pred_rows)

    results['Average Accuracy'] = sum(results.values())/len(results)
    # Return the dictionary
    return results