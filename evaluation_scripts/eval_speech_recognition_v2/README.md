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

 ```
 {
  "status": "S",
  "metrics": {
    "CER": 0.288172814054587,
    "WER": 0.5523590333716916,
    "1-WER": 0.44764096662830843,
    "MER": 0.5212240868706811,
    "WIL": 0.722667648482338,
    "WIP": 0.27733235151766206,
    "NORM": 0.105561971663809,
    "VERB": 0.35406698564593303
  },
  "evaluation_time": 13.503033,
  "error_report": ""
}
```