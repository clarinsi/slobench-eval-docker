FROM python:3.8.11-bullseye

COPY evaluation_scripts/eval_conll2002/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY evaluation_scripts/eval_conll2002/conlleval.py ./conlleval.py
COPY evaluation_scripts/eval_conll2002/tagging_conll2002_eval.py ./tagging_conll2002_eval.py
COPY evaluation_scripts/eval_conll2002/evaluate.py ./evaluate.py
COPY run.py ./run.py

ENTRYPOINT ["python", "run.py"]



