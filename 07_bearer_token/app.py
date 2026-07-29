import jwt
from datetime import datetime, timedelta

# Configuration
SECRET_KEY = "your_super_secret_key"
ALGORITHM = "HS256"

# Create payload
payload = {
    "user_id": 123,
    "exp": datetime.utcnow() + timedelta(hours=1),
    "iat": datetime.utcnow()
}

# Generate token
bearer_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
print(f"JWT Bearer Token: {bearer_token}")   


# Sending token

token = "abcxyz123"

headers = {
    "Authorization": f"Bearer {token}"
}

print(headers)
