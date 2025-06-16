FROM python:3.8.11-bullseye

COPY evaluation_scripts/eval_sloprageval/requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY evaluation_scripts/eval_sloprageval/sloprageval.py ./sloprageval.py
COPY evaluation_scripts/eval_sloprageval/evaluate.py ./evaluate.py
COPY run.py ./run.py

ENTRYPOINT ["python", "run.py"]