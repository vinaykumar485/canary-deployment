FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV APP_VERSION=v2

EXPOSE 80

CMD ["python","app.py"]
