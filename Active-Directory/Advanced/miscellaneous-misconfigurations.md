# Miscellaneous Misconfigurations

***

| Command                                                                                       | Description                                                                                                                                             |
| --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Import-Module .\SecurityAssessment.ps1`                                                      | Used to import the module `Security Assessment.ps1`. Performed from a Windows-based host.                                                               |
| `Get-SpoolStatus -ComputerName ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL`                           | SecurityAssessment.ps1 based tool used to enumerate a Windows target for `MS-PRN Printer bug`. Performed from a Windows-based host.                     |
| `adidnsdump -u inlanefreight\\forend ldap://172.16.5.5`                                       | Used to resolve all records in a DNS zone over `LDAP` from a Linux-based host.                                                                          |
| `adidnsdump -u inlanefreight\\forend ldap://172.16.5.5 -r`                                    | Used to resolve unknown records in a DNS zone by performing an `A query` (`-r`) from a Linux-based host.                                                |
| `Get-DomainUser * \| Select-Object samaccountname,description`                                | PowerView tool used to display the description field of select objects (`Select-Object`) on a target Windows domain from a Windows-based host.          |
| `Get-DomainUser -UACFilter PASSWD_NOTREQD \| Select-Object samaccountname,useraccountcontrol` | PowerView tool used to check for the `PASSWD_NOTREQD` setting of select objects (`Select-Object`) on a target Windows domain from a Windows-based host. |
| `ls \\academy-ea-dc01\SYSVOL\INLANEFREIGHT.LOCAL\scripts`                                     | Used to list the contents of a share hosted on a Windows target from the context of a currently logged on user. Performed from a Windows-based host.    |
