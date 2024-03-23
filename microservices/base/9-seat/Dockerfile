FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
COPY seat.py .

COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "seat.py"]
