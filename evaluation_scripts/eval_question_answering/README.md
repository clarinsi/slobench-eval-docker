# SloBENCH evaluation script - question answering

## Build docker image (from the root directory of this repo):
```
docker build -t eval:eval_question_answering -f evaluation_scripts/eval_question_answering/Dockerfile .
```

## Run evaluation (from the root directory of this repo)
```
docker run -it --name eval-container_question_asnwering --rm \
-v $PWD/evaluation_scripts/eval_question_answering/qa_ground_truth.zip:/ground_truth.zip \
-v $PWD/evaluation_scripts/eval_question_answering/qa_submission.zip:/submission.zip \
eval:eval_question_answering ground_truth.zip submission.zip
```

```
docker run -it --name eval-container_question_asnwering --rm \
-v $PWD/evaluation_scripts/eval_question_answering/qa_validation.zip:/ground_truth.zip \
-v $PWD/evaluation_scripts/eval_question_answering/qa_validation.zip:/submission.zip \
eval:eval_question_answering ground_truth.zip submission.zip
```