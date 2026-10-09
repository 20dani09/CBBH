# Certificate Transparency (HackingHub)

https://crt.sh/

```text
https://crt.sh/?cn=%.paypal.com
```

```text
https://crt.sh/?o=Paypal
```

```bash
curl -s 'https://crt.sh/?cn=paypal.com&output=json' | jq -r '.[].name_value' | sed 's/\*\.//g' | sort -u
```

```bash
curl -s 'https://crt.sh/?o=paypal&output=json' | jq -r '.[].common_name' | sed 's/\*\.//g' | sort -u > paypal.txt
```

```bash
cat paypal.txt | rev | cut -d "." -f 1,2 | rev | sort -u
```

## Procedencia

| Repositorio | Archivo original | Commit de origen |
| --- | --- | --- |
| CBBH | BB/hackinghub/Recon/Certificate Transparency.md | 284a0a42d23a00f2b47b7460371a517a14cb6261 |

[Índice de categoría](../README.md) · [Inicio](../../README.md)
