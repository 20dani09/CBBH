___
# massDNS

https://github.com/blechschmidt/massdns

```bash
subfinder -d spotify.com --silent -all -o spotify
```

```bash
massdns -r resolvers.txt -A spotify -o J > test.txt
```

# Brute Force

```bash
suffledns -a domain.com -w dns.txt -r resolvers.txt -mode bruteforce -m massdns --silent
```

https://github.com/trickest/resolvers

https://github.com/proabiral/Fresh-Resolvers

```bash
suffledns -a domain.com -w dns.txt -r resolvers.txt -mode bruteforce -m massdns --silent | httpx -title --silent
```

# DNSGen

https://github.com/AlephNullSK/dnsgen

```bash
cat domains.txt | dnsgen - | massdns -r resolvers.txt -t A -o J --flush 2>/dev/null
```