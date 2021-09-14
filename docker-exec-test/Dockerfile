FROM python:3.8.11-bullseye

RUN mkdir -p /scripts && \
    mkdir -p /input-files
WORKDIR /scripts

RUN pip install --no-cache-dir scikit-learn===0.24.2

COPY runner-script.py ./runner-script.py

CMD [ "python", "./runner-script.py" ]