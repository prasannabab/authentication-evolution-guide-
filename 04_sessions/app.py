# 1: Create session storage.
import uuid

# Server-side session storage
sessions = {}

# Simulated database
users = {
    "alice": "password123"
}

# 2: Login function
def login(username, password):

    if users.get(username) == password:

        session_id = str(uuid.uuid4())

        sessions[session_id] = username

        return session_id

    return None
# 3: User logs in.
session = login("alice", "password123")
print(session)

# 4: get the user
def profile(session_id):

    username = sessions.get(session_id)

    if username:
        print(f"Welcome {username}")

    else:
        print("Unauthorized")

# 5: profile
profile(session)
