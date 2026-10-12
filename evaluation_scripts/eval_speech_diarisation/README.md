# Speech Diarisation Benchmark

This folder contains sample reference and sample submission datasets
for evaluating speech diarisation systems.

## Submission Format

Submissions should be a zip file containing two RTTM files:

```
.
├── ROG-Art.rttm
└── ROG-Dialog.rttm
```
## Metrics

Metrics are calculated separately for `ROG-Art` and `ROG-Dialog` and
reported as percentages:

| Metric | Description            | Meaning                            |
| ------ | ---------------------- | ---------------------------------- |
| DER    | Diarisation Error Rate | Overall error, sum of MISS+FA+CONF |
| MISS   | Missed Speech Rate     | Speech not detected                |
| FA     | False Alarm Rate       | Non-speech detected as speech      |
| CONF   | Confusion Rate         | Speaker misattribution             |
### Example metric output

```json
{
    "DER_ROG-Art": 44.33,
    "MISS_ROG-Art": 30.53,
    "FA_ROG-Art": 1.75,
    "CONF_ROG-Art": 12.05,
    "DER_ROG-Dialog": 21.86,
    "MISS_ROG-Dialog": 8.55,
    "FA_ROG-Dialog": 4.24,
    "CONF_ROG-Dialog": 9.08
}
```

## RTTM Format

Each line in an RTTM file consists of whitespace-separated fields:

```rttm
SPEAKER <file id> 1 <start seconds> <duration seconds> <NA> <NA> <speaker id> <NA> <NA>
```

See the sample submission for examples.

## Downloading Audio Files

```bash
curl --remote-name-all https://www.clarin.si/repository/xmlui/bitstream/handle/11356/2062/ROG-Art.wav.zip
curl --remote-name-all https://www.clarin.si/repository/xmlui/bitstream/handle/11356/2073/ROG-Dialog_audio.zip
```

# Build docker image (from the root directory of this repo):
```
docker build --platform linux/amd64 -t slobench/eval:speech_diarisation_1.0 -f evaluation_scripts/eval_speech_diarisation/Dockerfile .
```

# Run mock evaluation (from the root directory of this repo)
```
docker run -it --name eval_speech_diarisation --rm \
-v $PWD/evaluation_scripts/eval_speech_diarisation/sample_reference.zip:/reference_dataset.zip \
-v $PWD/evaluation_scripts/eval_speech_diarisation/sample_submission.zip:/submission.zip \
slobench/eval:speech_diarisation_1.0 reference_dataset.zip submission.zip
```
