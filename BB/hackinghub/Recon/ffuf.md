___

```bash
ffuf -w content.txt -u https://URL/FUZZ 
```

# Subdomain & VHost

```bash
ffuf -w dns.txt -u https://FUZZ.URL
```

```bash
ffuf -w dns.txt -u https://URL -H "Host: FUZZ.URL"
```

# Passwords

```bash
ffuf -request r.txt -w password.txt
```

# Hidden Development Files

https://github.com/internetwache/GitTools

