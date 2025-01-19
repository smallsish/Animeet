from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import pika
import json

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# RabbitMQ connection parameters
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
QUEUE_NAME = "notifications"

# Health check route
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"message": "Service is healthy", "service": "notifications"}), 200

# Publish a notification request to RabbitMQ queue
@app.route('/publish-notification', methods=['POST'])
def publish_notification():
    data = request.json
    user_id = data.get("user_id")
    event_id = data.get("event_id")
    user_name = data.get("user_name")  # User's name
    event_name = data.get("event_name")  # Event name
    price = data.get("price")  # Price in cents
    email = data.get("email")

    # Ensure all required fields are present
    if not all([user_id, event_id, email, user_name, event_name, price]):
        return jsonify({"message": "Missing one or more required fields: user_id, event_id, user_name, event_name, price, email"}), 400

    # Payload with notification details
    payload = {
        "user_id": user_id,
        "event_id": event_id,
        "user_name": user_name,
        "event_name": event_name,
        "price": price / 100, # Convert to dollars for display
        "email": email,
        "type": "payment"
    }
    
    # Attempt to send the message to RabbitMQ
    try:
        connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=QUEUE_NAME,
            body=json.dumps(payload),
            properties=pika.BasicProperties(delivery_mode=2)  # Persistent message
        )
        connection.close()
        return jsonify({
            "message": "Notification request sent to queue",
            "user_id": user_id,
            "event_id": event_id,
            "user_name": user_name,
            "event_name": event_name,
            "price": f"${price / 100:.2f}",
            "email": email
        }), 200
    except Exception as e:
        print(f"Failed to publish notification to RabbitMQ: {str(e)}")
        return jsonify({"message": f"Failed to publish notification: {str(e)}"}), 500


# Publish a notification request to RabbitMQ queue
@app.route('/publish-join-notification', methods=['POST'])
def publish_join_notification():
    data = request.json
    email = data.get("email")
    subject = data.get("subject")
    body = data.get("body")

    # Ensure all required fields are present
    if not all([email, subject, body]):
        return jsonify({"message": "Missing one or more required fields: email, subject, body"}), 400

    # Payload with notification details
    payload = {
        "subject": subject,
        "body": body,
        "email": email,
        "type": "join"
    }
    
    # Attempt to send the message to RabbitMQ
    try:
        connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=QUEUE_NAME,
            body=json.dumps(payload),
            properties=pika.BasicProperties(delivery_mode=2)  # Persistent message
        )
        connection.close()
        return jsonify({
            "message": "Notification request sent to queue",
            "subject": subject,
            "body": body,
            "email": email
        }), 200
    except Exception as e:
        print(f"Failed to publish notification to RabbitMQ: {str(e)}")
        return jsonify({"message": f"Failed to publish notification: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("APP_PORT", 5000)))