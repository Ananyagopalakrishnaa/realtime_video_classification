import os
import time
import logging
from googleapiclient.discovery import build
from kafka import KafkaProducer
from googleapiclient.errors import HttpError
import json
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

# Define Kafka bootstrap server
KAFKA_BOOTSTRAP_SERVER = 'kafka:9092'

# Define YouTube API key
# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv('YOUTUBE_API_KEY')

# Check if API key is set
if not API_KEY:
    raise ValueError("YouTube API key is not set.")


# Check if API key is set
if not API_KEY:
    raise ValueError("YouTube API key is not set.")

time.sleep(5)
# Function to connect to Kafka producer
def connect_kafka_producer():
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVER,
                value_serializer=lambda v: v.encode('utf-8')
            )
            logging.info("Successfully connected to Kafka")  
            return producer
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            time.sleep(5)

# Initialize Kafka producer
producer = connect_kafka_producer()

# Initialize YouTube client
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Define search parameters
search_params = {
    'maxResults': 10,
    'type': 'video',
    'regionCode': 'US',
}

# Define Kafka topic
KAFKA_TOPIC = 'youtube_topic1'

while True:
    try:
        # Execute YouTube search request
        search_request = youtube.search().list(part="snippet", **search_params)
        response = search_request.execute()

        # Process each video item in the response
        for item in response.get('items', []):
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            description = item['snippet']['description']
            
            # Write data to Kafka topic
            # Write data to Kafka topic
            message = {"title": title, "description": description}
            producer.send(KAFKA_TOPIC, value=json.dumps(message))

        logging.info(f"Fetched and sent {len(response.get('items', []))} videos to Kafka {KAFKA_TOPIC}")  
        
        # Wait for 5 minutes before fetching again
        time.sleep(300)
    except HttpError as e:
        logging.error(f"An error occurred: {e}")
        # Handle the error, such as retrying the request after some time
        time.sleep(60)  # Wait for 60 seconds before retrying
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")
        # Handle other unexpected errors
