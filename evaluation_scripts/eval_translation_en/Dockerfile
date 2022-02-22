FROM python:3.8.11-bullseye

COPY evaluation_scripts/eval_translation_en/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Cache BERT
RUN python -c "import bert_score.score as bert_score; bert_score(['I am the best.'], ['I am the worst.'], lang='en', verbose=True)[2].mean();"

RUN python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet'); nltk.download('omw-1.4');"


COPY evaluation_scripts/eval_translation_en/translation_eval.py ./translation_eval.py
COPY evaluation_scripts/eval_translation_en/evaluate.py ./evaluate.py
COPY run.py ./run.py

ENTRYPOINT ["python", "run.py"]



