# SloBENCH evaluation script - sequence_tagging_conllu

All commands should be run from the root directory of this repository.

## Build docker image 
```
docker buildx build --platform linux/amd64 -t sequence_tagging_conllu -f evaluation_scripts/eval_sequence_tagging_conllu/Dockerfile .
```

## Run evaluation 

Evaluation within SloBENCH will be run as follows:

```
docker run -it --name eval-container_sequence_tagging_conllu --rm \
-v $PWD/evaluation_scripts/eval_sequence_tagging_conllu/reference.zip:/reference_dataset.zip \
-v $PWD/evaluation_scripts/eval_sequence_tagging_conllu/submission.zip:/submission.zip \
slobench/eval:sequence_tagging_conllu_1.1 reference_dataset.zip submission.zip
```

As `reference.zip` is not available, you can do manual testing as follows:


```
docker run -it --name eval-container_sequence_tagging_conllu --rm \
-v $PWD/evaluation_scripts/eval_sequence_tagging_conllu/sample_reference.zip:/reference_dataset.zip \
-v $PWD/evaluation_scripts/eval_sequence_tagging_conllu/sample_submission.zip:/submission.zip \
slobench/eval:sequence_tagging_conllu_1.1 reference_dataset.zip submission.zip
```

This command should result in an output like this:


```
{
  "status": "S",
  "metrics": {
    "LAS Precision": 1.0,
    "LAS Recall": 1.0,
    "LAS F1 Score": 1.0,
    "MLAS Precision": 0.0,
    "MLAS Recall": 0.0,
    "MLAS F1 Score": 0.0,
    "BLEX Precision": 0.0,
    "BLEX Recall": 0.0,
    "BLEX F1 Score": 0.0
  },
  "evaluation_time": 3.410189,
  "error_report": ""
}
```