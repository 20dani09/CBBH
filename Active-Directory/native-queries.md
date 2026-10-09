# Active Directory: consultas con PowerShell

| Comando | Descripción |
| --- | --- |
| `Get-Module`                                                                             | PowerShell cmd-let used to list modules loaded in the current session, their version and command options from a Windows-based host.                                                                       |
| `Import-Module ActiveDirectory`                                                          | Loads the `Active Directory` PowerShell module from a Windows-based host.                                                                                                                 |
| `Get-ADDomain`                                                                           | PowerShell cmd-let used to gather Windows domain information from a Windows-based host.                                                                                                   |
| `Get-ADUser -Filter {ServicePrincipalName -ne "$null"} -Properties ServicePrincipalName` | PowerShell cmd-let used to enumerate user accounts on a target Windows domain and filter by `ServicePrincipalName`. Performed from a Windows-based host.                                  |
| `Get-ADTrust -Filter *`                                                                  | PowerShell cmd-let used to enumerate any trust relationships in a target Windows domain and filters by any (`-Filter *`). Performed from a Windows-based host.                            |
| `Get-ADGroup -Filter * \| select name`                                                   | PowerShell cmd-let used to enumerate groups in a target Windows domain and filters by the name of the group (`select name`). Performed from a Windows-based host.                         |
| `Get-ADGroup -Identity "Backup Operators"`                                               | PowerShell cmd-let used to search for a specifc group (`-Identity "Backup Operators"`). Performed from a Windows-based host.                                                              |
| `Get-ADGroupMember -Identity "Backup Operators"`                                         | PowerShell cmd-let used to discover the members of a specific group (`-Identity "Backup Operators"`). Performed from a Windows-based host.                                                |

## Directivas de grupo

| Comando | Descripción |
| --- | --- |
| `Get-GPO -All \| Select DisplayName`                                  | PowerShell cmd-let used to enumerate GPO names. Performed from a Windows-based host.                                                                                    |
| `Get-GPO -Guid 7CA9C789-14CE-46E3-A722-83F4097AF532`                  | PowerShell cmd-let used to display the name of a GPO given a `GUID`. Performed from a Windows-based host.                                                               |

## Referencia

[Get-Module: módulos de la sesión y módulos disponibles](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/get-module?view=powershell-5.1).

## Relacionado

- [Controles de seguridad](security-controls.md)
- [Herramientas de revisión](audit-tools.md)
