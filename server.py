from flask import Flask, request, abort, jsonify
import hmac
import hashlib
import os
import sqlite3
import json
from datetime import datetime
import logging

app = Flask(__name__)
DB_PATH = 'events.db'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

def verify_signature(payload, received_signature, secret):
    computed_hmac = hmac.new(secret, payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed_hmac, received_signature)

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS payment_events (
                event_id TEXT PRIMARY KEY,
                event_type TEXT,
                payment_id TEXT,
                received_at TEXT
            )
        ''')

def insert_event(event_id, event_type, payment_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            INSERT OR REPLACE INTO payment_events (event_id, event_type, payment_id, received_at)
            VALUES (?, ?, ?, ?)
        ''', (event_id, event_type, payment_id, datetime.utcnow().isoformat()))

@app.route('/webhook/payments', methods=['POST'])
def webhook_payments():
    shared_secret = os.environ.get('RAZORPAY_SHARED_SECRET', '').encode()
    payload = request.get_data()
    received_signature = request.headers.get('X-Razorpay-Signature', '')

    if not verify_signature(payload, received_signature, shared_secret):
        logging.warning("Invalid signature for payload: %s", payload)
        abort(403, description="Invalid signature")

    try:
        data = json.loads(payload)
        event_type = data.get('event')
        event_id = data.get('id')
        payment_id = (
            data.get('payload', {})
                .get('payment', {})
                .get('entity', {})
                .get('id')
        )
        if not (event_type and event_id and payment_id):
            logging.error("Missing event data: %s", data)
            abort(400, description="Missing event data")
        insert_event(event_id, event_type, payment_id)
    except json.JSONDecodeError as e:
        logging.error("JSON decode error: %s", e)
        abort(400, description="Invalid JSON")
    except sqlite3.DatabaseError as e:
        logging.error("Database error: %s", e)
        abort(500, description="Database error")
    except Exception as e:
        logging.exception("Unexpected error")
        abort(400, description=f"Bad Request: {e}")

    return jsonify({"status": "success"})

@app.route('/payments/<payment_id>/events')
def payments_events(payment_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute('''
            SELECT event_type, received_at FROM payment_events
            WHERE payment_id = ?
            ORDER BY received_at
        ''', (payment_id,))
        events = [{'event_type': row[0], 'received_at': row[1]} for row in cursor.fetchall()]
    return jsonify(events)

init_db()

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(debug=debug_mode)


# TODO: Address the following limitations for production use:s
# Secret Management

# The shared secret defaults to an empty string if not set. The app should fail to start if the secret is missing.
# Secrets should not be stored in environment variables in some deployment scenarios; use a secrets manager if possible.
# Database Choice and Migration

# SQLite is not suitable for concurrent writes or high-traffic production workloads. Use a production-grade database (PostgreSQL, MySQL).
# No schema migration support (e.g., Alembic for SQLAlchemy).
# Input Validation

# No strict schema validation for incoming JSON. Use a library like Marshmallow or Pydantic to validate and sanitize input.
# Error Handling

# Error messages may leak sensitive information to clients.
# Logging may expose sensitive data (e.g., raw payloads).
# Security

# No rate limiting or abuse protection (e.g., Flask-Limiter).
# No authentication or authorization for sensitive endpoints.
# No CORS or security headers (e.g., HSTS, Content Security Policy).
# No enforcement of HTTPS.
# Concurrency and Thread Safety

# Flask’s built-in server and SQLite are not thread-safe for production. Use a WSGI server (Gunicorn, uWSGI) and a production database.
# Resource Management

# No connection pooling for the database.
# No graceful shutdown or health checks.
# Testing and Monitoring

# No automated tests or test coverage.
# No monitoring, alerting, or logging aggregation.
# Deployment

# No Dockerfile or deployment scripts.
# No configuration for environment-specific settings.
# Documentation

# No API documentation (Swagger/OpenAPI).
# No README or usage instructions.
