# slobench-eval-docker
This is a sister repo of the SloBench project. It contains the evaluation script framework.

## Structure
Upon uploading a submission to SloBench, the uploaded `submission.zip` file gets passed to a docker containter, along with the `ground_truth.zip` file.

The `run.py` script unzips the ground truth data into the `/data-truth` path and the submitted data into `/data-submission`.

It then runs the task's corresponding `eval.py` evaluation script, which compares the contents of the previously mentioned paths and returns a dictionary of metricName:metricScore pairs, eg.:
```
{
    'overall': 88.2,
    'metric1': 100.0,
    'metric2': 32.1,
    'metric3': 123.33
}
```

`run.py` finally puts all of this into a TSEO (Task Submission Evaluation Object), containing the metric scores of the evaluation + some metadata, which get passed back to the SloBench server.

## Dockerfile
Each evaluation script has it's own Dockerfile, to enable custom environments for evaluation (custom Python versions, ...).

When a new task evaluation script gets added to this repo, the a docker container gets composed and pushed to the `slobench/eval:[TASK-NAME]` docker repo.

## Compiling a task evaluation docker image
Build docker image (from root directory of this repo):
```
docker build -t eval:TASK_NAME -f evaluation_scripts/TASK_NAME/Dockerfile .
```

Run mock evaluation
```
docker run -it --name eval-container --rm -v /submission.json.zip:/submission.zip -v /submission.json.zip:/test_dataset.zip eval:TASK_NAME test_dataset.zip submission.zip
```

## Currently supported tasks
- eval_prototype