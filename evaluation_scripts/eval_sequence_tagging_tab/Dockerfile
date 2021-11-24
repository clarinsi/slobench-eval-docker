FROM python:3.8.11-bullseye

COPY evaluation_scripts/eval_sequence_tagging_tab/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY evaluation_scripts/eval_sequence_tagging_tab/tagging_tab_eval.py ./tagging_tab_eval.py
COPY evaluation_scripts/eval_sequence_tagging_tab/evaluate.py ./evaluate.py
COPY run.py ./run.py

ENTRYPOINT ["python", "run.py"]



