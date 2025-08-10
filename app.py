"""Minimal Flask app for banking intent classification demo"""
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Core banking intents for demo
INTENTS = [
    {"id": "balance_inquiry", "name": "Balance Inquiry"},
    {"id": "transfer_money", "name": "Transfer Money"},
    {"id": "payment_bill", "name": "Bill Payment"},
    {"id": "card_issue", "name": "Card Issues"},
    {"id": "fraud_report", "name": "Fraud Report"},
]

@app.route('/')
def home():
    return jsonify({
        "service": "Matchelor Banking Intent Classifier",
        "status": "active",
        "version": "1.0.0-demo"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/intents')
def get_intents():
    return jsonify({"intents": INTENTS})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)