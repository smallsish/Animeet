import os
import logging
import stripe
from flask import Flask, request, jsonify
from datetime import datetime, timezone, timedelta
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the Stripe API key and webhook secret from environment variables
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

# Used to construct the success and cancel URLs for the Checkout session
YOUR_DOMAIN = os.getenv("APP_DOMAIN", "http://localhost:5000")
# YOUR_DOMAIN = "http://localhost:20005"

# Initialize the Flask app
app = Flask(__name__)


if os.environ.get('db_conn'):
    app.config['SQLALCHEMY_DATABASE_URI'] = \
            os.environ.get('db_conn') + '/payment'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'mysql+mysqlconnector://root:root@mysql:3306/payment'
        # 'mysql+mysqlconnector://root:root@host.docker.internal:3306/payment'  # noqa: E501
    )

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}  # noqa: E501

# Database configuration using SQLAlchemy to manage DB interactions
# app.config["SQLALCHEMY_DATABASE_URI"] = (
#     "mysql+mysqlconnector://root:root@mysql:3306/payment"
# )
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database with Flask
db = SQLAlchemy(app)

# Configure logging to output to stdout (so it shows up in logs)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger()


# Set expiration to 10 minutes from now
expires_at = int((datetime.now() + timedelta(minutes=300)).timestamp())


# Define the Payment model to represent payment records in the database
class Payment(db.Model):
    __tablename__ = "payment"
    payment_id = db.Column(db.String(64), primary_key=True)  # Stripe payment ID  # noqa: E501
    user_id = db.Column(db.Integer, nullable=False)  # User ID
    group_id = db.Column(db.Integer, nullable=False)  # Group ID
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Convert a Payment object to a dictionary for easy JSON serialization
    def to_dict(self):
        return {
            "payment_id": self.payment_id,
            "user_id": self.user_id,
            "group_id": self.group_id,
            "date": self.date.strftime("%Y-%m-%d %H:%M:%S"),
        }


@app.route("/health", methods=["GET"])
def health_check():
    logger.debug("Health check route hit")
    return jsonify({"message": "Service is healthy", "service": "payment"}), 200  # noqa: E501


@app.route("/checkout-session", methods=["POST"])
def create_checkout_session():
    """
    Create a new payment session (checkout session) with Stripe.
    """
    data = request.get_json()
    user_id = data.get("user_id")
    group_id = data.get("group_id")
    event_id = data.get("event_id")  # Retrieve event_id from the request data
    event_name = data.get("event_name")  # Retrieve event_name from the request data  # noqa: E501
    price = data.get("price")  # Retrieve price if needed for metadata
    amount = data.get("amount")  # Amount in the smallest currency unit (e.g., cents for SGD)  # noqa: E501

    if not all([user_id, group_id, event_id, event_name, amount]):
        return (
            jsonify({
                    "message": "Invalid input, user_id, group_id, event_id, event_name, and amount are required."  # noqa: E501
            }), 400,
        )

    try:
        # Create a Checkout session with inline price
        # data instead of a Price ID
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "sgd",
                        "product_data": {"name": event_name},
                        "unit_amount": amount,
                    },
                    "quantity": 1,
                }
            ],
            metadata={
                "user_id": user_id,
                "group_id": group_id,
                "event_id": event_id,
                "event_name": event_name,
                "price": price
            },
            mode="payment",
            success_url="http://localhost/success",
            cancel_url="http://localhost/cancel",
            expires_at=expires_at,
        )

        return (
            jsonify(
                {"status": "success", "session_id": session.id, "url": session.url}  # noqa: E501
            ),
            201,
        )

    except Exception as e:
        logger.error(f"Error creating Checkout Session: {e}")
        return (
            jsonify({"message": "Error processing checkout session", "error": str(e)}),  # noqa: E501
            500,
        )


@app.route("/payments", methods=["GET"])
def get_all_payments():
    """
    Fetch all payment records from the database.
    """
    try:
        payments = Payment.query.all()
        return jsonify({"data": [payment.to_dict() for payment in payments]}), 200  # noqa: E501
    except Exception as e:
        logger.error(f"Error fetching payments: {e}")
        return jsonify({"message": "Error fetching payments"}), 500


@app.route("/payments/<int:user_id>", methods=["GET"])
def get_payments_by_user(user_id):
    """
    Fetch payment records from the database filtered by user ID.
    """
    try:
        payments = Payment.query.filter_by(user_id=user_id).all()
        if not payments:
            return jsonify({"message": "Payments not found for specified user."}), 404  # noqa: E501
        return jsonify({"data": [payment.to_dict() for payment in payments]}), 200  # noqa: E501
    except Exception as e:
        logger.error(f"Error fetching payments for user {user_id}: {e}")
        return jsonify({"message": "Error fetching payments for the user"}), 500  # noqa: E501


@app.route("/refund", methods=["POST"])
def refund_payment():
    """
    Endpoint to process a refund for a given payment intent.
    """
    data = request.get_json()
    payment_intent_id = data.get("payment_id")

    if not payment_intent_id:
        return jsonify({"error": "Missing payment_id"}), 400

    try:
        # Issue a refund for the given PaymentIntent ID
        refund = stripe.Refund.create(payment_intent=payment_intent_id)

        # Check for successful refund
        if refund["status"] == "succeeded":

            # Query the payment record by payment_id
            payment = Payment.query.filter_by(payment_id=payment_intent_id).first()  # noqa: E501
            if payment:
                # Delete the payment from the database
                db.session.delete(payment)
                db.session.commit()
                logger.info(f"Payment {payment_intent_id} successfully refunded and deleted from database.")  # noqa: E501
            return jsonify({"status": "success", "refund_id": refund["id"]}), 200  # noqa: E501
        else:
            return jsonify({"status": "failure", "error": refund["status"]}), 400  # noqa: E501
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error during refund: {e}")
        return jsonify({"status": "failure", "error": str(e)}), 503
    except Exception as e:
        logger.error(f"Unexpected error during refund: {e}")
        return (
            jsonify({"status": "failure", "error": "An unexpected error occurred"}),  # noqa: E501
            500,
        )


@app.route("/payments", methods=["POST"])
def add_payment():
    """
    Endpoint to add a new payment entry to the database.
    """
    data = request.get_json()
    payment_id = data.get("payment_id")
    user_id = data.get("user_id")
    group_id = data.get("group_id")
    date = data.get("date")

    # Validate the incoming data
    if not all([payment_id, user_id, group_id, date]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Parse the date
        parsed_date = datetime.fromisoformat(date)

        # Create a new Payment entry
        payment = Payment(payment_id=payment_id, user_id=user_id, group_id=group_id, date=parsed_date)  # noqa: E501

        # Add the new payment to the session and commit
        db.session.add(payment)
        db.session.commit()

        return jsonify({"status": "success", "message": "Payment added successfully"}), 201  # noqa: E501

    except Exception as e:
        logger.error(f"Error adding payment: {e}")
        return jsonify({"status": "failure", "error": str(e)}), 500


@app.route("/payments/<string:payment_id>", methods=["DELETE"])
def delete_payment(payment_id):
    """
    Delete a payment record as part of the compensating
    transaction in the Saga pattern.
    """
    try:
        payment = Payment.query.filter_by(payment_id=payment_id).first()
        if not payment:
            return jsonify({"message": "Payment not found"}), 404

        db.session.delete(payment)
        db.session.commit()
        logger.info(
            f"Payment {payment_id} successfully deleted as part of rollback."
        )  # noqa: E501
        return jsonify({"message": "Payment deleted successfully"}), 200
    except Exception as e:
        logger.error(f"Error deleting payment {payment_id}: {e}")
        return jsonify({"message": "Failed to delete payment", "error": str(e)}), 500  # noqa: E501


# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
