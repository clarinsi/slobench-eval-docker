FROM python:3.8.11-bullseye

COPY evaluation_scripts/eval_senticoref/scorer ./scorer
COPY evaluation_scripts/eval_senticoref/ua-scorer.py .
COPY evaluation_scripts/eval_senticoref/evaluate_corefud.py .
COPY evaluation_scripts/eval_senticoref/evaluate.py .
COPY evaluation_scripts/eval_senticoref/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY run.py .

ENTRYPOINT ["python3", "run.py"]