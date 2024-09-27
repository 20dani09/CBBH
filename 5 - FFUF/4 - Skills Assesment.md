___

![[Pasted image 20240927133629.png]]

# 

```bash
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt:FUZZ -u http://academy.htb:36410/ -H 'Host: FUZZ.academy.htb' -fs 985
```