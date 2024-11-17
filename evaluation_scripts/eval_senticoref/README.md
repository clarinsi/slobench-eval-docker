# eval_senticoref slobench evaluation script

All commands should be run from the root directory of the repository.

## Build docker image (from the root directory of this repo):

```
docker buildx build --platform linux/amd64 -t eval:eval_senticoref -f evaluation_scripts/eval_senticoref/Dockerfile .
```

## Run mock evaluation (from the root directory of this repo)

```
docker run -it --name eval-container_senticoref --rm \
-v $PWD/evaluation_scripts/eval_senticoref/sample_ground_truth.zip:/ground_truth.zip \
-v $PWD/evaluation_scripts/eval_senticoref/sample_submission.zip:/submission.zip \
eval:eval_senticoref ground_truth.zip submission.zip
```