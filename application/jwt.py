import hmac, json
from base64 import urlsafe_b64encode, urlsafe_b64decode
from hashlib import sha256

from datetime import datetime, timezone

from dotenv import load_dotenv
import os

load_dotenv()

def generate_jwt(user: dict) -> str:
    ENCODING = 'utf-8'
    SECRET_KEY = os.getenv('SECRET_KEY')
    iat_time = datetime.now(timezone.utc).timestamp()
    exp_time = iat_time + 6048000
    
    header = '{"alg":"HS256","typ":"JWT"}'
    payload = "{" + f'"id":"{user["id"]}","iat":{iat_time}, "exp": {exp_time}' + "}"
    
    encoded_header = urlsafe_b64encode(bytes(header, ENCODING)).decode().replace("=", "")
    encoded_payload = urlsafe_b64encode(bytes(payload, ENCODING)).decode().replace("=", "")

    signature = hmac.new(bytes(SECRET_KEY, ENCODING), bytes(encoded_header + '.' + encoded_payload, ENCODING), digestmod=sha256).digest()
    encoded_signature = urlsafe_b64encode(signature).decode().replace("=", "")
    
    return encoded_header + '.' + encoded_payload + '.' + encoded_signature

def is_valid_jwt(jwt: str) -> bool:
    if not jwt:
        return False

    ENCODING = 'utf-8'
    jwt = jwt.split(".")
    # check for correct length
    if len(jwt) != 3: 
        print("invalid jwt format")
        return False
    # retrieve header and payload information
    header = urlsafe_b64decode(jwt[0] + "==").decode(ENCODING)
    payload = urlsafe_b64decode(jwt[1] + "==").decode(ENCODING)
    # check for valid json strings
    try:
        header_json = json.loads(header)
        payload_json = json.loads(payload)
    except:
        print("bad header or payload")
        return False
    # check for correct header structure
    accepted_keys = ['alg', 'typ']
    accepted_values = ['HS256', 'JWT']
    for key, value in header_json.items():
        if key not in accepted_keys or value not in accepted_values:
            print("header bad parameter or value")
            return False
    # check that secret key hashing matches
    SECRET_KEY = os.getenv('SECRET_KEY')
    check_signature = hmac.new(bytes(SECRET_KEY, ENCODING), bytes(jwt[0] + '.' + jwt[1], ENCODING), digestmod=sha256).digest()
    arg_signature = urlsafe_b64decode(jwt[2] + "==")
    if not hmac.compare_digest(check_signature, arg_signature):
        print("invalid signature")
        return False
    # return true if all cases above pass
    return True
