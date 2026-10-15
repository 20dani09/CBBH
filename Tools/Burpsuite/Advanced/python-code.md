_____

Python code to track requests

```python
burp = {'http:' 'http://127.0.0.1:8080'}
s = requests.Session()
s.proxies = burp
```



# Intercept requests

```
proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}
```

```python
request.get(arg.url,proxies=proxies, verify=False)
```

on the request.get add , proxies=proxies, verify=False
