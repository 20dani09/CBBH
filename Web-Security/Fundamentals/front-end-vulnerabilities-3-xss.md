# XSS

|Type|Description|
|---|---|
|`Reflected XSS`|Occurs when user input is displayed on the page after processing (e.g., search result or error message).|
|`Stored XSS`|Occurs when user input is stored in the back end database and then displayed upon retrieval (e.g., posts or comments).|
|`DOM XSS`|Occurs when user input is directly shown in the browser and is written to an `HTML` DOM object (e.g., vulnerable username or page title).|

```javascript
#"><img src=/ onerror=alert(document.cookie)>
```

## Procedencia

| Repositorio | Archivo original | Commit de origen |
| --- | --- | --- |
| CBBH | 2- Introduction to Web Applications/3 - Front End Vulnerabilities/3 - XSS.md | 284a0a42d23a00f2b47b7460371a517a14cb6261 |

[Índice de categoría](../README.md) · [Inicio](../../README.md)
