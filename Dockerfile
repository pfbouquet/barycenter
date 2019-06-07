FROM python:3.7-slim AS tmp
WORKDIR /smart-meeting-place
COPY requirements.txt .
RUN pip install -r requirements.txt

FROM tmp
COPY . .
CMD ["python", "flask_app.py"]
