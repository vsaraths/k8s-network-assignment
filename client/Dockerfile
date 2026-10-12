FROM python:3.12-slim
WORKDIR /app
COPY Client.py .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "Client.py"]
