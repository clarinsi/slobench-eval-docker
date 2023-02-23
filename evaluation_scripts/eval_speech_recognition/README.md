# SloBENCH evaluation script - speech recognition

All commands should be run from the root directory of this repository.

## Build docker image 
```
docker buildx build --platform linux/amd64 -t slobench/eval:speech_recognition_1.0 -f evaluation_scripts/eval_speech_recognition/Dockerfile .
```

## Run evaluation 

Evaluation within SloBENCH will be run as follows:

```
docker run -it --name eval-container_speech_recognition --rm \
-v $PWD/evaluation_scripts/eval_speech_recognition/reference.zip:/reference_dataset.zip \
-v $PWD/evaluation_scripts/eval_speech_recognition/submission.zip:/submission.zip \
slobench/eval:speech_recognition_1.0 reference_dataset.zip submission.zip
```

As `reference.zip` is not available, you can do manual testing as follows:


```
docker run -it --name eval-container_speech_recognition --rm \
-v $PWD/evaluation_scripts/eval_speech_recognition/sample_reference.zip:/reference_dataset.zip \
-v $PWD/evaluation_scripts/eval_speech_recognition/sample_submission.zip:/submission.zip \
slobench/eval:speech_recognition_1.0 reference_dataset.zip submission.zip
```

This command should result in an output like this:


```
{
  "status": "S",
  "metrics": {
    "CER": 0.11940298507462686,
    "WER": 0.4,
    "MER": 0.4,
    "WIL": 0.64,
    "WIP": 0.36
  },
  "evaluation_time": 3.013593,
  "error_report": ""
}
```