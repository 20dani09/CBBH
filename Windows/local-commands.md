# Cuenta local y arquitectura de proceso

```cmd
net user username
```

## Check architecture

```powershell
[Environment]::Is64BitProcess
```

## Consultas del sistema

### Initial Enumeration

| **Command**                                                                                           | **Description**                                |
| ----------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| `xfreerdp /v:<target ip> /u:htb-student`                                                              | RDP to lab target                              |
| `ipconfig /all`                                                                                       | Get interface, IP address and DNS information  |
| `arp -a`                                                                                              | Review ARP table                               |
| `route print`                                                                                         | Review routing table                           |
| `Get-MpComputerStatus`                                                                                | Check Windows Defender status                  |
| `Get-AppLockerPolicy -Effective \| select -ExpandProperty RuleCollections`                            | List AppLocker rules                           |
| `Get-AppLockerPolicy -Local \| Test-AppLockerPolicy -path C:\Windows\System32\cmd.exe -User Everyone` | Test AppLocker policy                          |
| `set`                                                                                                 | Display all environment variables              |
| `systeminfo`                                                                                          | View detailed system configuration information |
| `wmic qfe`                                                                                            | Get patches and updates                        |
| `wmic product get name`                                                                               | Get installed programs                         |
| `tasklist /svc`                                                                                       | Display running processes                      |
| `query user`                                                                                          | Get logged-in users                            |
| `echo %USERNAME%`                                                                                     | Get current user                               |
| `whoami /priv`                                                                                        | View current user privileges                   |
| `whoami /groups`                                                                                      | View current user group information            |
| `net user`                                                                                            | Get all system users                           |
| `net localgroup`                                                                                      | Get all system groups                          |
| `net localgroup administrators`                                                                       | View details about a group                     |
| `net accounts`                                                                                        | Get passsword policy                           |
| `netstat -ano`                                                                                        | Display active network connections             |
| `pipelist.exe /accepteula`                                                                            | List named pipes                               |
| `gci \\.\pipe\`                                                                                       | List named pipes with PowerShell               |
| `accesschk.exe /accepteula \\.\Pipe\lsass -v`                                                         | Review permissions on a named pipe             |

## Compatibilidad y efectos de las consultas

La disponibilidad de WMIC depende de la versión de Windows. La consulta `wmic product get name` utiliza Win32_Product y puede iniciar comprobaciones y reparaciones de paquetes MSI; no es una consulta sin efectos secundarios.

[Comportamiento de Win32_Product, Microsoft](https://learn.microsoft.com/en-us/troubleshoot/windows-server/admin-development/windows-installer-reconfigured-all-applications).

## Relacionado

- [Codificación y hashes](file-encoding-and-hashes.md)
- [Consultas de dominio](../Active-Directory/native-queries.md)

## Filtro de conexiones

| Comando | Descripción |
| --- | --- |
| `netstat -antb \|findstr 1080`                                                                                                                                                                                     | Windows-based command used to list TCP network connections listening on port 1080.                                                                                                                                                                                      |

La tubería filtra líneas que contienen `1080`; la coincidencia no prueba por sí sola que un puerto esté escuchando.
