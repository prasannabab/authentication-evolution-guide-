# Chapter 06:
<b> API Keys were NOT invented to replace sessions.</b>

> They were invented because sessions don't fit application-to-application communication.

Let's pretend sessions never existed and start from scratch.

Suppose you build a Weather API.
```
Weather API
```
Another company builds a Travel website.
```
Travel Website
```
The Travel Website wants today's weather.

So it sends:
```
GET /weather?city=London
```
Your Weather API receives it.

Now your API asks...

> Who is making this request?

There are two possibilities.

#### Option 1

Nobody.

Anyone can access your API.
```
Internet

↓

Weather API
```
Problem:

Millions of requests.
Spam.

Bots.

Huge cloud bills.

No way to block anyone.

So you need authentication.

Now think...

How should the Travel Website authenticate?

First Idea

Give every company
```
Username
Password
```
Example
```
Username = travel_company

Password = password123
```
Every request:
```
GET /weather

Username: travel_company

Password: password123
```
Would this work?

Yes.

But Engineers Started Asking Questions

Imagine 1000 companies use your API.

Travel Company

Food Company

Taxi Company

Bank

Hotel

Airline

Each has
```
Username

Password
```
Now suppose one developer accidentally uploads
```
password123
```
to GitHub.

Now the attacker has the real account password.

That account may also be used to:

Log into your dashboard
Change billing
Delete resources
Change settings

You've exposed the master credential.

Engineers Asked

> Why give applications a real account password?

Applications aren't humans.

They don't log into dashboards.

They only need one thing:

Call the API

Nothing more.

New Idea

Instead of giving applications
```
Username

Password
```
Give them

Random Secret

Example
```
abc123xyz987
```
This secret has only one purpose:

Call Weather API

It cannot log into your dashboard.

It cannot change your password.

It cannot reset your account.

It only identifies the application.

This random secret became the API Key.

So What Changed?

Instead of
```
Username: travel_company
Password: password123
```
You now send
```
X-API-Key: abc123xyz987
```
The server checks:
```
abc123xyz987

↓

Travel Website

↓

Allowed
```
Notice what happened.

The server is not asking

Who is the user?

It is asking

Which application is calling me?

That is a completely different problem.

Let's Build It

Suppose your Weather API stores:
```
API_KEYS = {
    "abc123": "Travel Website",
    "xyz999": "Food Delivery"
}
```
Incoming request:
```
GET /weather

X-API-Key: abc123
```
Python:
```
api_key = request.headers.get("X-API-Key")

if api_key in API_KEYS:
    print("Valid Application")
else:
    print("Unauthorized")
```
No login.

No session.

No cookie.

Just one lookup.

### What Problem Did API Keys Solve?
##### Problem 1

Applications should not know real account passwords.

Instead
```
Application

↓

API Key
```
##### Problem 2

Applications don't have browsers.

Therefore
```
No Cookies

No Sessions
```
##### Problem 3

Need to identify
```
Application

instead of

User
```

#### Problem 4

Need easy revocation.

Suppose Travel Website is hacked.

Delete:
```
abc123
```
Generate
```
newKey987
```
Done.

Nobody changes passwords.
<br>
<br>
<br>

> below has the details about why Bearer token is needed

<b>An API Key does NOT have to know about the user.</b>

The reason <b>Bearer Tokens</b> were invented is because <b>some APIs need to know which user is making the request.</b>

Let's build this slowly.

##### Case 1: Weather API

Suppose you built this API:
```
Weather API
```
Your customer is:
```
Travel Website
```
Request:
```
GET /weather?city=London

X-API-Key: abc123
```
Server checks:
```
abc123

↓

Travel Website
```
##### Question:

> Does the Weather API care whether Alice or Bob clicked the button?

<b> No. </b>

It simply returns:
```
{
   "temperature": 28
}
```
Everyone gets the same weather.

So the API Key is enough.

##### Case 2: Banking API

Now imagine:
```
Bank API
```
Request:
```
GET /balance
```
> Should everyone receive the same balance?

<b>No.</b>

Suppose three users exist.
```
Alice
$10,000

Bob
$2,500

Charlie
$500
```
Now the request arrives.
```
GET /balance

X-API-Key: bank-mobile-app
```
What should the server return?
```
Alice's balance?

Bob's balance?

Charlie's balance?
```
The API Key only tells us:
```
Request came from

↓

Bank Mobile App
```
It does not tell us

Which customer?
Why?

Because every customer uses the same mobile application.
```
Alice
      \
Bob -----> Bank Mobile App
      /
Charlie
```
The mobile app has one API Key.
```
API Key

↓

bank-mobile-app
```
If 10 million customers use the app,

the API Key is still the same.
<br>
<br>
<br>
You are thinking:

> If we already have sessions for users and API Keys for service-to-service communication, why did Bearer Tokens come?

The answer is:

<b>Bearer Tokens were NOT invented because API Keys needed user information.</b>

<b>They were invented because sessions don't work well for modern API clients (mobile apps, SPAs, microservices).</b>

Let's go through the timeline.

##### Phase 1 - Traditional Web Applications

Around 2000, a typical application looked like this.
```
Browser
   │
   ▼
Web Server
   │
   ▼
Database
```
User logs in.

Username + Password

Server creates

Session

Browser stores

Cookie

Everything works.

There is no API Key involved.

##### Phase 2 - Service-to-Service APIs

Now companies expose APIs.

Example:
```
Travel Website
      │
      ▼
Weather API
```
Question:
```
Who is calling?
```
Answer:
```
Travel Website
```
So API Keys were introduced.
```
GET /weather

X-API-Key: abc123
```
<b>Notice:<b>
```
No user.

No session.

No JWT.
```
The API Key is enough.

##### Phase 3 - Mobile Apps Arrive

Now smartphones become popular.

Example:
```
Alice

↓

Bank Mobile App

↓

Bank API
```
Now think carefully.

Alice logs into the mobile app.

Should the mobile app use sessions?

Option 1 - Use Sessions

Alice logs in.

Server creates
```
SESSIONID=xyz
```
Now every API request must send
```
Cookie:
SESSIONID=xyz
```
Question:

> Who automatically manages cookies?

Answer:

> Browsers.

Not all mobile apps.

Not all desktop applications.

Not all IoT devices.

Not every API client.

A mobile developer now has to:
```
Store cookies.
Handle cookie expiration.
Handle cookie domains and paths.
Deal with cookie policies.
```
It becomes cumbersome outside the browser.

Another Problem - Microservices

Imagine Netflix.
```
Browser

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
Suppose the session is stored in:
```
Redis
```
Every service now has to ask Redis:

> Who owns SESSIONID xyz?

Every request.

Thousands of times per second.

This creates coupling and extra network lookups.

#### The Big Question

What if we don't store the user's session on the server at all?

What if the client carries proof of identity?

That idea became the Bearer Token.

Bearer Token

Instead of
```
SESSIONID = xyz
```
The client receives

Bearer Token
```
Example:

Authorization:
Bearer abc123xyz
```
Now every service simply verifies the token.

No shared session lookup is required.

Where Does API Key Fit?

Here's the key insight.

API Keys and Bearer Tokens solve different problems.

API Key

Answers:

Which application is calling?

Example
```
Google Maps

↓

Uber App
```
Google only cares that

Uber App

is an authorized client.

Bearer Token

Answers:

Which user is using Uber?

Example
```
Uber App

↓

Alice
```
Now Uber backend knows

Alice
Can They Exist Together?

Absolutely.

Example:
```
POST /orders

X-API-Key: mobile-app-key

Authorization: Bearer eyJhbGci...
```
Now the backend knows
```
Application

↓

Official Mobile App

AND

User

↓

Alice
```
Both identities are useful.

> So Why Not Continue Using Sessions?

Good question.

Sessions work extremely well for traditional web applications.

Example:
```
Browser

↓

Amazon Website
```
Sessions are still widely used there.

The problem appeared when clients became more diverse.

Today, clients include:
```
Browser

Mobile App

React SPA

CLI Tool

Python Script

IoT Device

Smart TV

Game Console
```
A browser naturally understands cookies.

Most other clients do not have built-in browser cookie behavior.

Using a simple HTTP header is often easier across all of them.

Evolution Timeline

Notice that there are actually two parallel tracks.

                 USER AUTHENTICATION
```
Username + Password
        │
        ▼
Sessions (Browser)
        │
        ▼
Bearer Tokens
        │
        ▼
JWT
        │
        ▼
OAuth / OIDC

```
          APPLICATION AUTHENTICATION
```
Username + Password
        │
        ▼
API Keys
        │
        ▼
Client Credentials (OAuth)
```
This is the part that most tutorials never explain.

People usually draw one straight line:
```
Sessions
↓

API Keys
↓

Bearer Tokens
```
That is historically misleading.

The reality is:
```
Sessions evolved for browser users.
API Keys evolved for application identity (service-to-service communication).
Bearer Tokens evolved for user identity in API-based clients (mobile apps, SPAs, distributed systems).
The one sentence that makes everything click
```


Authentication evolved along two parallel paths:

<b>User Authentication: Sessions → Bearer Tokens → JWT → OAuth/OIDC </b>
 <b> Application Authentication: Basic Authentication → API Keys → OAuth 2.0 Client Credentials  </b>

That distinction will prevent readers from thinking that API Keys "became" Bearer Tokens. They didn't—they solve different authentication problems.
