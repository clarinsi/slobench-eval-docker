FROM python:3.8.11-bullseye

COPY evaluation_scripts/eval_coref149/scorer ./scorer
COPY evaluation_scripts/eval_coref149/ua-scorer.py .
COPY evaluation_scripts/eval_coref149/evaluate_corefud.py .
COPY evaluation_scripts/eval_coref149/evaluate.py .
COPY evaluation_scripts/eval_coref149/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY run.py .

ENTRYPOINT ["python3", "run.py"]