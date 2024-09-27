___

![[Pasted image 20240927133629.png]]

# VHost 

```bash
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt:FUZZ -u http://academy.htb:36410/ -H 'Host: FUZZ.academy.htb' -fs 985
```

![[Pasted image 20240927140045.png]]

![[Pasted image 20240927140239.png]]
# Extension 

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/web-extensions.txt:FUZZ -u http://faculty.academy.htb:36410/indexFUZZ
```




