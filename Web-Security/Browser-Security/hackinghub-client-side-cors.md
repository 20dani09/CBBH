# CORS (HackingHub)

Cross-Origin Resource Sharing

Third-party cookies are used when a website (Website A) makes a request to another website (Website B). The cookies from Website B are sent along with the request. For these cookies to be sent, the original website must set the cookie with specific attributes: it must be secure (only sent over HTTPS), httponly (not accessible via JavaScript), and have the samesite policy set to None.

```text
Access-Control-Allow-Headers: Content-Type
Access-Control-Allow-Origin: https://3hzvbqwn.eu1.ctfio.com
Access-Control-Allow-Credentials: true
```

On the request add Origin

## Procedencia

| Repositorio | Archivo original | Commit de origen |
| --- | --- | --- |
| CBBH | BB/hackinghub/Client side/CORS.md | 284a0a42d23a00f2b47b7460371a517a14cb6261 |

[Índice de categoría](../README.md) · [Inicio](../../README.md)
