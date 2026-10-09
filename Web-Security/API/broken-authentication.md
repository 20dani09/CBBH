# Broken Authentication

```bash
curl -X 'POST' \ 'http://94.237.63.111:30334/api/v1/authentication/customers/passwords/resets/email-otps' \ -H 'accept: application/json' \ -H 'Content-Type: application/json' \ -d '{ "Email": "redacted@example.invalid" }'
```


[Captura pendiente de revisión: Pasted image 20240930183703.png](../../Resources/Audit/media.csv)

## Procedencia

| Repositorio | Archivo original | Commit de origen |
| --- | --- | --- |
| CBBH | API Attacks/2 - Broken Authentication.md | 284a0a42d23a00f2b47b7460371a517a14cb6261 |

Se han sustituido valores literales de autenticación o direcciones de correo por marcadores. Los detalles sin valores están en [el registro de redacciones](../../Resources/Audit/redactions.csv).

[Índice de categoría](../README.md) · [Inicio](../../README.md)
