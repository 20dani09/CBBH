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
