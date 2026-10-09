# Broken Function Level Authorization

```json
{
  "errorMessage": "User does not have any roles assigned"
}
```

![Pasted image 20241001194701.png](../../assets/images/d1c4b7601da2121f2448.png)


```bash
curl -X 'GET' \ 'http://83.136.254.37:40649/api/v1/customers/billing-addresses' \ -H 'accept: application/json' \ -H 'Authorization: Bearer <REDACTED_JWT>'
```

![Pasted image 20241001194859.png](../../assets/images/d0d2616e82ac5b5453ad.png)

## Procedencia

| Repositorio | Archivo original | Commit de origen |
| --- | --- | --- |
| CBBH | API Attacks/5 - Broken Function Level Authorization.md | 284a0a42d23a00f2b47b7460371a517a14cb6261 |

Se han sustituido valores literales de autenticación o direcciones de correo por marcadores. Los detalles sin valores están en [el registro de redacciones](../../Resources/Audit/redactions.csv).

[Índice de categoría](../README.md) · [Inicio](../../README.md)
