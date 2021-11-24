FROM python:3.8.11-bullseye

COPY evaluation_scripts/eval_sequence_tagging_conllu/conll18_ud_eval.py ./conll18_ud_eval.py
COPY evaluation_scripts/eval_sequence_tagging_conllu/evaluate.py ./evaluate.py
COPY run.py ./run.py

ENTRYPOINT ["python", "run.py"]



