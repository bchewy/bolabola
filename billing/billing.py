from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import requests
from flask_cors import CORS
import stripe
import os
import sys
from dotenv import load_dotenv
load_dotenv()

"""
Billing microservice accepts a post request to /checkout with the following JSON payload:
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
}
"""

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

# Initialize Stripe
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
stripe.api_key = STRIPE_SECRET_KEY

# public key for the frontend
@app.route('/public-key', methods=['GET'])
def public_key():
    """
    Returns the public key for the frontend
    """
    return jsonify({'publicKey': STRIPE_PUBLISHABLE_KEY})

# create checkout session
@app.route('/checkout', methods = ['GET'])
def create_checkout_session():
    if request.method == "GET":
        try:
            amount = request.json['total']*100 # convert to cents
            # Create a new Checkout Session using the Stripe API
            # (https://stripe.com/docs/api/checkout/sessions/create)
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f"{request.json['show_name']} - {ticket_type}",
                        },
                        'unit_amount': ticket_price *  100,  # Convert to cents
                    },
                    'quantity': ticket_quantity,
                } for ticket_type, (ticket_price, ticket_quantity) in request.json['tickets'].items()
                ],
                mode='payment',
                success_url='http://localhost:3000/success',
                cancel_url='http://localhost:3000/cancel',
            )
        except Exception as e:
            return jsonify(error=str(e)), 403

    return jsonify({'sessionId': checkout_session['id']})

# create route for success
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

ORCHESTRATOR_URL = os.environ.get('ORCHESTRATOR_URL')

@app.route('/success', methods = ['POST'])
def success():
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

if __name__ == '__main__':
    app.run(port=8002, debug=True)