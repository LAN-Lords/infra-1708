FROM python:3.10.12-slim-buster

WORKDIR /app/
COPY . /app/

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--workers", "8"]
