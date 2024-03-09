# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .
COPY videoasset.py .
COPY .env.example .
# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the events.py file into the container

# Set the command to run when the container starts
CMD ["python", "videoasset.py"]
