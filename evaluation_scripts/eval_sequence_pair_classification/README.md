# eval_sequence_pair_classification slobench evaluation script
This folder also contains ground truth and submission .zip files for mock testing (these obviously won't be included in the public repo)

## Build docker image (from the root directory of this repo):
```
docker build -t eval:eval_sequence_pair_classification -f evaluation_scripts/eval_sequence_pair_classification/Dockerfile .
```

## Run mock evaluation (from the root directory of this repo)
```
docker run -it --name eval-container_sequence_pair_classification --rm 
-v $PWD/evaluation_scripts/eval_sequence_pair_classification/sample_ground_truth.zip:/ground_truth.zip 
-v $PWD/evaluation_scripts/eval_sequence_pair_classification/sample_submission.zip:/submission.zip 
eval:eval_sequence_pair_classification ground_truth.zip submission.zip
```