# Slobench evaluation script for MultiPragEval 

All commands should be run from the root directory of the repository.

## Build docker image (from the root directory of this repo):

```
docker buildx build --platform linux/amd64 -t slobench/eval:sloprageval -f evaluation_scripts/eval_sloprageval/Dockerfile .
```

## Run mock evaluation (from the root directory of this repo)

Evaluation within SloBENCH can be run as follows (files 'sample_reference.zip' and 'sample_submission.zip' are provided):

```
 docker run -it --name eval-container_prageval --rm \
  -v ${PWD}/evaluation_scripts/eval_sloprageval/sample_reference.zip:/reference.zip \
  -v ${PWD}/evaluation_scripts/eval_sloprageval/sample_submission.zip:/sample_submission.zip \
  slobench/eval:sloprageval reference.zip sample_submission.zip
  
```

This command should result in an output like this:  

```

{                                                                                                                                                               
  "status": "S",                                                  
  "metrics": {
    "Quality Accuracy": 0.9166666666666666,
    "Quantity Accuracy": 1.0,
    "Relation Accuracy": 1.0,
    "Manner Accuracy": 0.75,
    "Literal Accuracy": 1.0,
    "Average Accuracy": 0.9333333333333332
  },
  "evaluation_time": 0.025518,
  "error_report": ""
}


```



