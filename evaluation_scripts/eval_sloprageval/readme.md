# Slobench evaluation scripts for the SloPragEval benchmark

The directory contains evaluation scripts for the <b>SloPragEval</b> leaderboard which evaluates model performance on **pragmatics understanding** in a **multiple-choice question-answering** (MCQA) task.


### NOTE:

❗ All commands should be **run from the root directory** of the repository.

## 🐋 Build the Docker image:

```
docker buildx build --platform linux/amd64 -t slobench/eval:sloprageval -f evaluation_scripts/eval_sloprageval/Dockerfile .
```

## 🐳 Run mock evaluation:

You can run a mock evaluation within SloBENCH as follows (files '_sample_reference.zip_' and '_sample_submission.zip_' are already provided):

``` 
docker run -it --name eval-container_prageval --rm -v ${PWD}/evaluation_scripts/eval_sloprageval/sample_reference.zip:/reference.zip -v ${PWD}/evaluation_scripts/eval_sloprageval/sample_submission.zip:/sample_submission.zip slobench/eval:sloprageval reference.zip sample_submission.zip
```
## 📈 Get result

The above command should result in an output like the one below, reporting the **Accuracy per maxim** and the overall **Average accuracy**:  

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



