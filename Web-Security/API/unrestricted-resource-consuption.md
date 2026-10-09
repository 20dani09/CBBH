# Unrestricted Resource Consuption

https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/

```bash
curl -X 'POST' \ 'http://83.136.254.37:40649/api/v1/authentication/customers/passwords/resets/sms-otps' \ -H 'accept: application/json' \ -H 'Content-Type: application/json' \ -d '{ "Email": "redacted@example.invalid" }'
```

The SMS provider we are working with charges us a significant amount per message. We need to request a discount from them; otherwise, our revenues will decrease.

Use another customer's e-mail address and make the request multiple times

## Procedencia

| Repositorio | Archivo original | Commit de origen |
| --- | --- | --- |
| CBBH | API Attacks/4 - Unrestricted Resource Consuption.md | 284a0a42d23a00f2b47b7460371a517a14cb6261 |

Se han sustituido valores literales de autenticación o direcciones de correo por marcadores. Los detalles sin valores están en [el registro de redacciones](../../Resources/Audit/redactions.csv).

[Índice de categoría](../README.md) · [Inicio](../../README.md)
