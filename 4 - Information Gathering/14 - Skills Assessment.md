___

> What is the IANA ID of the registrar of the inlanefreight.com domain?

![[Pasted image 20240926183811.png]]

> What http server software is powering the inlanefreight.htb site on the target system? Respond with the name of the software, not the version, e.g., Apache.

![[Pasted image 20240926184026.png]]

> What is the API key in the hidden admin directory that you have discovered on the target system?

```bash
gobuster vhost -u http://inlanefreight.htb:45308/ -w /usr/share/seclists/Discovery/DNS/subdo  
mains-top1million-110000.txt --append-domain
```

![[Pasted image 20240926184858.png]]

