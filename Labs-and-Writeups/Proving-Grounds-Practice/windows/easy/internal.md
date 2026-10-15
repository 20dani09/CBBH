_____

>[!INFO]
> IP=192.168.231.40
> Windows

# Nmap
| PORT     | STATE | SERVICE        |
|----------|-------|----------------|
| 53/tcp   | open  | domain         |
| 135/tcp  | open  | msrpc          |
| 139/tcp  | open  | netbios-ssn    |
| 445/tcp  | open  | microsoft-ds   |
| 3389/tcp | open  | ms-wbt-server  |
| 5357/tcp | open  | wsdapi         |
| 49152/tcp| open  | unknown        |
| 49153/tcp| open  | unknown        |
| 49155/tcp| open  | unknown        |
| 49156/tcp| open  | unknown        |
| 49158/tcp| open  | unknown        |

```bash
sudo nmap -p- --open -sS --min-rate 5000 -n -Pn $IP | grep -oP '\d+(?=/tcp)' | paste -sd ',' -
```

```python
PORT      STATE SERVICE            VERSION
53/tcp    open  domain             Microsoft DNS 6.0.6001 (17714650) (Windows Server 2008 SP1)
| dns-nsid:
|_  bind.version: Microsoft DNS 6.0.6001 (17714650)
135/tcp   open  msrpc              Microsoft Windows RPC
139/tcp   open  netbios-ssn        Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds       Windows Server (R) 2008 Standard 6001 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
3389/tcp  open  ssl/ms-wbt-server?
|_ssl-date: 2024-02-07T17:39:44+00:00; -5h59m50s from scanner time.
| rdp-ntlm-info:
|   Target_Name: INTERNAL
|   NetBIOS_Domain_Name: INTERNAL
|   NetBIOS_Computer_Name: INTERNAL
|   DNS_Domain_Name: internal
|   DNS_Computer_Name: internal
|   Product_Version: 6.0.6001
|_  System_Time: 2024-02-07T17:39:35+00:00
| ssl-cert: Subject: commonName=internal
| Not valid before: 2023-01-27T15:30:02
|_Not valid after:  2023-07-29T15:30:02
5357/tcp  open  http               Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Service Unavailable
49152/tcp open  msrpc              Microsoft Windows RPC
49153/tcp open  msrpc              Microsoft Windows RPC
49155/tcp open  msrpc              Microsoft Windows RPC
49156/tcp open  msrpc              Microsoft Windows RPC
49158/tcp open  msrpc              Microsoft Windows RPC
```

## SMBv2 exploit (CVE-2009-3103, Microsoft Security Advisory 975497)

```bash
nmap --script smb-vuln\* -p139,445 $IP
```

https://www.exploit-db.com/exploits/40280

- MS09-050
