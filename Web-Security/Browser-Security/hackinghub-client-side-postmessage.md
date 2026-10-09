# postMessage (HackingHub)

## Dangers of PostMessage(XSS)
```html
<html>
<head>
    <script>
        let btn = function(){
            msg = {
                'msg'   :   document.getElementById('msg').value
            }
            document.getElementById('frame').contentWindow.postMessage(msg,'*');
        }
    </script>
</head>
<body>
<iframe src="https://pm.nahamseclab.com/four_target" id="frame"></iframe><br>
<input id="msg" value="Hello IFRAME">
<button onclick="btn()">RUN</button>
</body>
</html>
```

```html
    <script>
        window.addEventListener("message",function(event){
            if( event.data.hasOwnProperty('msg') ) {
                document.getElementById('message').innerHTML = event.data.msg;
            }
        });
    </script>
```

![Pasted image 20241129164644.png](../../assets/images/7a462b0c6f9151a428f8.png)

## Protecting PostMessage Origin

```html
	<script>
        window.addEventListener("message",function(event){
            if (event.data.hasOwnProperty('msg')) {
                if( event.origin === 'https://only-from-this-domain.com' ) {
                    document.getElementById('message').innerHTML = event.data.msg;
                }else{
                    alert("You're not allowed to send from here!");
                }
            }
        });
    </script>
```

## Exploiting PostMessage Origin Checks

```html
    <script>
        window.addEventListener("message",function(event){
            if (event.data.hasOwnProperty('msg')) {
                if( /(http:|https:)\/\/([a-z0-9.]{1,}).ctfio.com/.test( event.origin ) ) {
                    document.getElementById('message').innerHTML = event.data.msg;
                }else{
                    alert("You're not allowed to send from here!");
                }
            }
        });
    </script>
```

### Subdomain Regex Bypass
![Pasted image 20241129165328.png](../../assets/images/f47da5b6d45f61a22d24.png)

## PostMessage targetOrigin Exploitation

```html
    <script>
        function auth() {
            let data = {
                'user': {
                    'username': 'adam',
                    'token': '<REDACTED_TOKEN>'
                }
            }
            window.parent.postMessage(data, '*');
        }
    </script>
```

*Captura omitida por posibles datos sensibles.*

### Secure PostMessage targetOrigin

```html
window.parent.postMessage(data, 'https://service.protected.com');
```
