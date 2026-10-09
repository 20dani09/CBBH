# XSS

## Stored & Reflected

```html
<script>alert(document.cookie)</script>
```

![Pasted image 20240927172636.png](../../assets/images/f776d8605dd6b2e70b75.png)

![Pasted image 20240927172309.png](../../assets/images/f760422f6c364a826de3.png)

## DOM 

Some of the commonly used JavaScript functions to write to DOM objects are:

- `document.write()`
- `DOM.innerHTML`
- `DOM.outerHTML`

Furthermore, some of the `jQuery` library functions that write to DOM objects are:

- `add()`
- `after()`
- `append()`

```html
<img src="" onerror=alert(document.cookie)>
```


## Automated Discovery

https://github.com/s0md3v/XSStrike

Burp scanner

*Captura omitida por posibles datos sensibles.*
## Payloads

https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XSS%20Injection/README.md
https://github.com/payloadbox/xss-payload-list
