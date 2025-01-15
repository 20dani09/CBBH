___

# Parameter pollution

```bash
curl -X POST https://www.projectbaseline.com/studies/rheumatoid-arthritis-galvani/contact/ -H "Referer: https://www.twitch.tv/"
```

![[Pasted image 20250115173954.png]]

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>POST Request</title>
</head>
<body>
  <button onclick="sendPostRequest()">Send POST Request</button>

  <script>
    function sendPostRequest() {
      fetch('https://www.projectbaseline.com/studies/rheumatoid-arthritis-galvani/contact/', {
        method: 'POST',
        headers: {
          'Referer': 'https://www.twitch.tv/',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({}) // If you need to send any data in the body
      })
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error('Error:', error));
    }
  </script>
</body>
</html>
```

![[Pasted image 20250115174453.png]]

