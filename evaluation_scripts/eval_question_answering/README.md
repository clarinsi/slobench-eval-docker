# SloBENCH evaluation script - question answering

All commands should be run from the root directory of this repository.

## Build docker image 
```
docker build -t eval:eval_question_answering -f evaluation_scripts/eval_question_answering/Dockerfile .
```

## Run evaluation 

Evaluation within SloBENCH will be run as follows:

```
docker run -it --name eval-container_question_asnwering --rm \
-v $PWD/evaluation_scripts/eval_question_answering/qa_ground_truth.zip:/ground_truth.zip \
-v $PWD/evaluation_scripts/eval_question_answering/qa_submission.zip:/submission.zip \
eval:eval_question_answering ground_truth.zip submission.zip
```

As `qa_ground_truth.zip` for `qa_test.zip` is not available, you can do manual testing as follows:


```
docker run -it --name eval-container_question_asnwering --rm \
-v $PWD/evaluation_scripts/eval_question_answering/qa_validation.zip:/ground_truth.zip \
-v $PWD/evaluation_scripts/eval_question_answering/qa_validation.zip:/submission.zip \
eval:eval_question_answering ground_truth.zip submission.zip
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
docker run -it --name eval-container_question_asnwering --rm \
-v $PWD/evaluation_scripts/eval_question_answering/qa_validation.zip:/ground_truth.zip \
-v PATH_TO_MY_VALIDATION_DATA_PREDICTIONS.zip:/submission.zip \
eval:eval_question_answering ground_truth.zip submission.zip
```