___

```bash
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt:FUZZ -u http://nahamstore.thm/ -H 'Host: FUZZ.nahamstore.thm' -fw 125
```

![[Pasted image 20241012124444.png]]

