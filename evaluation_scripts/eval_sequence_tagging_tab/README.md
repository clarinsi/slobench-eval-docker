# SloBENCH evaluation script - sequence_tagging_tab

All commands should be run from the root directory of this repository.

## Build docker image 
```
docker buildx build --platform linux/amd64 -t slobench/eval:sequence_tagging_tab -f evaluation_scripts/eval_sequence_tagging_tab/Dockerfile .
```

## Run evaluation 

Evaluation within SloBENCH will be run as follows:

```
docker run -it --name eval-container_sequence_tagging_tab --rm \
-v $PWD/evaluation_scripts/eval_sequence_tagging_tab/reference.zip:/reference_dataset.zip \
-v $PWD/evaluation_scripts/eval_sequence_tagging_tab/submission.zip:/submission.zip \
slobench/eval:sequence_tagging_tab_1.1 reference_dataset.zip submission.zip
```

As `reference.zip` is not available, you can do manual testing as follows:


```
docker run -it --name eval-container_sequence_tagging_tab --rm \
-v $PWD/evaluation_scripts/eval_sequence_tagging_tab/sample_reference.zip:/reference_dataset.zip \
-v $PWD/evaluation_scripts/eval_sequence_tagging_tab/sample_submission.zip:/submission.zip \
slobench/eval:sequence_tagging_tab_1.1 reference_dataset.zip submission.zip
```

This command should result in an output like this:


```
{
  "status": "S",
  "metrics": {
    "Precision": 0.9811290281848772,
    "Recall": 0.9829913004684363,
    "F1 score": 0.9818619988615366
  },
  "evaluation_time": 0.459997,
  "error_report": ""
}
```