import sys, hmac, hashlib
import os

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <filename>")
    sys.exit(1)

secret = os.environ["RAZORPAY_SHARED_SECRET"].encode()
filename = sys.argv[1]

with open(filename, "rb") as f:
    payload = f.read()

computed_hmac = hmac.new(secret, payload, hashlib.sha256).hexdigest()
print(computed_hmac)
