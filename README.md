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

5. **Invoke the API:**

   ```bash
   curl -X POST http://localhost:5000/webhook/payments -H "Content-Type: application/json" -H "X-Razorpay-Signature: <signature>" --data-binary @mock_payloads/payment_authorized_1.json
   
   {"status":"success"}
   ```
   
   ```bash
   curl -X POST http://localhost:5000/webhook/payments -H "Content-Type: application/json" -H "X-Razorpay-Signature: <signature>" --data-binary @mock_payloads/payment_captured_1.json 
   
   {"status":"success"}
   ```

* curl http://localhost:5000/payments/<paymend_id>/events