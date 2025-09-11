FROM python:3.8.11-bullseye

COPY evaluation_scripts/eval_pragmega/requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY evaluation_scripts/eval_pragmega/pragmegaeval.py ./pragmegaeval.py
COPY evaluation_scripts/eval_pragmega/evaluate.py ./evaluate.py
COPY run.py ./run.py

ENTRYPOINT ["python", "run.py"]