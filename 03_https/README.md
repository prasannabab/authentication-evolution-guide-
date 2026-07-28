## Why did it evolve?

Chapters 1 and 2 solved the database security problem by hashing passwords.

But another problem remained.

Imagine Alice logs in from a coffee shop.
```
Alice
   |
   | username=alice
   | password=MyPassword123
   |
Wi-Fi Router
   |
Internet
   |
Server
```
If the connection uses plain HTTP, anyone on the same network can capture the traffic.

### Security Issues
Packet Sniffing

An attacker running a packet capture tool (such as Wireshark) could see:
```
POST /login HTTP/1.1

username=alice
password=MyPassword123
```
Even though the password is hashed in the database, it travels as plain text over HTTP before reaching the server.

Hashing protects stored passwords, not passwords in transit.

### Man-in-the-Middle (MITM)
```
Alice
   |
Attacker
   |
Server
```
The attacker intercepts and can even modify requests.

### Solution
Use TLS (HTTPS).
```
Alice
    |
Encrypted Tunnel
    |
Server
```
Now the attacker only sees encrypted bytes.


