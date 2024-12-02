import json
import numpy as np
from kafka import KafkaConsumer
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType
from pyspark.ml.feature import Tokenizer, StopWordsRemover, CountVectorizer, StandardScaler
import re
import logging
import time

logging.basicConfig(level=logging.INFO)

time.sleep(1)
# Initialize Spark session
spark = SparkSession.builder \
    .appName("YouTubeDataMLP") \
    .config("spark.driver.memory", "4g") \
    .config("spark.executor.memory", "2g") \
    .config("spark.network.timeout", "10000000") \
    .getOrCreate()


def remove_hyperlinks(text):
    return re.sub(r'http\S+', '', text)


remove_hyperlinks_udf = udf(remove_hyperlinks, StringType())
filter_short_words_udf = udf(lambda text: " ".join([word for word in text.split(" ") if len(word) >= 3]), StringType())


def preprocess_data(description, inp=1000):
    # Create a DataFrame with one row
    df = spark.createDataFrame([(description,)], ["Description"])

    # Apply hyperlink removal and filtering
    df = df.withColumn("Description", remove_hyperlinks_udf(col("Description")))
    df = df.withColumn("Description", filter_short_words_udf(col("Description")))

    # Tokenize
    tokenizer = Tokenizer(inputCol="Description", outputCol="tokens")
    df = tokenizer.transform(df)

    # Remove stop words
    remover = StopWordsRemover(inputCol="tokens", outputCol="filtered_tokens")
    df = remover.transform(df)

    # Vectorize
    vectorizer = CountVectorizer(inputCol="filtered_tokens", outputCol="features")
    df = vectorizer.fit(df).transform(df)

    # Standard scaling
    scaler = StandardScaler(inputCol="features", outputCol="scaled_features", withStd=True, withMean=True)
    scaler_model = scaler.fit(df)
    df = scaler_model.transform(df)

    # Extract the features column as a list
    features = df.select("scaled_features").rdd.flatMap(lambda x: x).collect()[0]
    features = np.array(features)

    # Pad or truncate features to match the input size
    if len(features) > inp:
        features = features[:inp]
    elif len(features) < inp:
        features = np.pad(features, (0, inp - len(features)), mode='constant')

    return features


class MLPClassifier:
    def __init__(self, inp, hsize, osize, lrate, epochs):
        self.inp = inp
        self.hsize = hsize
        self.osize = osize
        self.lrate = lrate
        self.epochs = epochs
        # Initialize weights and biases with He initialization
        self.weights_hidden = np.random.randn(inp, hsize) * np.sqrt(2 / inp)
        self.biases_hidden = np.zeros(hsize)
        self.weights_output = np.random.randn(hsize, osize) * np.sqrt(2 / hsize)
        self.biases_output = np.zeros(osize)

    def forward(self, X):
        # Forward propagation
        hidden_output = relu(np.dot(X, self.weights_hidden) + self.biases_hidden)
        output = smax(np.dot(hidden_output, self.weights_output) + self.biases_output)
        return output

def smax(x):
    expx = np.exp(x - np.max(x))
    return expx / expx.sum(axis=0)

def relu(x):
    return np.maximum(0, x)


# Initialize MLP model
inp = 1000
hsize = 18
osize = 6
lrate = 0.2
epochs = 15

mlp = MLPClassifier(inp, hsize, osize, lrate, epochs)

# Kafka consumer
consumer = KafkaConsumer(
    'youtube_topic1',
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')))

for message in consumer:
    try:
        data = message.value
        title = data['title']
        description = data['description']
        logging.info(f"Received title: {title}")
        logging.info(f"Received description: {description}")

        processed_data = preprocess_data(description, inp=1000)

        # Predict using MLP
        prediction = mlp.forward(processed_data)
        logging.info(f"Title: {title}, Predicted Category: {prediction}")
    except Exception as e:
        logging.error(f"Error processing message: {e}")