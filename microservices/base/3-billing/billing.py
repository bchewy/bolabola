from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import requests
from flask_cors import CORS
import stripe
import os
import sys
# from dotenv import load_dotenv
# load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

# Initialize Stripe
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
stripe.api_key = STRIPE_SECRET_KEY

############################################################################################################
##################################    STRIPE PUBLIC KEY     ################################################
############################################################################################################
# public key for the frontend
@app.route('/api/v1/billing/public-key', methods=['GET'])
def public_key():
    """
    Returns the public key for the frontend
    """
    return jsonify({'publicKey': STRIPE_PUBLISHABLE_KEY})

############################################################################################################
#########################    END OF STRIPE PUBLIC KEY    ###################################################
############################################################################################################

############################################################################################################
#########################################    CHECKOUT SESSION     ##########################################
############################################################################################################
# create checkout session when the user clicks on the "Buy" button
# (https://stripe.com/docs/api/checkout/sessions/create)
@app.route('/api/v1/billing/checkout', methods = ['GET'])
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
    ticket_dict = {
        "A": 100,
        "B": 50,
        "C": 25,
        "Online": 10
    }
    if request.method == "GET":
        try:
            # line_items shows the details of the tickets on the receipt
            line_items = []
            for ticket in request.json['tickets']:
                line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f"{request.json['match_name']} - {ticket['category']}"
                        },
                        'unit_amount': ticket_dict[ticket['category']] * 100 # convert to cents
                    },
                    'quantity': ticket['quantity']
                })

            # create a new checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url='http://localhost:9003/success',
                cancel_url='http://localhost:9003/cancel',
            )
        except Exception as e:
            return jsonify(error=str(e)), 403

    return jsonify({'sessionId': checkout_session['id']})

# create route for successful checkout
ORCHESTRATOR_URL = os.environ.get('ORCHESTRATOR_URL')
@app.route('/api/v1/billing/checkout/success', methods = ['POST'])
def success():
    """
    on success, send POST back to orchestrator with the following JSON payload:
    {
        "order_id": "1234",
        "show_name": "Hamilton",
        "show_datetime": "2024-02-10T19:00:00",
        "tickets": [
            {"category": "A", "price": 400, "quantity": 2},
            {"category": "B", "price": 300, "quantity": 3},
            {"category": "C", "price": 200, "quantity": 4}
        ],
        "total": 2600,
        "user_id": "123",
        "payment_status": "success"
    }
    """
    # Extract session ID from request
    session_id = request.json['sessionId']
    # Retreive Checkout Session from Stripe
    checkout_session = stripe.checkout.Session.retrieve(session_id)
    # Prepare payload to send back to orchestrator
    payload = {
        "order_id": request.json['order_id'],
        "show_name": request.json['show_name'],
        "show_datetime": request.json['show_datetime'],
        "tickets": request.json['tickets'],
        "total": request.json['total'],
        "user_id": request.json['user_id'],
        "payment_status": checkout_session['payment_status']
    }
    # Send POST request to orchestrator
    response = requests.post(ORCHESTRATOR_URL, json=payload)
    if response.ok:
        return jsonify({"message": "Payment confirmed and orchestrator notified."}),  200
    else:
        return jsonify({"error": "Failed to notify the orchestrator."}),  500

############################################################################################################
#####################################    END OF CHECKOUT SESSION     #######################################
############################################################################################################

############################################################################################################
#########################################    PAYMENT REFUND     ############################################
############################################################################################################
# refund a user's payment
# https://docs.stripe.com/api/refunds/object
@app.route('/api/v1/billing/refund', methods = ['POST'])
def refund_payment():
    """
    This method refunds a user's payment.
    Accepts a JSON payload about the tickets, as long as it has charge_id. Eg:
    {
        "charge_id": "ch_1NirD82eZvKYlo2CIvbtLWuY""
    }
    """
    try:
        if 'charge_id' not in request.json:
            return jsonify({"error": "charge_id not found"}), 400
        charge_id = request.json['charge_id']
        refund = stripe.Refund.create(
            charge=charge_id,
        )
        return jsonify(refund)
    except Exception as e:
        return jsonify(error=str(e)), 403

############################################################################################################
######################################    END OF PAYMENT REFUND    #########################################
############################################################################################################
    
if __name__ == '__main__':
    app.run(port=9003, debug=True)