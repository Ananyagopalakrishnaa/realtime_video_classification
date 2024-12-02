# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set environment variables to specify Python runtime for PySpark
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3

# Install OpenJDK 11
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk-headless && \
    apt-get clean;

# Set Java environment variables
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
ENV PATH $JAVA_HOME/bin:$PATH

# Create a virtual environment and set it as the default Python environment
RUN python3 -m venv /opt/venv
ENV PATH /opt/venv/bin:$PATH

# Update pip
RUN pip install --upgrade pip

# Install PySpark and Kafka integration with Spark
RUN pip install pyspark==3.1.2
RUN pip install kafka-python

# Install additional Python libraries needed for data processing
RUN pip install pandas numpy tabulate

# Set Spark configurations to include Kafka package
ENV PYSPARK_SUBMIT_ARGS="--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 pyspark-shell --conf spark.executor.extraJavaOptions=-Dio.netty.tryReflectionSetAccessible=true --conf spark.driver.extraJavaOptions=-Dio.netty.tryReflectionSetAccessible=true"

# Set the working directory in the container
WORKDIR /app

# Copy the local directory contents into the container at /app
COPY . /app

# Expose port for PySpark web UI (if needed, otherwise can be omitted)
EXPOSE 4040

# Set the default command to run the PySpark script, ensure the virtual environment is activated
CMD ["/bin/bash", "-c", "source /opt/venv/bin/activate && python mlp_script.py"]