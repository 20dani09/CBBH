___
# Vhost

```bash
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt:FUZZ -u http://nahamstore.thm/ -H 'Host: FUZZ.nahamstore.thm' -fw 125
```

![[Pasted image 20241012124444.png]]

```
www.nahamstore.thm shop.nahamstore.thm marketing.nahamstore.thm stock.nahamstore.thm
```


# Directory

```bash
feroxbuster -u http://nahamstore.thm -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt -x php
```

![[Pasted image 20241012125809.png]]

