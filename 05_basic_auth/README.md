# Chapter 5 – Basic Authentication
### Why did it evolve?
When REST APIs became popular, browsers weren't the only clients anymore.

Now there were:
```
Mobile Apps
Desktop Applications
Scripts
Third-party Integrations
```
Cookies weren't always convenient.

A standardized authentication method was needed.

### How it works

The client sends:
```
Authorization: Basic YWxpY2U6cGFzc3dvcmQxMjM=
```
That Base64 value is simply:
```
alice:password123
```
Python Example
```
import requests

response = requests.get(
    "https://httpbin.org/basic-auth/user/pass",
    auth=("user", "pass")
)

print(response.status_code)
```
The requests library automatically creates the Authorization header.

### Security Problems
Base64 is NOT encryption

Anyone can decode it.
```
import base64

encoded = "YWxpY2U6cGFzc3dvcmQxMjM="

decoded = base64.b64decode(encoded)

print(decoded.decode())
```
Output:
```
alice:password123
```
Password sent every request
```
GET /profile

Authorization:
Basic xxxxxxxxx
```
Every API request carries the password.

If credentials leak, the attacker owns the account.

#### Solution

Always use HTTPS.

Even then, sending the password repeatedly isn't ideal.

Developers wanted something that could be revoked without changing the user's password.

That led to API Keys and later Bearer Tokens.
<br>
<br>
<br>

> Above info is basic details. below has clear details.

This is actually one of the biggest misconceptions in authentication.

Many people think the evolution was:
```
Sessions
    ↓
Basic Authentication
```
But that's not because Basic Authentication is more secure. In fact, sessions are generally more secure for browser-based applications.

Basic Authentication evolved to solve a different problem.

Let's walk through the history.

#### Before the Internet

Initially, applications were desktop applications.
```
User

↓

Login

↓

Application

↓

Database
```
Simple username and password.

#### Websites Appeared

When websites became popular, HTTP introduced a problem.

HTTP is stateless.

Every request is independent.

Example:
```
GET /products
```
The server doesn't know who you are.

Next request:
```
GET /orders
```
Again, it doesn't know.

#### Solution: Sessions

Servers started creating sessions.
```
Password

↓

Verified Once

↓

Session Created

↓

Cookie

↓

Future Requests
```
This worked extremely well.

For browser applications, it is still one of the best solutions today.

#### Then APIs Became Popular

Around the late 1990s and early 2000s, something changed.

Not every client was a browser anymore.

Clients included:
```
Browser

Mobile App

Desktop App

Java Program

Python Script

Cron Job

IoT Device

Server A calling Server B
```
Now ask yourself:

<b>Can all of these automatically manage browser cookies?</b>

> No.

Only browsers naturally handle cookies.

A Python script doesn't.

A Java service doesn't.

A Linux cron job doesn't.

So sessions became inconvenient for many non-browser clients.

Example

Suppose you are writing a Python script.
```
import requests

requests.get("https://company.com/profile")
```
How will this script know about
```
SESSIONID
```
cookies?

It has to manually:
```
Log in
Capture the cookie
Store it
Send it on every request
Refresh it if needed
```
That's a lot of work.

#### Industry Needed a Standard

Instead of every server inventing its own authentication mechanism,

HTTP introduced a standard header.
```
Authorization:
```
Now every client could send credentials in the same way.

#### Basic Authentication

Instead of
```
Cookie:
SESSIONID=abcd
```
the client sends
```
Authorization:
Basic YWxpY2U6cGFzc3dvcmQ=
```
Every HTTP library understands this.

Python
```
requests.get(url, auth=("alice", "password"))
```
Java
```
Authenticator
```
curl
```
curl -u alice:password
```
Browsers

Built-in support.

This interoperability was the main benefit.

#### What Problem Did Basic Authentication Solve?
##### Problem 1 — No Browser Required

Sessions assume a browser that automatically stores cookies.

Basic Authentication works anywhere.

Examples:
```
Python

Java

Go

Node.js

Bash

curl

PowerShell
```
##### Problem 2 — HTTP Standard

Before Basic Authentication,

every application invented its own login header.

Example

Company A
```
Username:
```
Company B
```
User:
```
Company C
```
Login:
```
No consistency.

Basic Authentication standardized it.
```
Authorization:
Basic ...
```
Every HTTP client understands it.

##### Problem 3 — Easy Automation

Imagine a backup script.
```
Every Night

↓

Download Reports

↓

Store Backup
```
No browser.

No cookies.

Basic Authentication is simple for automation.

<b>Did It Solve Session Security Problems?</b>

No.

This is the important point.

Basic Authentication did not fix the weaknesses of sessions.

> It solved the problem of client compatibility and standardization.

#### In Fact, It Introduced New Problems

Every request contains

Username

Password

again and again.

Even though Base64 is used,

Base64 is not encryption.

So HTTPS is still mandatory.

#### Comparison
##### Session
```
Password

↓

One Login

↓

Session ID

↓

Future Requests
```
Password travels once.

##### Basic Authentication
```
Password

↓

Every Request

↓

Every Request

↓

Every Request
```
Password always travels.

#### So Why Was It Accepted?

Because the internet was changing.

Not everything was a browser anymore.

Imagine these clients:
```
Python Script

↓

Weather API
```
or
```
Server A

↓

Server B
```
Sessions don't fit naturally here because there's no browser managing cookies.

Basic Authentication was simple and standardized.

#### Then Another Problem Appeared

Suppose you're calling an API <b>10,000 times per day.</b>

Every request still contains:
```
Username

Password
```
Questions arise:
- What if the password leaks?
- What if the user changes their password?
- How can you give temporary access?
- How can you give read-only access?
- How can you revoke access without changing the password?

Basic Authentication has no good answers.

#### The Next Evolution: API Keys

Instead of sending the real password,

the server issues an API key.
```
Username + Password

↓

Authenticate Once

↓

Issue API Key

↓

Use API Key
```
Now:
- The user's real password stays protected.
- The API key can be rotated or revoked.
- Different applications can have different keys.
- Permissions can be managed independently.

### Evolution So Far
```
Username & Password
        │
        ▼
Sessions
        │
        │ Solved:
        │ - HTTP is stateless
        │ - Browser remembers users
        │
        ▼
Basic Authentication
        │
        │ Solved:
        │ - Standardized HTTP authentication
        │ - Worked for browsers, scripts, services, and tools
        │ - No dependency on cookie handling
        │
        ▼
API Keys
        │
        │ Solved:
        │ - Avoid sending user passwords
        │ - Better for application-to-application authentication
        │ - Easier key rotation and revocation
        ▼
Bearer Tokens
```
One small correction to the overall timeline

For historical accuracy, it's worth noting that <b>HTTP Basic Authentication and cookies/sessions developed around the same era rather than one replacing the other</b>. They addressed different needs:

<b>Sessions + Cookies</b> → Best for browser users logging into websites. <br>
<b>Basic Authentication</b> → A standardized way for any HTTP client (browsers, scripts, services) to send credentials. <br>
<b>API Keys</b> → Better for identifying applications instead of users. <br>
<b>Bearer Tokens/JWT</b> → Better for modern APIs, mobile apps, and distributed systems. <br>

This distinction is important because it helps to understand that authentication methods didn't always evolve by replacing one another—many coexisted because they solved different problems.
