___

# GET

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt:FUZZ -u http://admin.academy.htb:46757/admin/admin.php?FUZZ=key -fs 798
```
# POST

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt:FUZZ -u http://admin.academy.htb:46757/admin/admin.php -X POST -d 'FUZZ=key' -H 'Content-Type: application/x-www-form-urlencoded' -fs 798
```

```bash
ffuf -w /usr/share/seclists/Fuzzing/1-digit-1-1000.txt -u http://admin.academy.htb:46757/admin/admin.php -X POST -d 'id=FUZZ' -H 'Content-Type: application/x-www-form-urlencoded' -fs 768
```



```bash
curl -X POST -H 'Content-Type: application/x-www-form-urlencoded' http://admin.academy.htb:46757/admin/admin.php -d 'id=73'
```

