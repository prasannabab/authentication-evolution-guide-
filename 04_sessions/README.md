## The Problem

In the previous chapter, HTTPS encrypted communication.

So now our password is safe while traveling over the internet.

But there is still a problem.

Imagine you open Amazon.
```
1. Login
2. View Products
3. Add to Cart
4. View Orders
5. Logout
```
If every request required your username and password:
```
GET /products
username=alice
password=Password123

GET /carts
username=alice
password=Password123

GET /orders
username=alice
password=Password123
```
Imagine doing the above steps for 500 times while browsing.
Problems:
- Password sent repeatedly
- More chances to leak
- Bad performance

## The Question
Once the server verifies my password...

### Why should it ask again?
Exactly.
The server already knows who you are.
It only needs a way to remember you.
That is the birth of Sessions.

Simple diagram
```
Username
Password
       │
       ▼
Server verifies
       │
       ▼
Create Session
       │
       ▼
Generate Session ID
```
Example
```
Session ID
a7f84c9b12ef4567
```

The server stores
```
Session Table

+----------------------+--------+
| Session ID           | User   |
+----------------------+--------+
| a7f84c9b12ef4567     | Alice  |
+----------------------+--------+
```
The browser only receives
```
a7f84c9b12ef4567
```
The browser <b>does not receive Alice's information</b>.

It only receives a random identifier.

## Step-by-Step Flow
### Step 1
Alice logs in.
```
POST /login

{
    "username":"alice",
    "password":"Password123"
}
```
### Step 2
Server validates credentials.
```
Database

Alice
Password Hash
```
Password matches.

### Step 3
Server creates a session.
```
Random Session ID

9f3d81a4c5e8
```
Stores
```
Memory

9f3d81a4c5e8
        │
        ▼
Alice
```
