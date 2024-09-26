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

![[Pasted image 20240926185150.png]]

```
The admin panel is currently under maintenance, but the API is still accessible with the key e963d863ee0e82ba7080fbf558ca0d3f
```

> After crawling the inlanefreight.htb domain on the target system, what is the email address you have found? Respond with the full email, e.g., mail@inlanefreight.htb.

```
gobuster vhost -u http://web1337.inlanefreight.htb:45308/ -w /usr/share/seclists/Discovery/D  
NS/subdomains-top1million-110000.txt --append-domain
```

![[Pasted image 20240926185907.png]]

![[Pasted image 20240926190935.png]]


> What is the API key the inlanefreight.htb developers will be changing too?

![[Pasted image 20240926190202.png]]


