import base64
import hmac
from hashlib import sha256

encoding = 'utf-8'
header = '{"alg":"HS256","typ":"JWT"}'
payload = '{"sub":"rizzlyogawabear@gmail.com","iat":5516239024}'

encoded_header = base64.urlsafe_b64encode(bytes(str(header), encoding)).decode().replace("=", "")
encoded_payload = base64.urlsafe_b64encode(bytes(str(payload), encoding)).decode().replace("=", "")
# print(header)
# print(payload)



secret_key = 'your-256-bit-secret'
signature = hmac.new(bytes(secret_key, encoding), bytes(encoded_header + '.' + encoded_payload, encoding), digestmod=sha256).digest()
encoded_signature = base64.urlsafe_b64encode(bytes(signature)).decode().replace("=", "")
# print(encoded_signature)


token = encoded_header + '.' + encoded_payload + '.' + encoded_signature
print("\n\n\n\n", token)


correct = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyaXp6bHlvZ2F3YWJlYXJAZ21haWwuY29tIiwiaWF0Ijo1NTE2MjM5MDI0fQ.GHhMbNh_-p7gxQe14bUzEGObJ03LUkCk2LW9V6MfdHU"
if correct == token:
    print("\n\n\n\nyeayeayaeyaey")
else:
    print("\n\n\n\n nonfosnfoasnfoansodf")
    
    
    
    
    