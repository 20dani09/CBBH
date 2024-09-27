___

# GET

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt:FUZZ -u http://admin.academy.htb:46757/admin/admin.php?FUZZ=key -fs 798
```


