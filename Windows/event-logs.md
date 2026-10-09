# Windows: consulta de eventos

| Comando | Descripción |
| --- | --- |
| `Get-WinEvent -LogName security \| where { $_.ID -eq 4688 -and $_.Properties[8].Value -like '*/user*' } \| Select-Object @{name='CommandLine';expression={ $_.Properties[8].Value }}` | Searching event logs with PowerShell                       |

El ejemplo filtra el evento de creación de procesos 4688. La presencia de la línea de comandos depende de la configuración de auditoría del sistema.

## Relacionado

- [Comandos locales](local-commands.md)
