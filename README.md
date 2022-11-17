![](cjvt-header.png)
# SloBENCH official evaluation scripts


This is an accompanying repository that contains evaluation scripts used by the evaluation leaderboards in SloBENCH tool - [https://slobench.cjvt.si](https://slobench.cjvt.si).

## Submission evaluation methodology.
SloBENCH tool expects a user to upload a `submission.zip` file that contains contents according to the rules of a specific leaderboard.

> Note: Zip file must not contain any other files, not expected by the system (e.g., __MACOSX). To be sure your submission is sound, you may use zip command from command line - for example: `zip submission.zip ./*.txt`

Uploaded submission file is automatically extracted along with the `reference_dataset.zip` file.

The `run.py` script unzips the ground truth data into the `/data-reference` path and the submitted data into `/data-submission`.

Then it runs the task's corresponding `eval.py` evaluation script, which compares the contents of the previously mentioned paths and returns a dictionary of *metricName:metricScore* pairs, for example:

```
{
    'overall': 88.2,
    'metric1': 100.0,
    'metric2': 32.1,
    'metric3': 123.33
}
```

Script `run.py` returns evaluation results (or possibly an error) along with some running metadata into a Task Submission Evaluation Object, which is passed to the SloBENCH Web Server.

## Leaderboard evaluation
Each evaluation script is packaged into its own container - see specific Dockerfiles for your target leaderboard.

When a new task evaluation script gets added to this repo, the a docker container gets composed and pushed to the `slobench/eval:[TASK-NAME]` docker repo.

## Compiling and running an evaluation locally
Build docker image from root directory of this repository, cloned to your machine, as follows:

```
docker buildx build --platform linux/amd64 -t eval:TASK_NAME -f evaluation_scripts/TASK_NAME/Dockerfile .
```

Test your evaluation as follows:

```
docker run -it --name eval-container --rm \
-v $PWD/DATA_WITH_LABELS.zip:/ground_truth.zip \
-v $PWD/YOUR_SYSTEM_OUTPUT_DATA.zip:/submission.zip \
eval:TASK_NAME ground_truth.zip submission.zip
```
Change *TASK-NAME* accordingly and provide paths to your samples of ground truth/reference data (i.e., *DATA_WITH_LABELS.zip*) and your system output (i.e., *YOUR_SYSTEM_OUTPUT_DATA.zip*) for the reference data.

For more information check README file of selected leaderboard.

## Pushing an image to DockerHub

This repository is accompanied with DockerHub repository [https://hub.docker.com/r/slobench/eval](https://hub.docker.com/r/slobench/eval). Images are pushed from local builds using the following commands:

```
docker login
docker tag eval:eval_TASK-NAME slobench/eval:TASK-NAME_VERSION
docker push slobench/eval:TASK-NAME_VERSION
```

## Currently supported tasks

This repository supports the following tasks:

* **eval\_question\_answering**: Evaluation of selected SuperGLUE-like QA tasks.
* **eval\_sequence\_tagging\_conllu**: General CONLLU-based evaluation tasks.
* **eval\_sequence\_tagging\_tab**: General sequence labelling evaluation tasks.
* **eval\_summarization**: Text summarization evaluation.
* **eval\_translation_en**: Machine translation evaluation (English target).
* **eval\_translation_sl**: Machine translation evaluation (Slovene target).
* **eval\_sequence_pair_classification**: Sequence pair classification evaluation.

----


<center>
<table border="0" style="border: none;">
	<tr>
		<td>
			<img src="cjvt-logo.png" width="300pt" />
		</td>
		<td>
			<img src="clarin-logo.png" width="300pt" />
		</td>
	</tr>
</table>
<center>
SloBENCH tool was developed as an [Clarin.si 2021 project](https://www.clarin.si/info/storitve/projekti).


