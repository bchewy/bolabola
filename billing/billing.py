from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
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
    return jsonify({'publicKey': STRIPE_PUBLISHABLE_KEY})

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
                                'name': request.json['show_name'],
                            },
                            'unit_amount': amount,
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url='http://localhost:3000/success',
                cancel_url='http://localhost:3000/cancel',
            )
        except Exception as e:
            return jsonify(error=str(e)), 403

    return jsonify({'sessionId': checkout_session['id']})

if __name__ == '__main__':
    app.run(port=5000, debug=True)