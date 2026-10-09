# Estado de controles de seguridad

Consulta del estado de Defender, las políticas efectivas de AppLocker y el modo de lenguaje de PowerShell.

## Enumerating Security Controls

***

| Command                                                                    | Description                                                                                                                                                                                  |
| -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Get-MpComputerStatus`                                                     | PowerShell cmd-let used to check the status of `Windows Defender Anti-Virus` from a Windows-based host.                                                                                      |
| `Get-AppLockerPolicy -Effective \| select -ExpandProperty RuleCollections` | PowerShell cmd-let used to view `AppLocker` policies from a Windows-based host.                                                                                                              |
| `$ExecutionContext.SessionState.LanguageMode`                              | PowerShell script used to discover the `PowerShell Language Mode` being used on a Windows-based host. Performed from a Windows-based host.                                                   |

## Relacionado

- [Comandos locales de Windows](../Windows/local-commands.md)
- [Herramientas de revisión de Active Directory](audit-tools.md)
