# 80 - HTTP

```bash
whatweb http://$IP
```

## Gobuster

```bash
gobuster dir -u http://$IP -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 200 -b 403,404 -x php,html,txt
```

```bash
gobuster vhost -v -u http://$IP -w /usr/share/secLists/Discovery/DNS/subdomains-top1million-5000.txt -t 20 | grep -v "403"
```

## Ffuf

| **Command**                                                                                                                                                     | **Description**          |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| `ffuf -h`                                                                                                                                                       | ffuf help                |
| `ffuf -w wordlist.txt:FUZZ -u http://SERVER_IP:PORT/FUZZ`                                                                                                       | Directory Fuzzing        |
| `ffuf -w wordlist.txt:FUZZ -u http://SERVER_IP:PORT/indexFUZZ`                                                                                                  | Extension Fuzzing        |
| `ffuf -w wordlist.txt:FUZZ -u http://SERVER_IP:PORT/blog/FUZZ.php`                                                                                              | Page Fuzzing             |
| `ffuf -w wordlist.txt:FUZZ -u http://SERVER_IP:PORT/FUZZ -recursion -recursion-depth 1 -e .php -v`                                                              | Recursive Fuzzing        |
| `ffuf -w wordlist.txt:FUZZ -u https://FUZZ.hackthebox.eu/`                                                                                                      | Sub-domain Fuzzing       |
| `ffuf -w wordlist.txt:FUZZ -u http://academy.htb:PORT/ -H 'Host: FUZZ.academy.htb' -fs xxx`                                                                     | VHost Fuzzing            |
| `ffuf -w wordlist.txt:FUZZ -u http://admin.academy.htb:PORT/admin/admin.php?FUZZ=key -fs xxx`                                                                   | Parameter Fuzzing - GET  |
| `ffuf -w wordlist.txt:FUZZ -u http://admin.academy.htb:PORT/admin/admin.php -X POST -d 'FUZZ=key' -H 'Content-Type: application/x-www-form-urlencoded' -fs xxx` | Parameter Fuzzing - POST |
| `ffuf -w ids.txt:FUZZ -u http://admin.academy.htb:PORT/admin/admin.php -X POST -d 'id=FUZZ' -H 'Content-Type: application/x-www-form-urlencoded' -fs xxx`       | Value Fuzzing            |

### Wordlists

| **Command**                                                              | **Description**         |
| ------------------------------------------------------------------------ | ----------------------- |
| `/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt` | Directory/Page Wordlist |
| `/usr/share/seclists/Discovery/Web-Content/web-extensions.txt`           | Extensions Wordlist     |
| `/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt`      | Domain Wordlist         |
| `/usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt`     | Parameters Wordlist     |

## Brute-force

| **Command**                                                                                                                            | **Description**                                     |
| -------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| `hydra -h`                                                                                                                             | hydra help                                          |
| `hydra -C wordlist.txt SERVER_IP -s PORT http-get /`                                                                                   | Basic Auth Brute Force - Combined Wordlist          |
| `hydra -L wordlist.txt -P wordlist.txt -u -f SERVER_IP -s PORT http-get /`                                                             | Basic Auth Brute Force - User/Pass Wordlists        |
| `hydra -l admin -P wordlist.txt -f SERVER_IP -s PORT http-post-form "/login.php:username=^USER^&password=^PASS^:F=<form name='login'"` | Login Form Brute Force - Static User, Pass Wordlist |
| `hydra -L bill.txt -P william.txt -u -f ssh://SERVER_IP:PORT -t 4`                                                                     | SSH Brute Force - User/Pass Wordlists               |
| `hydra -l m.gates -P rockyou-10.txt ftp://127.0.0.1`                                                                                   | FTP Brute Force - Static User, Pass Wordlist        |

### Wordlists

| **Command**                                                                       | **Description**            |
| --------------------------------------------------------------------------------- | -------------------------- |
| `/usr/share/seclists/Passwords/Default-Credentials/ftp-betterdefaultpasslist.txt` | Default Passwords Wordlist |
| `/usr/share/seclists/Passwords/Leaked-Databases/rockyou.txt`                      | Common Passwords Wordlist  |
| `/usr/share/seclists/Usernames/Names/names.txt`                                   | Common Names Wordlist      |

### Misc

| **Command**                                     | **Description**                        |
| ----------------------------------------------- | -------------------------------------- |
| `cupp -i`                                       | Creating Custom Password Wordlist      |
| `sed -ri '/^.{,7}$/d' william.txt`              | Remove Passwords Shorter Than 8        |
| ``sed -ri '/[!-/:-@\[-`\{-~]+/!d' william.txt`` | Remove Passwords With No Special Chars |
| `sed -ri '/[0-9]+/!d' william.txt`              | Remove Passwords With No Numbers       |
| `./username-anarchy Bill Gates > bill.txt`      | Generate Usernames List                |
| `ssh b.gates@SERVER_IP -p PORT`                 | SSH to Server                          |
| `ftp 127.0.0.1`                                 | FTP to Server                          |
| `su - user`                                     | Switch to User                         |
