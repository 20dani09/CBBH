# Basic Fuzzing

## Directory 

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt:FUZZ -u http://83.136.255.217:55982/FUZZ
```

## Extension 

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/web-extensions.txt:FUZZ -u http://83.136.255.217:55982/blog/indexFUZZ
```

## Page 

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt:FUZZ -u http://83.136.255.217:55982/blog/FUZZ.php
```

## Recursive 

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt:FUZZ -u http://83.136.255.217:55982/FUZZ -recursion -recursion-depth 1 -e .php -v
```


## Feroxbuster

```bash
feroxbuster -u http://83.136.255.217:55982 -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt -x php -f -r
```

## Procedencia

| Repositorio | Archivo original | Commit de origen |
| --- | --- | --- |
| CBBH | 5- Ffuf/1 - Basic Fuzzing.md | 284a0a42d23a00f2b47b7460371a517a14cb6261 |

[Índice de categoría](../README.md) · [Inicio](../../README.md)
