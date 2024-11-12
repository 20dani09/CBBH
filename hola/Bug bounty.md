___

```bash
subfinder -d domain.com -o subdomains
cat subdomains | httpx -silent -o activesubdomains
```