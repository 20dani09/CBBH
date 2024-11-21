___

Content Security Policy

# Data

```
content-security-policy
	script-src 'self' https://app.hackinghub.io data:
```

```bash
<script data="data:text/html",<script>alert()</script>"></script>
```