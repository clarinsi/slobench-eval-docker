FROM python:3.8.11-bullseye

COPY evaluation_scripts/eval_ke_wsc/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY evaluation_scripts/eval_ke_wsc/ke_wsc_eval.py ./ke_wsc_eval.py
COPY evaluation_scripts/eval_ke_wsc/evaluate.py ./evaluate.py
COPY run.py ./run.py

ENTRYPOINT ["python", "run.py"]