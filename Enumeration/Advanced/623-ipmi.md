# 623 IPMI

***

**Default Port**: 623/UDP/TCP (It's usually on UDP but it could also be running on TCP)

| **Command**                                    | **Description**         |
| ---------------------------------------------- | ----------------------- |
| `msf6 auxiliary(scanner/ipmi/ipmi_version)`    | IPMI version detection. |
| `msf6 auxiliary(scanner/ipmi/ipmi_dumphashes)` | Dump IPMI hashes.       |

```bash
sudo nmap -sU --script ipmi-version -p 623
```
