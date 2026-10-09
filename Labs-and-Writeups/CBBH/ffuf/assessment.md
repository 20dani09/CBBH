# Skills Assessment

![Pasted image 20240927133629.png](../../../assets/images/4f0d4c02be4de575bb62.png)

## VHost 

```bash
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt:FUZZ -u http://academy.htb:36410/ -H 'Host: FUZZ.academy.htb' -fs 985
```

![Pasted image 20240927140045.png](../../../assets/images/7b062628e484fdd6ad97.png)

![Pasted image 20240927140239.png](../../../assets/images/10e25e207e278525284c.png)
## Extension 

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/web-extensions.txt:FUZZ -u http://faculty.academy.htb:36410/indexFUZZ
```

![Pasted image 20240927141007.png](../../../assets/images/583e31101a7093c58749.png)

## Recursive 

```bash
feroxbuster -u http://faculty.academy.htb:36410/ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt -x php,phps,php7 -f -r
```

![Pasted image 20240927141612.png](../../../assets/images/1f169d6d2fa2aa57ef8a.png)

## Parameters

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt:FUZZ -u http://faculty.academy.htb:36410/courses/linux-security.php7?FUZZ=key -fs 774
```

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt:FUZZ -u http://faculty.academy.htb:36410/courses/linux-security.php7 -X POST -d 'FUZZ=key' -H 'Content-Type: application/x-www-form-urlencoded' -fs 774
```

![Pasted image 20240927141922.png](../../../assets/images/49d416128e38e4218afb.png)

## Username fuzzing

```bash
ffuf -w /usr/share/seclists/Usernames/xato-net-10-million-usernames.txt -u http://faculty.academy.htb:36410/courses/linux-security.php7 -X POST -d 'username=FUZZ' -H 'Content-Type: application/x-www-form-urlencoded' -fs 781
```

![Pasted image 20240927143922.png](../../../assets/images/41083e59bf3822a09ef5.png)

```bash
curl -X POST -H 'Content-Type: application/x-www-form-urlencoded' http://faculty.academy.htb:36410/courses/linux-security.php7 -d 'username=harry'
```

![Pasted image 20240927144017.png](../../../assets/images/ca6b240d702b4a9e6f30.png)

## Material relacionado

- [Basic Fuzzing](../../../Tools/Ffuf/basic-fuzzing.md)
- [Domain Fuzzing](../../../Tools/Ffuf/domain-fuzzing.md)
- [Parameter](../../../Tools/Ffuf/parameter.md)


## Procedencia

| Repositorio | Archivo original | Commit de origen |
| --- | --- | --- |
| CBBH | 5- Ffuf/4 - Skills Assesment.md | 284a0a42d23a00f2b47b7460371a517a14cb6261 |

[Índice de categoría](../../README.md) · [Inicio](../../../README.md)
