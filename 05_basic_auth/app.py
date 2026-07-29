import requests

response = requests.get(
    "https://httpbin.org/basic-auth/user/pass",
    auth=("user", "pass")
)

print(response.status_code)


import base64

encoded = "YWxpY2U6cGFzc3dvcmQxMjM="

decoded = base64.b64decode(encoded)

print(decoded.decode())
