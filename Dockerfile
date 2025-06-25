FROM python:3.10-slim
WORKDIR /app
COPY cleaner.py .
ENTRYPOINT ["python","cleaner.py"]