from flask import Flask

app = Flask(__name__)

@app.route('/webhook/payments', methods=['POST', 'GET'])
def webhook_payments():
    return '<p>Hello, World!</p>'

@app.route('/payments/<payment_id>/events')
def payments_events(payment_id): 
    return f'<p>Hello {payment_id}</p>'
