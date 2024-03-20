# Node
FROM node:21
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["node", "index.js"]


# python things

# FROM python:3.9-slim
# WORKDIR /app
# COPY requirements.txt .
# COPY match.py .
# RUN pip install --no-cache-dir -r requirements.txt
# CMD ["python", "match.py"]


