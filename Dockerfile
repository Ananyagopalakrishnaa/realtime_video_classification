# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir google-api-python-client kafka-python

# Run the Python script when the container launches
CMD ["python", "./fetch_youtube_data.py"]
