# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install required Python packages
RUN pip install --no-cache-dir google-api-python-client kafka-python python-dotenv

# Set build-time argument for API key
ARG YOUTUBE_API_KEY

# Pass the API key to the environment
ENV YOUTUBE_API_KEY=${YOUTUBE_API_KEY}

# Run the Python script when the container launches
CMD ["python", "./fetch_youtube_data.py"]
