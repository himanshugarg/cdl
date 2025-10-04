## Getting Started

1. **Clone the repository:**
    ```
    git clone https://github.com/himanshugarg/cdl.git
    cd cdl
    ```

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
    - Configure the environment variable RAZORPAY_SHARED_SECRET

4. **Run the application:**
    ```
    flask --app server run
    ```

5. **Compute payload signature:**
    ```bash
    $ python hash.py mock_payloads/payment_captured_1.json 
    <signature>
    ```

6. **Invoke the API:**

   ```bash
   curl -X POST http://localhost:5000/webhook/payments -H "Content-Type: application/json" -H "X-Razorpay-Signature: <signature>" --data-binary @mock_payloads/payment_authorized_1.json
   
   {"status":"success"}
   ```
   
   ```bash
   curl -X POST http://localhost:5000/webhook/payments -H "Content-Type: application/json" -H "X-Razorpay-Signature: <signature>" --data-binary @mock_payloads/payment_captured_1.json 
   
   {"status":"success"}
   ```

   ```
   curl http://localhost:5000/payments/<paymend_id>/events
   ```

7. ** Query the SQLite DB **

    ```
    sqlite> select * from payment_events 
    ...> ;

| event_id|event_type|payment_id|received_at
| --- | --- | --- | --- |
|evt_auth_002|payment.authorized|pay_002|2025-10-04T02:01:35.008650
|evt_auth_003|payment.authorized|pay_003|2025-10-04T02:01:35.064702
...
evt_cap_014|payment.captured|pay_014|2025-10-04T09:30:53.026691
