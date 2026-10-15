# 53 - DNS

***

| **Command**                                                                                                   | **Description**                          |
| ------------------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| `dig ns <domain.tld> @<nameserver>`                                                                           | NS request to the specific nameserver.   |
| `dig any <domain.tld> @<nameserver>`                                                                          | ANY request to the specific nameserver.  |
| `dig axfr <domain.tld> @<nameserver>`                                                                         | AXFR request to the specific nameserver. |
| `dnsenum --dnsserver <nameserver> --enum -p 0 -s 0 -o found_subdomains.txt -f ~/subdomains.list <domain.tld>` | Subdomain brute forcing.                 |

## DNS Records

| DNS Record | Description                                                                                                                                                                                                                                       |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A          | Returns an IPv4 address of the requested domain as a result.                                                                                                                                                                                      |
| AAAA       | Returns an IPv6 address of the requested domain.                                                                                                                                                                                                  |
| MX         | Returns the responsible mail servers as a result.                                                                                                                                                                                                 |
| NS         | Returns the DNS servers (nameservers) of the domain.                                                                                                                                                                                              |
| TXT        | This record can contain various information. The all-rounder can be used, e.g., to validate the Google Search Console or validate SSL certificates. In addition, SPF and DMARC entries are set to validate mail traffic and protect it from spam. |
| CNAME      | This record serves as an alias. If the domain www.hackthebox.eu should point to the same IP, and we create an A record for one and a CNAME record for the other.                                                                                  |
| PTR        | The PTR record works the other way around (reverse lookup). It converts IP addresses into valid domain names.                                                                                                                                     |
| SOA        | Provides information about the corresponding DNS zone and email address of the administrative contact.                                                                                                                                            |

```bash
dig axfr internal.inlanefreight.htb @10.129.33.24
```

```bash
dnsenum --dnsserver 10.129.33.24 --enum -p 0 -s 0 -o subdomains.txt -f /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt inlanefreight.htb
```

## AXFR example

```bash
dig axfr inlanefreight.htb 10.129.53.194
```

```bash
nslookup -query=axfr inlanefreight.htb 10.129.53.194 | grep "Name:" | cut -d ":" -f2 | while read ZONE; do nslookup -query=axfr $ZONE 10.129.53.194; done > zones.txt
```

```bash
nslookup -query=axfr internal.inlanefreight.htb 10.129.53.194
```
