___

# Dangers of PostMessage(XSS)
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

![[Pasted image 20241129164644.png]]


