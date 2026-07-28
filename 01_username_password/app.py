users = {
    "alice": "password123"
}

username = input("Username: ")
password = input("Password: ")

if users.get(username) == password:
    print("Login Successful")
else:
    print("Invalid Credentials")
