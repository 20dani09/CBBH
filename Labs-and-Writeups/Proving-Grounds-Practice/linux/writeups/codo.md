____
# Walkthrough for Codo

## Enumeration

We start with a simple nmap scan

```
┌──(vagrant㉿kali)-[~/cves/codo]
└─$ nmap -sC -sV 192.168.146.134
Starting Nmap 7.92 ( https://nmap.org ) at 2022-09-01 01:34 EDT
Nmap scan report for 192.168.146.134
Host is up (0.0014s latency).
Not shown: 998 filtered tcp ports (no-response)
Bug in http-generator: no string output.
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 8e:69:b1:98:e6:dc:54:5d:47:c2:79:db:bb:3c:a9:b6 (RSA)
|   256 1e:9e:53:0c:77:ad:ff:ad:f1:c6:60:94:16:32:88:26 (ECDSA)
|_  256 1a:94:b9:9f:77:40:2d:ef:e6:51:3e:d4:65:71:4d:6a (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: All topics | CODOLOGIC
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.54 seconds
```

We find port 22 and 80 as open

We find Codoforum on port 80

admin:admin works for login http://192.168.146.134/admin

## Exploitation

Vulnerable to CVE-2022-31854 - https://www.exploit-db.com/exploits/50978

Login to the admin panel and upload `shell.php` in Upload logo

shell.php is uploaded at http://192.168.146.134/sites/default/assets/img/attachments/shell.php

We have code execution as `www-data`
