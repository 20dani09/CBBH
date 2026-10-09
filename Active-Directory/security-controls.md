# Estado de controles de seguridad

Se conserva la consulta local de Defender, AppLocker y LanguageMode. Las funciones relacionadas con acceso a contraseñas de LAPS permanecen en la fuente.

## Enumerating Security Controls

***

| Command                                                                    | Description                                                                                                                                                                                  |
| -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Get-MpComputerStatus`                                                     | PowerShell cmd-let used to check the status of `Windows Defender Anti-Virus` from a Windows-based host.                                                                                      |
| `Get-AppLockerPolicy -Effective \| select -ExpandProperty RuleCollections` | PowerShell cmd-let used to view `AppLocker` policies from a Windows-based host.                                                                                                              |
| `$ExecutionContext.SessionState.LanguageMode`                              | PowerShell script used to discover the `PowerShell Language Mode` being used on a Windows-based host. Performed from a Windows-based host.                                                   |

## Procedencia

| Repositorio | Archivo original | Commit de origen |
| --- | --- | --- |
| notes | active-directory/enumerating-security-controls.md | b4c68ccbe43fe7218e8cee1a15bb7346a6c3bb89 |

[Índice de categoría](README.md) · [Inicio](../README.md)
