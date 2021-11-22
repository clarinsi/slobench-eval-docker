FROM python:3.8.11-bullseye

COPY evaluation_scripts/eval_summarization/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update \
    && apt-get install -y libxml-parser-perl=2.46-2

COPY evaluation_scripts/eval_summarization/dependencies/ROUGE-1.5.5 ./ROUGE-1.5.5
COPY evaluation_scripts/eval_summarization/summarization_eval.py ./summarization_eval.py
COPY evaluation_scripts/eval_summarization/evaluate.py ./evaluate.py
COPY run.py ./run.py

RUN /bin/bash -c '/ROUGE-1.5.5/data/WordNet-2.0-Exceptions/buildExeptionDB.pl /ROUGE-1.5.5/data/WordNet-2.0-Exceptions /ROUGE-1.5.5/data/smart_common_words.txt /ROUGE-1.5.5/data/WordNet-2.0.exc.db'

ENV ROUGE=/ROUGE-1.5.5

ENTRYPOINT ["python", "run.py"]