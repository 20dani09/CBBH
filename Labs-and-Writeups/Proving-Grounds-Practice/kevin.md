# Kevin

Proving Grounds Practice · Windows

**Apunte parcial: enumeración de servicios.**

Las direcciones, fechas y versiones corresponden a las sesiones documentadas.

## Enumeración

```bash
sudo nmap -p- --open -sS --min-rate 5000 -n -Pn $IP | grep -oP '\d+(?=/tcp)' | paste -sd ',' -
```

```text
PORT      STATE  SERVICE       VERSION
80/tcp    open   http          GoAhead WebServer
|_http-server-header: GoAhead-Webs
| http-title: HP Power Manager
|_Requested resource was http://192.168.231.45/index.asp
135/tcp   open   msrpc         Microsoft Windows RPC
139/tcp   open   netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open   microsoft-ds  Windows 7 Ultimate N 7600 microsoft-ds (workgroup: WORKGROUP)
3389/tcp  closed ms-wbt-server
3573/tcp  open   tag-ups-1?
49152/tcp open   msrpc         Microsoft Windows RPC
49153/tcp open   msrpc         Microsoft Windows RPC
49154/tcp open   msrpc         Microsoft Windows RPC
49155/tcp open   msrpc         Microsoft Windows RPC
49158/tcp open   msrpc         Microsoft Windows RPC
49160/tcp open   msrpc         Microsoft Windows RPC
Service Info: Host: KEVIN; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode:
|   2:1:0:
|_    Message signing enabled but not required
|_clock-skew: mean: -3h19m50s, deviation: 4h37m07s, median: -5h59m50s
| smb-security-mode:
|   account_used: <blank>
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb-os-discovery:
|   OS: Windows 7 Ultimate N 7600 (Windows 7 Ultimate N 6.1)
|   OS CPE: cpe:/o:microsoft:windows_7::-
|   Computer name: kevin
|   NetBIOS computer name: KEVIN\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2024-02-07T11:06:27-08:00
|_nbstat: NetBIOS name: KEVIN, NetBIOS user: <unknown>, NetBIOS MAC: 00:50:56:ba:44:3e (VMware)
| smb2-time:
|   date: 2024-02-07T19:06:27
|_  start_date: 2024-02-07T19:03:43
```

## Referencias de consulta

- [Nmap: opciones y ejemplos](../../Tools/nmap-options.md).
- [Protocolos de red](../../Network-Pentesting/README.md).
