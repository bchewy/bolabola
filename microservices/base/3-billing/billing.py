from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    jsonify,
)
import requests
from flask_cors import CORS
import stripe
import os
import sys
import json

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
# app.secret_key = "ee89f7f418d66bdfbb7fb59b07025ec2"

# Initialize Stripe
STRIPE_SECRET_KEY = "sk_test_51Oh9s0F4chEmCmGgIJNiU5gOrEeqWv3IX8F0drbkTvI8STRNH060El8kYr1wUnA6JhLjq2HmNx8KtYSzqZFsATAY00EjgRxXmE"
STRIPE_PUBLISHABLE_KEY = "pk_test_51Oh9s0F4chEmCmGg0Cbvmc8wbE3puY2dnkr8Gz7H1i0uVy8rAvhpIGVlO5DDBengMt5rVYRycjGU0t6wKTeoJjvg008zdJD9Vz"
stripe.api_key = "sk_test_51Oh9s0F4chEmCmGgIJNiU5gOrEeqWv3IX8F0drbkTvI8STRNH060El8kYr1wUnA6JhLjq2HmNx8KtYSzqZFsATAY00EjgRxXmE"


@app.route("/ping", methods=["GET"])
def ping():
    print("pinged")
    return jsonify({"message": "Pong!"})


############################################################################################################
##################################    STRIPE PUBLIC KEY     ################################################
############################################################################################################
# public key for the frontend
@app.route("/public-key", methods=["GET"])
def public_key():
    """
    Returns the public key for the frontend
    """
    return jsonify({"code": 200, "publicKey": STRIPE_PUBLISHABLE_KEY})


############################################################################################################
#########################    END OF STRIPE PUBLIC KEY    ###################################################
############################################################################################################


############################################################################################################
#########################################    CHECKOUT SESSION     ##########################################
############################################################################################################
# create checkout session when the user clicks on the "Buy" button
# (https://stripe.com/docs/api/checkout/sessions/create)
@app.route("/checkout", methods=["POST"])
def create_checkout_session():
    """
    This method creates a new checkout session.
    Accepts the following JSON payload:
    {
        "match_id": "1234",
        "match_name": "Arsenal vs Chelsea",
        "tickets": [
            {"category": "A", "quantity": 2},
            {"category": "B", "quantity": 3},
            {"category": "C", "quantity": 4}
        ],
        "user_id": "123",
        "serial_no": "1"
    }
    """
    ticket_dict = {"A": 100, "B": 50, "C": 25}
    if request.method == "POST":
        try:
            print("Billing service received the following payload: ", request.json)
            # these variables store the quantity of each ticket category for metadata use
            A, B, C = 0, 0, 0

            # line_items shows the details of the tickets on the receipt
            line_items = []

            for ticket in request.json["tickets"]:
                # fill in metadata for Stripe
                if ticket["category"] == "A":
                    A = ticket["quantity"]
                elif ticket["category"] == "B":
                    B = ticket["quantity"]
                elif ticket["category"] == "C":
                    C = ticket["quantity"]
                # fill in line_items for Stripe
                line_items.append(
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": f"{request.json['match_name']} - {ticket['category']}"
                            },
                            "unit_amount": ticket_dict[ticket["category"]]
                            * 100,  # convert to cents
                        },
                        "quantity": ticket["quantity"],
                    }
                )

            # create a new checkout session
            metadata = {
                "match_id": request.json["match_id"],
                "user_id": request.json["user_id"],
                "A": A,
                "B": B,
                "C": C,
                "serial_no": "1", # to get dynamically
            }
            print("Doing stripe checkout now")
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=line_items,
                mode="payment",
                success_url="http://localhost:5173/views/checkoutSuccess?session_id={CHECKOUT_SESSION_ID}",
                cancel_url="http://localhost:5173/views/checkoutCancel",
                metadata=metadata,  # pass the metadata to the webhook
            )
            # send over the link to match-booking orchestrator
        except Exception as e:
            print("Error: ", str(e))
            return jsonify(error=str(e)), 403
    return jsonify({"code": 200, "checkout_session": checkout_session})


# Stripe calls this webhook
@app.route(
    "/webhook/stripe", methods=["POST"]
)  # if you change this endpoint, pls let yiji know so he can change in Stripe
def stripe_webhook():
    endpoint_secret = (
        "whsec_d0d59a6c1c4e0d297659d18b66aa3785034db493bb5092a993fd29df21bb18df"
    )
    event = None
    payload = request.data
    sig_header = request.headers["Stripe-Signature"]
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return "Invalid signature", 400

    # send payment information to orchestrator
    ORCHESTRATOR_URL = "http://kong:8000/api/v1/booking/process-webhook"

    session = event["data"]["object"]
    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        # Prepare payload to send back to orchestrator
        payload = {
            "status": "complete",
            "payment_intent": session["payment_intent"],
            "metadata": session["metadata"],
        }

    elif event["type"] == "checkout.session.expired":
        payload = {
            "status": "expired",
            "payment_intent": session["payment_intent"],
            "metadata": session["metadata"],
        }
    elif event["type"] == "checkout.session.cancelled":
        payload = {
            "status": "cancelled",
            "payment_intent": session["payment_intent"],
            "metadata": session["metadata"],
        }
    else:
        # Unexpected event type
        return "Unexpected event type", 400

    # Send POST request to orchestrator
    print("Tried sending to this link: ", ORCHESTRATOR_URL)
    response = requests.post(ORCHESTRATOR_URL, json=payload)
    print("The response from orchestrator is: ", response)

    if response.ok:
        return (
            jsonify({"stats": "Payment confirmed and orchestrator notified."}),
            200,
        )
    else:
        print("Cannot notify orchestrator")
        return jsonify({"error": "Failed to notify the orchestrator."}), 500


############################################################################################################
#####################################    END OF CHECKOUT SESSION     #######################################
############################################################################################################


############################################################################################################
#########################################    PAYMENT REFUND     ############################################
############################################################################################################
# refund a user's payment
@app.route("/refund", methods=["POST"])
def refund_payment():
    """
    This method refunds a user's payment.
    When the refund orchestrator calls initiate-refund, this method is called.
    When this method is called, it will call stripe to refund the payment.
    This method accepts a JSON payload about the tickets, as long as it has a payment_intent. Eg:
    {
        "payment_intent": "pi_1NirD82eZvKYlo2CIvbtLWuY"
    }
    output: https://docs.stripe.com/api/refunds/object
    "pi_3OvgQTF4chEmCmGg1A9ZYrVI"
    The output will be returned to the orchestrator.
    """
    try:
        # receive refund information from orchestrator
        payload = request.json

        if "payment_intent" not in payload:
            return jsonify({"error": "payment_intent not found"}), 400

        metadata = {
            "user_id": payload["user_id"],
            "match_id": payload["match_id"],
            "category": payload["category"],
            "quantity": payload["quantity"],
            "payment_intent": payload["payment_intent"],
        }

        # call stripe to refund the payment
        refund = stripe.Refund.create(
            payment_intent=payload["payment_intent"],
            metadata=metadata,
        )

        # prepare refund information to send to orchestrator
        refund_info = {
            "status": refund.status,
            "payment_intent": refund.payment_intent,
            "metadata": refund.metadata,
        }

        # return refund information to orchestrator
        return jsonify({"message": "Refund successful", "data": refund_info}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


############################################################################################################
######################################    END OF PAYMENT REFUND    #########################################
############################################################################################################

if __name__ == "__main__":
    app.run(port=9003, debug=True, host="0.0.0.0")
