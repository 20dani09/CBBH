# sosimple

Proving Grounds Play · Linux

**Apunte parcial: enumeración de servicios.**

Las direcciones, fechas y versiones corresponden a las sesiones documentadas.

## Enumeración

```bash
nmap -p- --open -sS --min-rate 5000 -v -n -Pn $IP
```

```bash
nmap -sCV -p22,80 $IP
```

```text
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 5b5543efafd03d0e63207af4ac416a45 (RSA)
|   256 53f5231be9aa8f41e218c6055007d8d4 (ECDSA)
|_  256 55b77b7e0bf54d1bdfc35da1d768a96b (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: So Simple
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

## Referencias de consulta

- [Nmap: opciones y ejemplos](../../Tools/nmap-options.md).
- [Protocolos de red](../../Network-Pentesting/README.md).
