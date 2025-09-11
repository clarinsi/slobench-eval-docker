# Slobench evaluation scripts for the SloPragEval benchmark

The directory contains evaluation scripts for the <b>SloPragMega</b> leaderboard which evaluates model performance on **understanding Metaphor, Irony, and Humour** in a **multiple-choice question-answering** (MCQA) task.


### NOTE:

❗ All commands should be **run from the root directory** of the repository.

## 🐋 Build the Docker image:

```
docker buildx build --platform linux/amd64 -t slobench/eval:pragmega -f evaluation_scripts/eval_pragmega/Dockerfile .
```

## 🐳 Run mock evaluation:

You can run a mock evaluation within SloBENCH as follows (files '_pragmega_sample_reference.zip_' and '_pragmega_sample_submission.zip_' are already provided):

``` 
docker run -it --name eval-container_pragmega --rm -v ${PWD}/evaluation_scripts/eval_pragmega/pragmega_sample_reference.zip:/reference.zip -v ${PWD}/evaluation_scripts/eval_pragmega/pragmega_sample_submission.zip:/sample_submission.zip slobench/eval:pragmega reference.zip sample_submission.zip
```
## 📈 Get result

The above command should result in an output like the one below, reporting the **Accuracy per Type (Metaphor/Irony/Humour)** and the overall **Average accuracy**:  

```

{
  "status": "S",
  "metrics": {
    "Metaphor Accuracy": 0.5,
    "Irony Accuracy": 0.5,
    "Humour Accuracy": 1.0,
    "Average Accuracy": 0.6666666666666666
  },
  "evaluation_time": 0.014919,
  "error_report": ""
}



```


