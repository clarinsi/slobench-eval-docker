FROM python:3.10.22-bookworm

COPY evaluation_scripts/eval_speech_recognition_v2/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY evaluation_scripts/eval_speech_recognition_v2/evaluate.py ./evaluate.py
COPY run.py ./run.py

ENTRYPOINT ["python", "run.py"]