# Squid

Proving Grounds Practice · Windows

**Apunte parcial: enumeración de servicios.**

Las direcciones, fechas y versiones corresponden a las sesiones documentadas.

## Enumeración

```bash
sudo nmap -p- --open -sS --min-rate 5000 -n -Pn $IP | grep -oP '\d+(?=/tcp)' | paste -sd ',' -
```

```text
PORT      STATE SERVICE       VERSION
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds?
3128/tcp  open  http-proxy    Squid http proxy 4.14
|_http-server-header: squid/4.14
|_http-title: ERROR: The requested URL could not be retrieved
49666/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-time: 
|   date: 2024-02-08T10:22:56
|_  start_date: N/A
|_clock-skew: -5h59m50s
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
```

## Referencias de consulta

- [Nmap: opciones y ejemplos](../../Tools/nmap-options.md).
- [Protocolos de red](../../Network-Pentesting/README.md).
