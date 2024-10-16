___

```python
PORT     STATE SERVICE VERSION  
22/tcp   open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.6 (Ubuntu Linux; protocol 2.0)  
| ssh-hostkey:    
|   2048 e5:bb:4d:9c:de:af:6b:bf:ba:8c:22:7a:d8:d7:43:28 (RSA)  
|   256 d5:b0:10:50:74:86:a3:9f:c5:53:6f:3b:4a:24:61:19 (ECDSA)  
|_  256 e2:1b:88:d3:76:21:d4:1e:38:15:4a:81:11:b7:99:07 (ED25519)  
80/tcp   open  http    Apache httpd 2.4.18  
|_http-title: Did not follow redirect to http://help.htb/  
|_http-server-header: Apache/2.4.18 (Ubuntu)  
3000/tcp open  http    Node.js Express framework  
|_http-title: Site doesn't have a title (application/json; charset=utf-8).
```

```bash
gobuster dir -u http://$IP -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 200 -x php,txt,html
```

![[Pasted image 20241016173354.png]]

