# eval_speech_recognition_v2 slobench evaluation script

This folder also contains reference dataset (ground truth) and submission .zip files for mock testing
(these obviously won't be included in the public repo).

## Build docker image (from the root directory of this repo):

```
docker buildx build --platform linux/amd64 -t slobench/eval:speech_recognition_v2_1.1 -f evaluation_scripts/eval_speech_recognition_v2/Dockerfile .
```

## Run mock evaluation (from the root directory of this repo)

```
docker run -it --name eval_speech_recognition_v2 --rm \
-v $PWD/evaluation_scripts/eval_speech_recognition_v2/sample_reference.zip:/sample_reference.zip \
-v $PWD/evaluation_scripts/eval_speech_recognition_v2/sample_submission.zip:/sample_submission.zip \
slobench/eval:speech_recognition_v2_1.1 sample_reference.zip sample_submission.zip
```

Expected output:

```json
{
  "status": "S",
  "metrics": {
    "CER1": 0.0312,  # Results for SloBench Speech Recognition data
    "WER1": 0.0435,  # Results for SloBench Speech Recognition data
    "MER1": 0.0435,  # Results for SloBench Speech Recognition data
    "WIL1": 0.0435,  # Results for SloBench Speech Recognition data
    "NORM1": 0.75,   # Results for SloBench Speech Recognition data
    "VERB1": 0.0,    # Results for SloBench Speech Recognition data
    "CER2": 0.1739,  # Results for Govorjena Slovenščina Data
    "WER2": 0.2632,  # Results for Govorjena Slovenščina Data
    "MER2": 0.25,    # Results for Govorjena Slovenščina Data
    "WIL2": 0.3767,  # Results for Govorjena Slovenščina Data
    "NORM2": 0.0,    # Results for Govorjena Slovenščina Data
    "VERB2": 0.0     # Results for Govorjena Slovenščina Data
  },
  "evaluation_time": 13.503033,
  "error_report": ""
}
```

# Info to populate the slobench website with

# Short description:

This benchmark scores submissions against colloquial and normalised transcripts and accounts for optional disfluencies.

# Description

# Multi-reference ASR benchmark

This benchmark uses much harder data from the Govorjena Sloveniščina portal and compares submissions against all possible reference constructed from the colloquial and normalised tiers, handling disfluencies as optional signal.

## The data
Two data sources:
* Existing SloBench Speech Recognition recordings (3h18min)
* New recordings from Govorjena Slovenščina portal (1h6min)

Each has two tiers two tiers: colloquial and normalised, and in each tier parts of the transcript can be marked as "deletable elements", meaning they can be removed from the transcript without affecting the evaluation. In practice they mostly prove to be filled pauses like `{uhm}` and repetitions or false starts, e.g. `{če bi} če bi ti šel`. Transcriptions can also include notes such as `[dih]` or `[smeh]`, but they are not used for evaluation.


## Multi-reference evaluation

This benchmark performs the same pre-processing as the previous speech recognition benchmark, but the metrics calculation now uses "gold" transcriptions obtained by constructing a transcription from both available tiers and optimally including the deletable elements.

On top of the previous benchmark, two new metrics are added:

- `NORM`: degree of normalisation, or how much better than colloq the normalised transcription is defined as (WER@colloq - WER@norm) / WER@colloq
- `VERB`: verbosity, defined as the percentage of included deletable elements.

These two metrics don't directly measure the performance of a model, but they provide insights into how the model is transcribing the audio: does it normalise its output or stick closer to the spoken signal, and does it prune the output to the bare minimum or output everything as has been said?

The methodology is explained in the paper below:

```bibtex
@misc{rupnik_2026_22766139,
  author       = {Rupnik, Peter and
                  Ljubešić, Nikola},
  title        = {Beyond WER and CER: Multi-Reference Evaluation for
                   Slovenian Speech Recognition Benchmarking
                  },
  year         = 2026,
  publisher    = {Institute of Contemporary History},
  doi          = {10.5281/zenodo.22766139},
  url          = {https://doi.org/10.5281/zenodo.22766139},
}
```

# Submission instructions

Check sample submission for a general idea of how the submission should look like.

It should be a ZIP archive containing a single file named asr_sample_submission.jsonl as so:

```
my_zipped_archive.zip:
└── asr_sample_submission.jsonl
```

The submission file is a line-delimited JSON file containing the audio ID and ASR output for each audio instance:

```
{"id":"GSO-P0051_T57-77_T59-717_57.770_59.717_SloBench-0099","text":"Mislim, da ne."}
{"id":"GSO-P0051_T236-12_T237-340_236.120_237.340_SloBench-0099","text":"Panirati je strašno"}
...
```


# Metrics:

The benchmark is evaluated separately for the two data sources, which is encoded in the metric key suffix: `1` for SloBench and `2` for GSO.

```
[
  {
    "CER1": "CER (SloBench)"
  },
  {
    "WER1": "WER (SloBench)"
  },
  {
    "MER1": "MER (SloBench)"
  },
  {
    "WIL1": "WIL (SloBench)"
  },
  {
    "NORM1": "NORM (SloBench)"
  },
  {
    "VERB1": "VERB (SloBench)"
  },
  {
    "CER2": "CER (GSO)"
  },
  {
    "WER2": "WER (GSO)"
  },
  {
    "MER2": "MER (GSO)"
  },
  {
    "WIL2": "WIL (GSO)"
  },
  {
    "NORM2": "NORM (GSO)"
  },
  {
    "VERB2": "VERB (GSO)"
  }
]
```