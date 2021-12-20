# SloBENCH evaluation script - summarization

All commands should be run from the root directory of this repository.

## Build docker image 
```
docker build -t eval:eval_summarization -f evaluation_scripts/eval_summarization/Dockerfile .
```

## Run evaluation 

Evaluation within SloBENCH will be run as follows:

```
docker run -it --name eval-container_summarization --rm \
-v $PWD/evaluation_scripts/eval_summarization/reference.zip:/reference_dataset.zip \
-v $PWD/evaluation_scripts/eval_summarization/submission.zip:/submission.zip \
eval:eval_summarization reference_dataset.zip submission.zip
```

As `reference.zip` is not available, you can do manual testing as follows:


```
docker run -it --name eval-container_summarization --rm \
-v $PWD/evaluation_scripts/eval_summarization/sample_reference.zip:/reference_dataset.zip \
-v $PWD/evaluation_scripts/eval_summarization/sample_submission.zip:/submission.zip \
eval:eval_summarization reference_dataset.zip submission.zip
```

This command should result in an output like this:


```
{
  "status": "S",
  "metrics": {
    "ROUGE 1 R": 0.22946,
    "ROUGE 1 P": 0.24924,
    "ROUGE 1 F1 Score": 0.23569,
    "ROUGE 2 R": 0.07594,
    "ROUGE 2 P": 0.08206,
    "ROUGE 2 F1 Score": 0.07755,
    "ROUGE L R": 0.19514,
    "ROUGE L P": 0.21193,
    "ROUGE L F1 Score": 0.20036
  },
  "evaluation_time": 106.199886,
  "error_report": ""
}
```