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

![[Pasted image 20240927141007.png]]

# Recursive 

```bash
feroxbuster -u http://faculty.academy.htb:36410/ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt -x php,phps,php7 -f -r
```

![[Pasted image 20240927141612.png]]

# Parameters

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt:FUZZ -u http://faculty.academy.htb:36410/courses/linux-security.php7?FUZZ=key -fs 774
```

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt:FUZZ -u http://faculty.academy.htb:36410/courses/linux-security.php7?FUZZ=key -X POST -d 'FUZZ=key' -H 'Content-Type: application/x-www-form-urlencoded' -fs 774
```

![[Pasted image 20240927141922.png]]

