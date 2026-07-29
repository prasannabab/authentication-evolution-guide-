import requests

headers = {
    "X-API-Key": "my-secret-api-key"
}

response = requests.get(
    "https://api.example.com/users",
    headers=headers
)

print(response.status_code)
