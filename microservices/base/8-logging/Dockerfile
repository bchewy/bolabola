# Use the official Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the notification.py file into the container
COPY logging.py .
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Install any necessary dependencies
RUN pip install requests
RUN pip install pika
RUN pip install flask


# Set the command to run the notification.py script
CMD ["python", "logging.py"]
