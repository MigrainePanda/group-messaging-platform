import json
from base64 import urlsafe_b64encode
import hmac
from hashlib import sha256


header = '{"alg":"HS256","typ":"JWT"}'

payload = '{"sub":"rizzlyogawabear@gmail.com","iat":5516239024}'

encoding = 'utf-8'
encoded_header = urlsafe_b64encode(bytes(str(header), encoding)).decode().replace("=", "")
encoded_payload = urlsafe_b64encode(bytes(str(header), encoding)).decode().replace("=", "")

signature_payload = f'{encoded_header}.{encoded_payload}'

secret_key = 'your-256-bit-secret'

signature = hmac.new(
    bytes(secret_key, encoding),
    msg = bytes(signature_payload, encoding),
    digestmod=sha256
).digest()

sigb64 = urlsafe_b64encode(bytes(signature)).decode().replace("=", "")

token = encoded_header + '.' + encoded_payload + '.' + sigb64
print("\n\n\n\n", token)


correct = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyaXp6bHlvZ2F3YWJlYXJAZ21haWwuY29tIiwiaWF0Ijo1NTE2MjM5MDI0fQ.GHhMbNh_-p7gxQe14bUzEGObJ03LUkCk2LW9V6MfdHU"
if correct == token:
    print("\n\n\n\nyeayeayaeyaey")
elif token == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyaXp6bHlvZ2F3YWJlYXJAZ21haWwuY29tIiwiaWF0Ijo1NTE2MjM5MDI0fQ.DYGnV6wzq3OyQfOC3zi24z8DY9YceBdHN2MP68kIuyQ":
    print("jawodjioawdjowia")
else:
    print("\n\n\n\n nonfosnfoasnfoansodf")

# encoded_signature = urlsafe_b64encode(str(signature).encode(encoding)).decode(encoding).rstrip('=')

# jwt_token = f'{signature_payload}.{encoded_signature}'

# print(jwt_token)

# resp = {
#     "token": jwt_token
# }


