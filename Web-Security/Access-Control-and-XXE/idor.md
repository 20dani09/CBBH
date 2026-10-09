# IDOR

![Pasted image 20241009183717.png](../../assets/images/8c28f60acfffd0bdda38.png)

uid=15 

![Pasted image 20241009184106.png](../../assets/images/d6b11702bc31e60e75a8.png)

## Encoded References

![Pasted image 20241009184432.png](../../assets/images/0fc08137006eb7075aae.png)

```bash
echo "MQ==" | base64 -d  
1
```

![Pasted image 20241009184607.png](../../assets/images/839991955f53e594a11a.png)

![Pasted image 20241009184635.png](../../assets/images/ae159dd2874d62d144a5.png)

## Insecure APIs

![Pasted image 20241009185527.png](../../assets/images/9bea572461d98a35f402.png)

```json
{"uid":"10","uuid":"bfd92386a1b48076792e68b596846499","role":"staff_admin","full_name":"admin","email":"redacted@example.invalid","about":"Never gonna give you up, Never gonna let you down"}
```

We can modify other users' details
[Captura pendiente de revisión: Pasted image 20241009185945.png](../../Resources/Audit/media.csv)

## Procedencia

| Repositorio | Archivo original | Commit de origen |
| --- | --- | --- |
| CBBH | 15- Web Attacks/2 - IDOR.md | 284a0a42d23a00f2b47b7460371a517a14cb6261 |

Se han sustituido valores literales de autenticación o direcciones de correo por marcadores. Los detalles sin valores están en [el registro de redacciones](../../Resources/Audit/redactions.csv).

[Índice de categoría](../README.md) · [Inicio](../../README.md)
