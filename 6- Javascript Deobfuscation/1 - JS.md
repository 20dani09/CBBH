___

# Deobfuscate
```js
eval(function (p, a, c, k, e, d) { e = function (c) { return c.toString(36) }; if (!''.replace(/^/, String)) { while (c--) { d[c.toString(a)] = k[c] || c.toString(a) } k = [function (e) { return d[e] }]; e = function () { return '\\w+' }; c = 1 }; while (c--) { if (k[c]) { p = p.replace(new RegExp('\\b' + e(c) + '\\b', 'g'), k[c]) } } return p }('g 4(){0 5="6{7!}";0 1=8 a();0 2="/9.c";1.d("e",2,f);1.b(3)}', 17, 17, 'var|xhr|url|null|generateSerial|flag|HTB|1_4m_7h3_53r14l_g3n3r470r|new|serial|XMLHttpRequest|send|php|open|POST|true|function'.split('|'), 0, {}))
```


```js
function generateSerial() {
    var flag = "HTB{1_4m_7h3_53r14l_g3n3r470r!}";
    var xhr = new XMLHttpRequest();
    var url = "/serial.php";
    xhr.open("POST", url, true);
    xhr.send(null);
}
```

https://matthewfl.com/unPacker.html

```bash
curl -X POST http://94.237.59.166:46802/serial.php
```

```bash
echo "N2gxNV8xNV9hX3MzY3IzN19tMzU1NGcz" | base64 -d
```

```bash
curl -X POST http://94.237.59.166:46802/serial.php -d 'serial=7h15_15_a_s3cr37_m3554g3'
```

![[Pasted image 20240927165928.png]]



