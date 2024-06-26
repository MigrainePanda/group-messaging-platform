import base64
import hmac
from hashlib import sha256

encoding = 'utf-8'
header = '{"alg":"HS256","typ":"JWT"}'
payload = '{"sub":"rizzlyogawabear@gmail.com","iat":5516239024}'

encoded_header = base64.urlsafe_b64encode(bytes(header, encoding)).decode().replace("=", "")
encoded_payload = base64.urlsafe_b64encode(bytes(payload, encoding)).decode().replace("=", "")
# print(header)
# print(payload)



secret_key = 'your-secret-key-is-not-cool'
encoded_secret_key = base64.urlsafe_b64encode(bytes(secret_key, encoding)).decode().replace("=", "")


signature = hmac.new(bytes(encoded_secret_key, encoding), bytes(encoded_header + '.' + encoded_payload, encoding), digestmod=sha256).digest()
encoded_signature = base64.urlsafe_b64encode(signature).decode().replace("=", "")





token = encoded_header + '.' + encoded_payload + '.' + encoded_signature
print("\n\n\n\n", token)


# token = ""
correct = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyaXp6bHlvZ2F3YWJlYXJAZ21haWwuY29tIiwiaWF0Ijo1NTE2MjM5MDI0fQ.RcnAucyLX5WW-Grc_89-9BS8ZDbRBDzbAR6mE_YYwgw"
if correct == token:
    print("\n\n\n\nyeayeayaeyaey")
else:
    print("\n\n\n\n nonfosnfoasnfoansodf")
    
    
    
    
    
# token =   "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyaXp6bHlvZ2F3YWJlYXJAZ21haWwuY29tIiwiaWF0Ijo1NTE2MjM5MDI0fQ.uTKGTYSfKOXOSylN9lRo9NOw13DxaZkUSLEzatyNRfM"
# correct = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyaXp6bHlvZ2F3YWJlYXJAZ21haWwuY29tIiwiaWF0Ijo1NTE2MjM5MDI0fQ.uTKGTYSfKOXOSylN9lRo9NOw13DxaZkUSLEzatyNRfM"

secret_key = 'your-secret-key'
signature = hmac.new(bytes(secret_key, encoding), bytes(encoded_header + '.' + encoded_payload, encoding), digestmod=sha256).digest()
encoded_signature = base64.urlsafe_b64encode(signature).decode().replace("=", "")
    