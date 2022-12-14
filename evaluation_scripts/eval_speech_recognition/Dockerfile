FROM python:3.8.11-bullseye

COPY evaluation_scripts/eval_speech_recognition/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY evaluation_scripts/eval_speech_recognition/asr_eval.py ./asr_eval.py
COPY evaluation_scripts/eval_speech_recognition/evaluate.py ./evaluate.py
COPY run.py ./run.py

ENTRYPOINT ["python", "run.py"]



