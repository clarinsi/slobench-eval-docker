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
    "Sentences Precision": 1.0,
    "Sentences Recall": 1.0,
    "Sentences F1 Score": 1.0,
    "Tokens Precision": 1.0,
    "Tokens Recall": 1.0,
    "Tokens F1 Score": 1.0,
    "Lemmas Precision": 1.0,
    "Lemmas Recall": 1.0,
    "Lemmas F1 Score": 1.0,
    "XPOS Precision": 0.9678710757981168,
    "XPOS Recall": 0.9678710757981168,
    "XPOS F1 Score": 0.9678710757981168,
    "UPOS Precision": 0.9869074123245981,
    "UPOS Recall": 0.9869074123245981,
    "UPOS F1 Score": 0.9869074123245981,
    "UFeats Precision": 0.9717927245246022,
    "UFeats Recall": 0.9717927245246022,
    "UFeats F1 Score": 0.9717927245246022,
    "LAS Precision": 1.0,
    "LAS Recall": 1.0,
    "LAS F1 Score": 1.0,
    "UAS Precision": 1.0,
    "UAS Recall": 1.0,
    "UAS F1 Score": 1.0
  },
  "evaluation_time": 10.367655,
  "error_report": ""
}
```