# Nmap

> Network Mapper (_Nmap_) is an open-source network analysis and security auditing tool written in C, C++, Python, and Lua. It is designed to scan networks and identify which hosts are available on the network using raw packets, and services and applications, including the name and version, where possible. It can also identify the operating systems and versions of these hosts.

* Host discovery
* Port scanning
* Service enumeration and detection
* OS detection
* Scriptable interaction with the target service

## Open TCP Ports

```bash
nmap -p- --open -sS --min-rate 5000 -v -n -Pn $IP
```

1. **`-p-`**: This option specifies that Nmap should scan all 65535 ports on the target host. The hyphen after `-p` indicates scanning all ports.
2. **`--open`**: This option tells Nmap to show only open ports, i.e., ports that are actively accepting connections.
3. **`-sS`**: This flag enables SYN stealth scanning. It's a common scanning technique used to reduce the chances of being detected by firewalls and intrusion detection systems.
4. **`--min-rate 5000`**: This sets the minimum rate at which Nmap sends packets. In this case, it's set to 5000 packets per second. This can be useful for increasing the speed of the scan.
5. **`-v`**: This enables verbose mode, which provides more detailed output about the scan in the terminal.
6. **`-n`**: This option tells Nmap not to perform DNS resolution on discovered IP addresses. This can speed up the scan as DNS resolution can sometimes cause delays.
7. **`-Pn`**: This option skips host discovery and treats all hosts as online. Normally, Nmap first performs host discovery to identify hosts that are online before scanning them. This option disables that step.
8. **`$IP`**: This is a placeholder for the target IP address. You should replace `$IP` with the actual IP address you want to scan.

## Service Version and Scripts

```bash
nmap -sCV -p$ports $IP
```

* **`-sC`**: This option enables the use of default scripts. Nmap comes with a wide range of scripts that can be used for various purposes, such as version detection, vulnerability scanning, and more. The `-sC` option instructs Nmap to use these default scripts against the target host.
* **`-V`**: This option enables version detection. Nmap will attempt to determine the version of the services running on the open ports. Knowing the version information can be crucial for identifying vulnerabilities associated with specific software versions.

## Scan Network Range

```bash
sudo nmap $IP/24 -sn -oA tnet | grep for | cut -d" " -f5
```

## Scan IP list

```bash
sudo nmap -sn -oA tnet -iL hosts.lst | grep for | cut -d" " -f5
```

## UDP Ports

Some system administrators sometimes forget to filter the UDP ports in addition to the TCP ones. Since UDP is a stateless protocol and does not require a three-way handshake like TCP. We do not receive any acknowledgment. Consequently, the timeout is much longer, making the whole UDP scan (-sU) much slower than the TCP scan (-sS).

```bash
sudo nmap $IP -F -sU
```

## Links:

https://nmap.org/book/man-port-scanning-techniques.html
