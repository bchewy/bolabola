from flask import Flask
import pika

app = Flask(__name__)

@app.route('/api/v1/refund', methods=['POST'])
def refund():
    """
    1. receives ticket information from frontend
    2. calls billing service for refund
    3. receives a status from billing service, success/failure
    4. if success, send ticket information to RabbitMQ to update db
    """

if __name__ == '__main__':
    app.run(port=9103)
