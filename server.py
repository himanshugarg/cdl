from flask import Flask
import hmac
import hashlib
from flask import request, abort
import os

app = Flask(__name__)

@app.route('/webhook/payments', methods=['POST', 'GET'])
def webhook_payments():
    shared_secret = os.environ.get('RAZORPAY_SHARED_SECRET', '').encode()
    payload = request.get_data()
    received_signature = request.headers.get('X-Razorpay-Signature', '')

    computed_hmac = hmac.new(shared_secret, payload, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(computed_hmac, received_signature):
        abort(403, description="Invalid signature")
    try:
        data = json.loads(payload)
        event_type = data.get('event_type')
        event_id = data.get('event_id')
        payment_id = data.get('payment_id')
        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payment_events (
            event_id TEXT PRIMARY KEY,
            event_type TEXT,
            payment_id TEXT,
            received_at TEXT
            )
        ''')
        cursor.execute('''
            INSERT OR REPLACE INTO payment_events (event_id, event_type, payment_id, received_at)
            VALUES (?, ?, ?, ?)
        ''', (event_id, event_type, payment_id, datetime.utcnow().isoformat()))
        conn.commit()
        conn.close()
    except Exception:
        abort(400, description="Bad Request")
    return '<p>Hello, World!</p>'

@app.route('/payments/<payment_id>/events')
def payments_events(payment_id): 
    return f'<p>Hello {payment_id}</p>'
