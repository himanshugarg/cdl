# API Documentation

## Overview

This service provides endpoints to receive and store Razorpay payment webhook events and to query stored payment events.

---

## Endpoints

### 1. POST `/webhook/payments`

**Description:**  
Receives a Razorpay payment webhook event, verifies its signature, and stores the event in the database.

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