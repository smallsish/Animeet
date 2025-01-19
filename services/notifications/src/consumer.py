import os
import pika
import json
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
QUEUE_NAME = "notifications"

# Function to compose and send an email
def send_email(recipient, user_name, event_name, price):
    sender = os.getenv("SENDER_EMAIL")
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    username = os.getenv("SENDER_EMAIL")
    password = os.getenv("SENDER_PASSWORD")

    # Verify SMTP configuration
    if not all([sender, smtp_server, smtp_port, username, password]):
        print("SMTP configuration is incomplete.")
        raise ValueError("SMTP configuration is incomplete in the .env file.")

    # Construct email body with personalized message
    body = (
        f"Dear {user_name},\n\n"
        f"We are pleased to inform you that your payment of ${price:.2f} for the event '{event_name}' has been successfully processed.\n\n"
        f"Thank you for using Animeet! We hope you enjoy the event.\n\n"
        f"Best Regards,\n"
        f"The Animeet Team"
    )

    # Compose and send the email
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = "Animeet Payment"
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.sendmail(sender, recipient, msg.as_string())
        print(f"Email successfully sent to {recipient}")
    except Exception as e:
        print(f"Failed to send email to {recipient}: {str(e)}")


# Function to compose and send an email
def send_join_email(recipient, subject, body):
    sender = os.getenv("SENDER_EMAIL")
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    username = os.getenv("SENDER_EMAIL")
    password = os.getenv("SENDER_PASSWORD")

    # Verify SMTP configuration
    if not all([sender, smtp_server, smtp_port, username, password]):
        print("SMTP configuration is incomplete.")
        raise ValueError("SMTP configuration is incomplete in the .env file.")

    # Compose and send the email
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.sendmail(sender, recipient, msg.as_string())
        print(f"Email successfully sent to {recipient}")
    except Exception as e:
        print(f"Failed to send email to {recipient}: {str(e)}")


# Consumer function to process notifications
def consume_notifications(stop_event=None):
    while True:
        try:
            print("Attempting to connect to RabbitMQ...")
            connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
            channel = connection.channel()
            channel.queue_declare(queue=QUEUE_NAME, durable=True)
            print(f"Connected to RabbitMQ. Listening on queue '{QUEUE_NAME}'...")

            def callback(ch, method, properties, body):
                payload = json.loads(body)
                try:
                    print(f"Processing message: {payload}")
                    if payload["type"] == "join": 
                        send_join_email(
                            recipient=payload["email"],
                            subject=payload["subject"],
                            body=payload["body"]
                        )
                        ch.basic_ack(delivery_tag=method.delivery_tag)
                        print(f"Notification processed and email sent to {payload['email']}")
                    elif payload["type"] == "payment": 
                        send_email(
                            recipient=payload["email"],
                            user_name=payload["user_name"],
                            event_name=payload["event_name"],
                            price=payload["price"]
                        )
                        ch.basic_ack(delivery_tag=method.delivery_tag)
                        print(f"Notification processed and email sent to {payload['email']}")
                    else :
                        print(f"Missing type: {payload}")
                except Exception as e:
                    print(f"Error processing message {payload}: {str(e)}")

            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

            print("Consumer is active and waiting for messages...")
            while not stop_event or not stop_event.is_set():
                connection.process_data_events(time_limit=1)

            print("Shutting down consumer...")
            connection.close()
            break

        except pika.exceptions.AMQPConnectionError as e:
            print(f"RabbitMQ connection error: {e}. Retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print(f"Unexpected error in consumer: {e}")
            time.sleep(5)

if __name__ == '__main__':
    consume_notifications()