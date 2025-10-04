# API Documentation

## Overview

Endpoints to POST and GET Razorpay payment webhook events.

---

## Endpoints

### POST `/webhook/payments`

**Description:**  
POST's a Razorpay payment webhook event

**Headers:**
- `Content-Type: application/json`
- `X-Razorpay-Signature: <computed HMAC SHA256 signature>`

**Request Body:**  
A JSON object representing a Razorpay payment event, e.g.:
```json
{
  "event": "payment.authorized",
  "payload": {
    "payment": {
      "entity": {
        "id": "pay_001",
        "status": "authorized",
        "amount": 1000,
        "currency": "INR"
      }
    }
  },
  "created_at": 1751885965,
  "id": "evt_auth_001"
}
```

**Responses**:

* 200 OK
* 400 Bad Request – Invalid JSON or missing required fields.
* 403 Forbidden – Invalid signature.
* 500 Internal Server Error – Database error.

### GET /payments/<payment_id>/events

**Description**:

GET's a list of events for the given payment ID.

**Path Parameters**:

`payment_id` (string): The payment ID to query.

**Response**:

* 200 OK

```json
[
  {
    "event_type": "payment.authorized",
    "received_at": "2025-10-04T12:34:56.789123"
  },
  ...
]