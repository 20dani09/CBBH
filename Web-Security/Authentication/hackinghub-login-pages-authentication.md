# Login Pages - Authentication (HackingHub)

## Weak Passwords

[Captura pendiente de revisión: Pasted image 20241217114441.png](../../Resources/Audit/media.csv)

## Default Passwords

Search for "Default credentials" on google

## Username enumeration through errors

Username is invalid

![Pasted image 20241217120440.png](../../assets/images/46ffdb11a35ccdde66df.png)
## Username Enumeration Through Forgot Password Function

Invalid username supplied

![Pasted image 20241217122422.png](../../assets/images/eb2211749eeafc420310.png)

## Brute Forcing Username and Password

Cluster-bomb

## Self Registration Using Content Discovery

```bash
ffuf -u https://vdooaly3.eu1.ctfio.com/hidden-registration/user_FUZZ -w content.txt
```

![Pasted image 20241217123723.png](../../assets/images/6dd3a751f3556b9c429d.png)

### Javascript Files

![Pasted image 20241217123935.png](../../assets/images/33c476dde63f33c02cc3.png)

### APIs

Leaked ``/by-api/api/auth/login/``

![Pasted image 20241217124748.png](../../assets/images/0934c974823347a9dd3d.png)

## Brute Forcing One-Time Password (OTP)

![Pasted image 20241217125652.png](../../assets/images/517c1f62d2eb2098a0e8.png)

## Leaked Password Reset Tokens
### 1
![Pasted image 20241217131421.png](../../assets/images/842af3ae24ba0572b6ef.png)

```bash
ffuf -u https://vdooaly3.eu1.ctfio.com/reset-token-leak/FUZZ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
```

![Pasted image 20241217131733.png](../../assets/images/658b58f79cab53b7532a.png)

![Pasted image 20241217131757.png](../../assets/images/acb48b139823956d9f5c.png)

![Pasted image 20241217131922.png](../../assets/images/d3999201783308ea7ac1.png)

### 2

```bash
ffuf -u https://vdooaly3.eu1.ctfio.com/api-token-leak/api/FUZZ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
```

![Pasted image 20241217133540.png](../../assets/images/01d07025608c93ba0824.png)

## Forced Password Reset

Add email field, 
[Captura pendiente de revisión: Pasted image 20241217134424.png](../../Resources/Audit/media.csv)

https://github.com/Vozec/CVE-2023-7028


```text
user[email][]=redacted@example.invalid&user[email][]=redacted@example.invalid
```

## Bypassing API Authentication with X-Forwarded-For

![Pasted image 20241217134850.png](../../assets/images/e4f2852f8b247ee82bb5.png)


```text
X-forwarded-for: 127.0.0.1
```

![Pasted image 20241217135113.png](../../assets/images/a959b0ad8f7e8aacdb1f.png)
## X-Forwarded-For with Information Disclosure

```bash
curl -I https://mzg7ibfb.eu1.ctfio.com/by-api-xip-2/admin/
```

![Pasted image 20241217135449.png](../../assets/images/a3272057e6bcab28f62d.png)

![Pasted image 20241217135702.png](../../assets/images/edcd52335a7e0b344a7c.png)
Brute force, 
![Pasted image 20241217135826.png](../../assets/images/970824f95a01839383de.png)
## Mass Assignment

[Captura pendiente de revisión: Pasted image 20241217154708.png](../../Resources/Audit/media.csv)

Add status on the register, 

[Captura pendiente de revisión: Pasted image 20241217154902.png](../../Resources/Audit/media.csv)

![Pasted image 20241217154932.png](../../assets/images/0a576b032a3187a81cda.png)

## Procedencia

| Repositorio | Archivo original | Commit de origen |
| --- | --- | --- |
| CBBH | BB/hackinghub/Login Pages - Authentication.md | 284a0a42d23a00f2b47b7460371a517a14cb6261 |

Se han sustituido valores literales de autenticación o direcciones de correo por marcadores. Los detalles sin valores están en [el registro de redacciones](../../Resources/Audit/redactions.csv).

[Índice de categoría](../README.md) · [Inicio](../../README.md)
