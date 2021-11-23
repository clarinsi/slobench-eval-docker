FROM python:3.8.11-bullseye

COPY evaluation_scripts/eval_translation/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet');"

COPY evaluation_scripts/eval_translation/translation_eval.py ./translation_eval.py
COPY evaluation_scripts/eval_translation/evaluate.py ./evaluate.py
COPY run.py ./run.py

ENTRYPOINT ["python", "run.py"]



