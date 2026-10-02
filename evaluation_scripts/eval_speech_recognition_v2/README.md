# eval_speech_recognition_v2 slobench evaluation script
This folder also contains reference dataset (ground truth) and submission .zip files for mock testing
(these obviously won't be included in the public repo).

## Build docker image (from the root directory of this repo):
```
docker buildx build --platform linux/amd64 -t slobench/eval:speech_recognition_2.0 -f evaluation_scripts/eval_speech_recognition_v2/Dockerfile .
```

## Run mock evaluation (from the root directory of this repo)
```
docker run -it --name eval_speech_recognition_v2 --rm \
-v $PWD/evaluation_scripts/eval_speech_recognition_v2/sample_reference.zip:/sample_reference.zip \
-v $PWD/evaluation_scripts/eval_speech_recognition_v2/sample_submission.zip:/sample_submission.zip \
slobench/eval:speech_recognition_2.0 sample_reference.zip sample_submission.zip
```

Expected output:

```json
 {
  "status": "S",
  "metrics": {
    "CER": 0.2881,
    "WER": 0.5523,
    "1-WER": 0.44,
    "MER": 0.5212,
    "WIL": 0.7226,
    "WIP": 0.2773,
    "NORM": 0.105,
    "VERB": 0.3543
  },
  "evaluation_time": 13.503033,
  "error_report": ""
}
```