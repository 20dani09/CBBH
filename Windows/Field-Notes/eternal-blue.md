____
machine
```bash
sudo nmap -sV -p445 --script=smb-vuln-ms17-010 $IP
```

```bash
nmap -p 445 -script vuln -oA scans/nmap-smbvulns $IP
```

```bash
nmap --script "vuln and safe" -p445 $IP
```

# Exploit github
____

https://github.com/worawit/MS17-010.git

https://github.com/3ndG4me/AutoBlue-MS17-010


# Metasploit
____

exploit/windows/smb/ms17_010_eternalblue

exploit(windows/smb/ms17_010_psexec)
