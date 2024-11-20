FROM python:3.8.11-bullseye

COPY evaluation_scripts/eval_coreference/scorer ./scorer
COPY evaluation_scripts/eval_coreference/ua-scorer.py .
COPY evaluation_scripts/eval_coreference/evaluate_corefud.py .
COPY evaluation_scripts/eval_coreference/evaluate.py .
COPY evaluation_scripts/eval_coreference/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY run.py .

ENTRYPOINT ["python3", "run.py"]