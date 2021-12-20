# SloBENCH evaluation script - translation

All commands should be run from the root directory of this repository.

## Build docker image 
```
docker build -t eval:eval_translation -f evaluation_scripts/eval_translation/Dockerfile .
```

## Run evaluation 

Evaluation within SloBENCH will be run as follows:

```
docker run -it --name eval-container_translation --rm \
-v $PWD/evaluation_scripts/eval_translation/reference.zip:/reference_dataset.zip \
-v $PWD/evaluation_scripts/eval_translation/submission.zip:/submission.zip \
eval:eval_translation reference_dataset.zip submission.zip
```

As `reference.zip` is not available, you can do manual testing as follows:


```
docker run -it --name eval-container_translation --rm \
-v $PWD/evaluation_scripts/eval_translation/sample_reference.zip:/reference_dataset.zip \
-v $PWD/evaluation_scripts/eval_translation/sample_submission.zip:/submission.zip \
eval:eval_translation reference_dataset.zip submission.zip
```

This command should result in an output like this:


```
{
  "status": "S",
  "metrics": {
    "BLEU (avg)": 0.540459638826303,
    "METEOR (avg)": 0.6818485042165279,
    "CHRF (avg)": 0.632641023976876,
    "BLEU (corpus)": 0.5815499689913606,
    "CHRF (corpus)": 0.6326410239768762
  },
  "evaluation_time": 1.876391,
  "error_report": ""
}
```