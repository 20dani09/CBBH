___
https://github.com/blechschmidt/massdns

```bash
subfinder -d spotify.com --silent -all -o spotify
```

```bash
massdns -r resolvers.txt -A spotify -o J > test.txt
```

# Brute Force

```bash
suffledns -a domain.com -w dns.txt -r resolvers.txt -mode bruteforce -
```