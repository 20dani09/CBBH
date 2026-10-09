# Cockpit

Proving Grounds Practice · Linux

**Apunte parcial: enumeración de servicios.**

Las direcciones, fechas y versiones corresponden a las sesiones documentadas.

## Enumeración 1

```text
PORT     STATE SERVICE         VERSION
22/tcp   open  ssh             OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   3072 98:4e:5d:e1:e6:97:29:6f:d9:e0:d4:82:a8:f6:4f:3f (RSA)
|   256 57:23:57:1f:fd:77:06:be:25:66:61:14:6d:ae:5e:98 (ECDSA)
|_  256 c7:9b:aa:d5:a6:33:35:91:34:1e:ef:cf:61:a8:30:1c (ED25519)
80/tcp   open  http            Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: blaze
9090/tcp open  ssl/zeus-admin?
| ssl-cert: Subject: commonName=blaze/organizationName=d2737565435f491e97f49bb5b34ba02e
| Subject Alternative Name: IP Address:127.0.0.1, DNS:localhost
| Not valid before: 2024-02-04T17:41:51
|_Not valid after:  2124-01-11T17:41:51
|_ssl-date: TLS randomness does not represent time
```

## Enumeración 2

```text
PORT     STATE SERVICE         VERSION
22/tcp   open  ssh             OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 5c:10:b5:46:af:65:e7:cd:ee:6d:1f:8d:13:db:51:e0 (RSA)
|   256 bd:35:6a:56:05:4d:81:d9:ee:21:8d:c9:79:6e:99:1e (ECDSA)
|_  256 8a:71:4f:d1:ed:11:dd:9c:1f:c6:51:6c:e8:e3:81:88 (ED25519)
80/tcp   open  http            Apache httpd 2.4.41 ((Ubuntu))
|_http-title: blaze
|_http-server-header: Apache/2.4.41 (Ubuntu)
9090/tcp open  ssl/zeus-admin?
| fingerprint-strings: 
|   GetRequest, HTTPOptions: 
|     HTTP/1.1 400 Bad request
|     Content-Type: text/html; charset=utf8
|     Transfer-Encoding: chunked
|     X-DNS-Prefetch-Control: off
|     Referrer-Policy: no-referrer
|     X-Content-Type-Options: nosniff
|     <!DOCTYPE html>
|     <html>
|     <head>
|     <title>
|     request
|     </title>
|     <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
|     <meta name="viewport" content="width=device-width, initial-scale=1.0">
|     <style>
|     body {
|     margin: 0;
|     font-family: "RedHatDisplay", "Open Sans", Helvetica, Arial, sans-serif;
|     font-size: 12px;
|     line-height: 1.66666667;
|     color: #333333;
|     background-color: #f5f5f5;
|     border: 0;
|     vertical-align: middle;
|     font-weight: 300;
|     margin: 0 0 10px;
|_    @font-face {
| ssl-cert: Subject: commonName=blaze/organizationName=027af6e4d559460db863a8a071592855
| Subject Alternative Name: IP Address:127.0.0.1, DNS:localhost
| Not valid before: 2022-03-21T10:49:17
|_Not valid after:  2122-02-25T10:49:17
|_ssl-date: TLS randomness does not represent time
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
.....
```

## Referencias de consulta

- [Nmap: opciones y ejemplos](../../Tools/nmap-options.md).
- [Protocolos de red](../../Network-Pentesting/README.md).
