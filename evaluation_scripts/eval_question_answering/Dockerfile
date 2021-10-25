FROM python:3.8.11-bullseye

COPY evaluation_scripts/eval_question_answering/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY evaluation_scripts/eval_question_answering/qa_eval.py ./qa_eval.py
COPY evaluation_scripts/eval_question_answering/evaluate.py ./evaluate.py
COPY run.py ./run.py

ENTRYPOINT ["python", "run.py"]