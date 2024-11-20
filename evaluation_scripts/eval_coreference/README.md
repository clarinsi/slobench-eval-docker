# eval_senticoref slobench evaluation script

All commands should be run from the root directory of the repository.

## Build docker image (from the root directory of this repo):

```
docker buildx build --platform linux/amd64 -t eval:eval_coreference -f evaluation_scripts/eval_coreference/Dockerfile .
```

## Run mock evaluation (from the root directory of this repo)

```
docker run -it --name eval-container_coreference --rm \
-v $PWD/evaluation_scripts/eval_coreference/sample_ground_truth.zip:/ground_truth.zip \
-v $PWD/evaluation_scripts/eval_coreference/sample_submission.zip:/submission.zip \
eval:eval_coreference ground_truth.zip submission.zip
```

This command should result in an output like this:  

```
{
  "status": "S",
  "metrics": {
    "Precision(muc)": 1.0,
    "Recall(muc)": 0.7222222222222222,
    "F1(muc)": 0.8387096774193548,
    "Precision(bcub)": 1.0,
    "Recall(bcub)": 0.7111111111111111,
    "F1(bcub)": 0.8311688311688311,
    "Precision(ceafe)": 0.9777777777777779,
    "Recall(ceafe)": 0.7333333333333334,
    "F1(ceafe)": 0.8380952380952381,
    "Precision(ceafm)": 1.0,
    "Recall(ceafm)": 0.7333333333333333,
    "F1(ceafm)": 0.846153846153846,
    "Precision(blanc)": 1.0,
    "Recall(blanc)": 0.6197560975609756,
    "F1(blanc)": 0.7604987121579753,
    "Precision(lea)": 1.0,
    "Recall(lea)": 0.7,
    "F1(lea)": 0.8235294117647058,
    "Precision(mor)": 1.0,
    "Recall(mor)": 0.7468354430379747,
    "F1(mor)": 0.855072463768116,
    "conll": 0.8359912488944747
  },
  "evaluation_time": 0.038627,
  "error_report": ""
}
```

Please note that you may also re-use the above evaluation procedure on other CorefUD-formatted coreference corpora 
(e.g., coref149). To do so, replace `sample_ground_truth.zip` and `sample_submission.zip` with your ground truth and 
submission, respectively.


