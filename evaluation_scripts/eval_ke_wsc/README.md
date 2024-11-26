# SloBENCH evaluation script - ke_wsc

All commands should be run from the root directory of this repository.

## Build docker image 
```
docker buildx build --platform linux/amd64 -t slobench/eval:ke_wsc -f evaluation_scripts/eval_ke_wsc/Dockerfile .   
```

## Run evaluation 

Evaluation within SloBENCH will be run as follows:

```
docker run -it --name eval-container_ke_wsc --rm \
  -v ${PWD}/evaluation_scripts/eval_ke_wsc/reference.zip:/reference.zip \
  -v ${PWD}/evaluation_scripts/eval_ke_wsc/sample_submission.zip:/sample_submission.zip \
  slobench/eval:ke_wsc reference.zip sample_submission.zip
```

As `reference.zip` is not available, you can do manual testing as follows:

```
docker run -it --name eval-container_ke_wsc --rm \
  -v ${PWD}/evaluation_scripts/eval_ke_wsc/sample_reference.zip:/sample_reference.zip \
  -v ${PWD}/evaluation_scripts/eval_ke_wsc/sample_submission.zip:/sample_submission.zip \
  slobench/eval:ke_wsc sample_reference.zip sample_submission.zip
```

This command should result in an output like this:

```
{
  "status": "S",
  "metrics": {
    "label_accuracy": 0.485,
    "f1_macro_knowledge_type": 0.11940358539247393,
    "f1_macro_knowledge_subtype": 0.00962566844919786
  },
  "evaluation_time": 0.025776,
  "error_report": ""
}
```