# SloBENCH evaluation script - question answering

All commands should be run from the root directory of this repository.

## Build docker image 
```
docker buildx build --platform linux/amd64 -t slobench/eval:question_answering -f evaluation_scripts/eval_question_answering/Dockerfile .
```

## Run evaluation 

Evaluation within SloBENCH will be run as follows:

```
docker run -it --name eval-container_question_answering --rm \
-v $PWD/evaluation_scripts/eval_question_answering/reference_dataset.zip:/reference_dataset.zip \
-v $PWD/evaluation_scripts/eval_question_answering/submission.zip:/submission.zip \
slobench/eval:question_answering_1.1 reference_dataset.zip submission.zip
```

As `reference_dataset.zip` for `test.zip` is not available, you can do manual testing as follows:


```
docker run -it --name eval-container_question_answering --rm \
-v $PWD/evaluation_scripts/eval_question_answering/qa_validation.zip:/reference_dataset.zip \
-v $PWD/evaluation_scripts/eval_question_answering/qa_validation.zip:/submission.zip \
slobench/eval:question_answering_1.1 reference_dataset.zip submission.zip
```

This command should result in an output like this:


```
{
  "status": "S",
  "metrics": {
    "BoolQ Accuracy": 1.0,
    "CB Accuracy": 1.0,
    "CB F1 Score": 1.0,
    "CB Average": 1.0,
    "COPA Accuracy": 1.0,
    "MultiRC F1a Score": 1.0,
    "MultiRC EM": 1.0,
    "MultiRC Average": 1.0,
    "RTE Accuracy": 1.0,
    "WSC Accuracy": 1.0,
    "Average": 1.0
  },
  "evaluation_time": 0.177651,
  "error_report": ""
}
```

If you prepare your own split (from validation or train part of data), adjust volume parameters accordingly. For example, testing your output on validation data split: 

```
docker run -it --name eval-container_question_answering --rm \
-v $PWD/evaluation_scripts/eval_question_answering/qa_validation.zip:/reference_dataset.zip \
-v PATH_TO_MY_VALIDATION_DATA_PREDICTIONS.zip:/submission.zip \
slobench/eval:question_answering_1.1 reference_dataset.zip submission.zip
```

## Reference output check

```
docker run -it --name eval-container_question_answering --rm \
-v $PWD/evaluation_scripts/eval_question_answering/sample_reference_dataset.zip:/reference_dataset.zip \
-v $PWD/evaluation_scripts/eval_question_answering/sample_submission.zip:/submission.zip \
slobench/eval:question_answering_1.1 reference_dataset.zip submission.zip
```

This command should result in an output like this:


```
{
  "status": "S",
  "metrics": {
    "BoolQ Accuracy": 0.6666666666666666,
    "CB Accuracy": 0.6666666666666666,
    "CB F1 Score": 0.4,
    "CB Average": 0.5333333333333333,
    "COPA Accuracy": 0.6666666666666666,
    "MultiRC F1a Score": 0.4,
    "MultiRC EM": 0.0,
    "MultiRC Average": 0.2,
    "RTE Accuracy": 0.6666666666666666,
    "WSC Accuracy": 0.0,
    "Average": 0.45555555555555555
  },
  "evaluation_time": 0.196328,
  "error_report": ""
}
```