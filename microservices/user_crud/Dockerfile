# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the user_crud.py file into the container
COPY user_crud.py .

# Copy the user_schemas.py file into the container
COPY user_schemas.py .

# Copy the main.py file into the container
COPY main.py .

# Set the command to run when the container starts
CMD ["python", "main.py"]
