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
            {"category": "C", "quantity": 4},
            {"category": "Online", "quantity": 1}
        ],
        "user_id": "123"
    }
    """
    ticket_dict = {"A": 100, "B": 50, "C": 25, "Online": 10}
    if request.method == "POST":
        try:
            # line_items shows the details of the tickets on the receipt
            line_items = []
            for ticket in request.json["tickets"]:
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
            print(line_items[0])
            # create a new checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=line_items,
                mode="payment",
                success_url="http://localhost:5173/views/checkoutSuccess?session_id={CHECKOUT_SESSION_ID}",
                cancel_url="http://localhost:5173/views/checkoutCancel",
            )
        except Exception as e:
            return jsonify(error=str(e)), 403
    print(checkout_session.id)
    return jsonify({"code": 200, "checkout_session": checkout_session})


# Create a webhook endpoint for the checkout session
@app.route(
    "/webhook/stripe", methods=["POST"]
)  # if you change this endpoint, pls let yiji know so he can change in Stripe
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_SECRET_KEY)
    except ValueError as e:
        # Invalid payload
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return "Invalid signature", 400

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        payment_intent = event["data"]["object"]
        print("The payment intent is: ")
        print(payment_intent)
        print("Checkout Session completed!")
        # send payment confirmation to orchestrator
        ORCHESTRATOR_URL = "http://localhost:8000/api/v1/match-booking/match-booking"
        # Prepare payload to send back to orchestrator
        payload = {
            "payment_status": payment_intent["payment_status"],
            "charge_id": payment_intent["id"],
        }
        # Send POST request to orchestrator
        response = requests.post(ORCHESTRATOR_URL, json=payload)
        if response.ok:
            return (
                jsonify({"message": "Payment confirmed and orchestrator notified."}),
                200,
            )
        else:
            return jsonify({"error": "Failed to notify the orchestrator."}), 500

    return jsonify({"code": 200, "status": "success"}), 200


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
    Accepts a JSON payload about the tickets, as long as it has charge_id. Eg:
    {
        "charge_id": "ch_1NirD82eZvKYlo2CIvbtLWuY""
    }
    output: https://docs.stripe.com/api/refunds/object
    """
    try:
        if "charge_id" not in request.json:
            return jsonify({"error": "charge_id not found"}), 400
        charge_id = request.json["charge_id"]
        refund = stripe.Refund.create(
            charge=charge_id,
        )
        return jsonify(refund)
    except Exception as e:
        return jsonify(error=str(e)), 403


############################################################################################################
######################################    END OF PAYMENT REFUND    #########################################
############################################################################################################

if __name__ == "__main__":
    app.run(port=9003, debug=True, host="0.0.0.0")
