# Inventario de red y captura local

| Comando | Descripción |
| --- | --- |
| `nslookup ns1.inlanefreight.com`                                                                    | Used to query the domain name system and discover the IP address to domain name mapping of the target entered from a Linux-based host.                                                                                                                                                                      |
| `sudo tcpdump -i ens224`                                                                            | Used to start capturing network packets on the network interface proceeding the `-i` option a Linux-based host.                                                                                                                                                                                             |
| `fping -asgq 172.16.5.0/23`                                                                         | Performs a ping sweep on the specified network segment from a Linux-based host.                                                                                                                                                                                                                             |
| `sudo nmap -v -A -iL hosts.txt -oN /home/User/Documents/host-enum`                                  | Performs an nmap scan that with OS detection, version detection, script scanning, and traceroute enabled (`-A`) based on a list of hosts (`hosts.txt`) specified in the file proceeding `-iL`. Then outputs the scan results to the file specified after the `-oN`option. Performed from a Linux-based host |

## Relacionado

- [Nmap](../Tools/nmap-options.md)
- [DNS](../Network-Pentesting/Protocols/dns.md)
