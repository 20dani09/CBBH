_____

```bash
openssl s_client -connect $IP:443
```

# Fuzzing


```bash
gobuster dir -u http://$IP -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 200 -x php,txt,html -k
```
