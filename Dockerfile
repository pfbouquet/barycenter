FROM python:3.7-slim

WORKDIR /smart-meeting-place

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "flask_app.py"]
