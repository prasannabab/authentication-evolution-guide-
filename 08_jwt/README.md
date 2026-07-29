This is where everything starts coming together.

By Chapter 8, your readers should already know:

1: Username & Password → Identify the user.
2: Password Hashing → Protect stored passwords.
3: HTTPS → Protect data in transit.
4: Sessions → Remember browser users.
5: Basic Authentication → Standard HTTP authentication.
6: API Keys → Identify applications.
7: Bearer Tokens → Authenticate users for APIs without relying on cookies.

Now they'll naturally ask:

 <b>If Bearer Tokens already work, why was JWT invented?</b>

This is the perfect transition.

# Chapter 8 – JWT (JSON Web Token)
The Big Question

In Chapter 7, we learned that clients send:
```
Authorization: Bearer abc123xyz
```
The server receives:
```
abc123xyz
```
Question:

What is <b>abc123xyz</b>?

The answer could be anything.

It might be:
```
12345
```
or
```
random-secret-string
```
The HTTP specification only says:
```
Authorization: Bearer <token>
```
It <b>does not define the token format.</b>

## What Happened Before JWT?

Suppose we build our own Bearer Token system.

Alice logs in.

Server creates
```
token = xyz123
```
Server stores
```
Token Store

xyz123
      ↓
Alice
```
Client sends
```
Authorization: Bearer xyz123
```
Server receives it.

Now the server asks:
```
Who owns xyz123?
```
It checks the database.
```
Token Store

xyz123

↓

Alice
```
Works perfectly.

### But a New Problem Appeared

Imagine Google.

Millions of users.

Every request requires:
```
Database Lookup

↓

Find Token

↓

Find User
```
Every request.

Millions per second.

### Microservices Make It Worse

Imagine Netflix.
```
Client

↓

API Gateway

↓

User Service

↓

Order Service

↓

Payment Service

↓

Recommendation Service
```
Every service receives
```
Authorization: Bearer xyz123
```
Each service must ask
```
Database

↓

Who owns xyz123?
```
Thousands of database lookups.

Every second.

#### Engineers Asked

Can the token carry the user information itself?

Instead of
```
xyz123

↓

Database

↓

Alice
```
What if
```
Token

↓

Already Contains

↓

Alice
```
That idea became <b>JWT</b>.

What Is JWT?

JWT stands for:
```
<b>JSON Web Token</b>
``
Instead of a random string
```
xyz123
```
The token contains information.

Example payload:
```
{
  "user": "Alice",
  "role": "admin",
  "exp": 1750000000
}
```
The server no longer needs to ask
```
Who is Alice?
```
The answer is inside the token.

JWT Structure

A JWT has three parts.
```
Header

.

Payload

.

Signature
```
Example:
```
xxxxx.yyyyy.zzzzz
```
Three Base64URL-encoded parts separated by dots.

### Part 1 – Header

Example
```
{
  "alg": "HS256",
  "typ": "JWT"
}
```
Meaning:
```
Algorithm

↓

HS256

Token Type

↓

JWT
```
### Part 2 – Payload

Example
```
{
  "sub": "alice",
  "role": "admin",
  "email": "alice@example.com",
  "exp": 1750000000
}
```
This contains claims.

Common claims:
```
sub

↓

Subject (User ID)

----------------

exp

↓

Expiration Time

----------------

iat

↓

Issued At

----------------

iss

↓

Issuer

----------------

aud

↓

Audience
```
Part 3 – Signature

This is the most important part.

Server computes:

Header

+

Payload

+

Secret Key

↓

Hash

↓

Signature

Suppose the payload says

{
  "role":"admin"
}

Attacker changes it to

{
  "role":"superadmin"
}

Now the signature no longer matches.

Server immediately rejects the token.

Complete JWT

Looks like

eyJhbGci...

.

eyJzdWI...

.

Qx9gK...
Request Flow
Alice

↓

Login

↓

Server Creates JWT

↓

Client Stores JWT

↓

Every Request

↓

Authorization: Bearer JWT

Server receives JWT.

Instead of querying a database, it:

Verifies the signature.
Checks expiration.
Reads the payload.
Knows the user.
Python Example

Create a JWT using PyJWT.

import jwt
import datetime

SECRET = "my-secret-key"

payload = {
    "sub": "alice",
    "role": "admin",
    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
}

token = jwt.encode(payload, SECRET, algorithm="HS256")

print(token)

Verify the token.

decoded = jwt.decode(
    token,
    SECRET,
    algorithms=["HS256"]
)

print(decoded)

Output

{
    "sub": "alice",
    "role": "admin",
    "exp": 1750000000
}

No database lookup required.

What Problem Did JWT Solve?
Problem 1 – Database Lookup

Before JWT

Bearer Token

↓

Database Lookup

↓

Find User

With JWT

Bearer Token

↓

Verify Signature

↓

Read Payload

No token lookup table.

Problem 2 – Microservices

Before JWT

Payment Service

↓

Redis

↓

User

After JWT

Payment Service

↓

Verify JWT

↓

Done

Every service can validate the same token independently (as long as it has the signing secret or public key).

Problem 3 – Scalability

Ten servers?

Hundred servers?

No shared session or token store is required for access token validation in the common JWT approach.

Does JWT Eliminate the Database Completely?

No.

This is a common misunderstanding.

Suppose the payload contains

{
   "sub":"alice"
}

If the request needs Alice's orders,

the application still queries:

Orders Table

JWT removes the need to look up who the token belongs to, not the need to fetch application data.

Security Problems Introduced by JWT
Problem 1 – Cannot Easily Revoke

Suppose Alice logs out.

The token is still valid until:

exp

expires.

That's why refresh tokens, short-lived access tokens, or token revocation strategies are commonly used.

Problem 2 – Never Store Sensitive Data

Bad payload:

{
   "password":"Password123"
}

JWT payloads are encoded, not encrypted.

Anyone holding the token can decode the header and payload.

Never store passwords or secrets inside a JWT.

JWT Is Signed, Not Encrypted

Many beginners think JWTs are encrypted.

Usually they are not.

Example payload

{
   "user":"Alice"
}

Anyone can Base64URL-decode it.

The signature prevents modification, but it does not hide the contents.

Evolution
Bearer Token

↓

Random String

↓

Server Lookup

↓

JWT

↓

Self-Contained Token

↓

Signature Verification

↓

No Token Lookup
Important Clarification

One of the biggest misconceptions is:

Bearer Token and JWT are not the same thing.

Think of it like this:

Authorization: Bearer <something>

The <something> could be:

A random opaque token (requiring a database or introspection lookup)
A JWT
Another token format

Bearer describes how the token is sent (the HTTP authentication scheme).

JWT describes what the token looks like (its format and contents).

So JWT did not replace Bearer Tokens.

JWT became one of the most popular formats for Bearer Tokens.

A more accurate chapter flow for your book

I would organize the story like this:

Chapter 7
Bearer Authentication
│
├── What is the Authorization: Bearer header?
├── Opaque (random) bearer tokens
├── Server-side token lookup
└── Limitations

        ↓

Chapter 8
JWT
│
├── Why opaque bearer tokens don't scale well
├── JWT structure (Header, Payload, Signature)
├── Signing vs Encryption
├── Validation
├── Python examples
├── Security pitfalls
└── Why refresh tokens become necessary

        ↓

Chapter 9
Refresh Tokens

That progression tells the historical and technical story much more naturally than introducing JWT without first establishing what a bearer token actually is.
