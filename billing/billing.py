from flask import Flask, request, jsonify
from flask_cors import CORS
import stripe
import os
import sys

"""
Billing microservice accepts a POST request to /checkout with the following JSON payload:
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
    "user_id": "123"
}
"""

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize Stripe
stripe.api_key = os.environ.get('STRIPE_API_KEY')

# to receive the JSON payload
@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        # Create a new PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=data['total'],
            currency='usd',
            metadata={
                'order_id': data['order_id'],
                'show_name': data['show_name'],
                'show_datetime': data['show_datetime'],
                'user_id': data['user_id']
            }
        )
        return jsonify({'client_secret': intent.client_secret})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 403
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)