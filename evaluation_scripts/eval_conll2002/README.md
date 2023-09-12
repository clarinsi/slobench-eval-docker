# SloBENCH evaluation script - conll2002

All commands should be run from the root directory of this repository.

## Build docker image 
```
docker buildx build --platform linux/amd64 -t slobench/eval:conll2002 -f evaluation_scripts/eval_conll2002/Dockerfile .
```

## Run evaluation 

Evaluation within SloBENCH will be run as follows:

```
docker run -it --name eval-container_conll2002 --rm \
-v $PWD/evaluation_scripts/eval_conll2002/reference.zip:/reference_dataset.zip \
-v $PWD/evaluation_scripts/eval_conll2002/submission.zip:/submission.zip \
slobench/eval:conll2002_1.0 reference_dataset.zip submission.zip
```

As `reference.zip` is not available, you can do manual testing as follows:


```
docker run -it --name eval-container_conll2002 --rm \
-v $PWD/evaluation_scripts/eval_conll2002/sample_reference.zip:/reference_dataset.zip \
-v $PWD/evaluation_scripts/eval_conll2002/sample_submission.zip:/submission.zip \
slobench/eval:conll2002_1.0 reference_dataset.zip submission.zip
```

This command should result in an output like this:


```
{
  "status": "S",
  "metrics": {
    "Precision": 99.51159951159951,
    "Recall": 99.14841849148418,
    "F1 score": 99.32967702620353,
    "P (DERIV-PER)": 100.0,
    "R (DERIV-PER)": 88.88888888888889,
    "F1 (DERIV-PER)": 94.11764705882352,
    "P (LOC)": 98.82352941176471,
    "R (LOC)": 98.82352941176471,
    "F1 (LOC)": 98.82352941176471,
    "P (MISC)": 100.0,
    "R (MISC)": 100.0,
    "F1 (MISC)": 100.0,
    "P (ORG)": 99.79338842975206,
    "R (ORG)": 99.38271604938271,
    "F1 (ORG)": 99.58762886597937,
    "P (PER)": 99.24812030075188,
    "R (PER)": 99.24812030075188,
    "F1 (PER)": 99.24812030075188
  },
  "evaluation_time": 0.044729,
  "error_report": ""
}
```