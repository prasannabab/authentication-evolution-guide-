import jwt

payload = {
    "user": "Alice",
    "role": "admin"
}

token = jwt.encode(
    payload,
    "secret",
    algorithm="HS256"
)

print(token)


# deccode
decoded = jwt.decode(
    token,
    "secret",
    algorithms=["HS256"]
)

print(decoded)
