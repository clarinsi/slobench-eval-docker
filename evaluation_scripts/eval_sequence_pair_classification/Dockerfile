FROM python:3.8.11-bullseye

COPY evaluation_scripts/eval_sequence_pair_classification/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY evaluation_scripts/eval_sequence_pair_classification/eval_seq_pair.py ./eval_seq_pair.py
COPY evaluation_scripts/eval_sequence_pair_classification/evaluate.py ./evaluate.py
COPY run.py ./run.py

ENTRYPOINT ["python", "run.py"]