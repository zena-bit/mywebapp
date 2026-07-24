import requests
from django.conf import settings

def get_access_token():
    consumer_key = getattr(settings, 'MPESA_CONSUMER_KEY', '')
    consumer_secret = getattr(settings, 'MPESA_CONSUMER_SECRET', '')
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
    try:
        response = requests.get(url, auth=(consumer_key, consumer_secret), timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('access_token'), data.get('expires_in')
    except Exception as e:
        pass
    return None, None


import base64
from datetime import datetime

def initiate_stk_push(phone, amount, order_reference="Order123"):
    access_token, _ = get_access_token()
    if not access_token:
        return {"error": "Failed to get access token"}, 500

    shortcode = getattr(settings, 'MPESA_SHORTCODE', '174379')
    passkey = getattr(settings, 'MPESA_PASSKEY', 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919')
    callback_url = getattr(settings, 'MPESA_CALLBACK_URL', 'https://your-domain.com/mpesa/callback/')
    
    # Format phone to: 2547XXXXXXXX or 2541XXXXXXXX
    phone = str(phone).strip().replace('+', '')
    if phone.startswith('0'):
        phone = '254' + phone[1:]
    
    # Current timestamp: YYYYMMDDHHMMSS
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    
    # Generate password
    data_to_encode = f"{shortcode}{passkey}{timestamp}"
    password = base64.b64encode(data_to_encode.encode('utf-8')).decode('utf-8')
    
    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    stk_push_payload = {
        'BusinessShortCode': int(shortcode),
        'Password': password,
        'Timestamp': timestamp,
        'TransactionType': 'CustomerPayBillOnline',
        'Amount': int(float(amount)),  # Integer
        'PartyA': int(phone),   # Customer phone number
        'PartyB': int(shortcode),
        'PhoneNumber': int(phone),
        'CallBackURL': callback_url,
        'AccountReference': order_reference,
        'TransactionDesc': 'Payment for goods'
    }
    
    try:
        response = requests.post(url, json=stk_push_payload, headers=headers, timeout=15)
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500
