# Firewall and IDS IPS Evasion

***

When a port is shown as filtered, it can have several reasons. In most cases, firewalls have certain rules set to handle specific connections. The packets can either be dropped, or rejected. When a packet gets dropped, Nmap receives no response from our target, and by default, the retry rate (--max-retries) is set to 1. This means Nmap will resend the request to the target port to determine if the previous packet was not accidentally mishandled.

## Firewall Rules

_Dropped_ packets are ignored, and no response is returned from the host. This is different for _rejected_ packets that are returned with an RST flag. These packets contain different types of ICMP error codes or contain nothing at all.

Such errors can be:

* Net Unreachable
* Net Prohibited
* Host Unreachable
* Host Prohibited
* Port Unreachable
* Proto Unreachable

Nmap's _TCP ACK scan (-sA)_ method is much harder to filter for firewalls and IDS/IPS systems than regular SYN (-sS) or Connect scans (sT) because they only send a TCP packet with only the ACK flag. When a port is closed or open, the host must respond with an RST flag. Unlike outgoing connections, all connection attempts (with the SYN flag) from external networks are usually blocked by firewalls. However, the packets with the ACK flag are often passed by the firewall because the firewall cannot determine whether the connection was first established from the external network or the internal network.

## IDS/IPS

Unlike firewalls and their rules, the detection of IDS/IPS systems is much more difficult because these are passive traffic monitoring systems. _IDS systems_ examine all connections between hosts. If the IDS finds packets containing the defined contents or specifications, the administrator is notified and takes appropriate action in the worst case.

_IPS systems_ take measures configured by the administrator independently to prevent potential attacks automatically. It is essential to know that IDS and IPS are different applications and that IPS serves as a complement to IDS.

Several virtual private servers (_VPS_) with different IP addresses are recommended to determine whether such systems are on the target network during a penetration test. If the administrator detects such a potential attack on the target network, the first step is to block the IP address from which the potential attack comes. As a result, we will no longer be able to access the network using that IP address, and our Internet Service Provider (_ISP_) will be contacted and blocked from all access to the Internet.

* _IDS system_s alone are usually there to help administrators detect potential attacks on their network. They can then decide how to handle such connections. We can trigger certain security measures from an administrator, for example, by aggressively scanning a single port and its service. Based on whether specific security measures are taken, we can detect if the network has some monitoring applications or not.
* One method to determine whether such _IPS system_ is present in the target network is to scan from a single host (_VPS_). If at any time this host is blocked and has no access to the target network, we know that the administrator has taken some security measures. Accordingly, we can continue our penetration test with another _VPS_.

### Decoys

There are cases in which administrators block specific subnets from different regions in principle. This prevents any access to the target network. Another example is when IPS should block us. For this reason, the Decoy scanning method (_-D_) is the right choice. With this method, Nmap generates various random IP addresses inserted into the IP header to disguise the origin of the packet sent. With this method, we can generate random (_RND_) a specific number (for example: 5) of IP addresses separated by a colon (:). Our real IP address is then randomly placed between the generated IP addresses. In the next example, our real IP address is therefore placed in the second position. Another critical point is that the decoys must be alive. Otherwise, the service on the target may be unreachable due to SYN-flooding security mechanisms.

```bash
sudo nmap 10.129.2.28 -p 80 -sS -Pn -n --disable-arp-ping --packet-trace -D RND:5
```

| Scanning Options   | Description                                      |
| ------------------ | ------------------------------------------------ |
| $IP                | Scans the specified target.                      |
| -p 80              | Scans only the specified ports.                  |
| -sS                | Performs SYN scan on specified ports.            |
| -Pn                | Disables ICMP Echo requests.                     |
| -n                 | Disables DNS resolution.                         |
| --disable-arp-ping | Disables ARP ping.                               |
| --packet-trace     | Shows all packets sent and received.             |
| -D RND:5           | Generates five random IP addresses that indicate |
|                    | the source IP of the connection.                 |

#### Scan by Using Different Source IP

```bash
sudo nmap $IP -n -Pn -p 445 -O -S $newIP 
```

### DNS Proxying

By default, _Nmap_ performs a reverse DNS resolution unless otherwise specified to find more important information about our target. These DNS queries are also passed in most cases because the given web server is supposed to be found and visited. The DNS queries are made over the _UDP port 53_. The _TCP port 5_3 was previously only used for the so-called "Zone transfers" between the DNS servers or data transfer larger than 512 bytes. More and more, this is changing due to IPv6 and DNSSEC expansions. These changes cause many DNS requests to be made via TCP port 53.

However, _Nmap_ still gives us a way to specify DNS servers ourselves (_--dns-server ns,ns_). This method could be fundamental to us if we are in a demilitarized zone (_DMZ_). The company's DNS servers are usually more trusted than those from the Internet. So, for example, we could use them to interact with the hosts of the internal network. As another example, we can use _TCP port 53_ as a source port (--source-port) for our scans. If the administrator uses the firewall to control this port and does not filter IDS/IPS properly, our TCP packets will be trusted and passed through.

```bash
sudo nmap $IP -p50000 -sS -Pn -n --disable-arp-ping --packet-trace --source-port 53
```

Now that we have found out that the firewall accepts _TCP port 53_, it is very likely that IDS/IPS filters might also be configured much weaker than others. We can test this by trying to connect to this port by using _Netcat_.

```bash
nc -nv --source-port 53 $IP port
nc -nv -p 53 $IP port
```

#### DNS version

```bash
sudo nmap -sSU -p 53 --script dns-nsid $IP
```
