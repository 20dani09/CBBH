____

```html
<script>
		for (var truckID of ["FusionExpress01", "FusionExpress02", "FusionExpress03"]) {
			var xhr = new XMLHttpRequest();
			xhr.open('POST', '/', false);
			xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
			xhr.onreadystatechange = function() {
				if (xhr.readyState === XMLHttpRequest.DONE) {
					var resp = document.getElementById(truckID)
					if (xhr.status === 200) {
						var responseData = xhr.responseText;
						var data = JSON.parse(responseData);

						if (data['error']) {
							resp.innerText = data['error'];
						} else {
							resp.innerText = data['location'];
						}
					} else {
						resp.innerText = "Unable to fetch current truck location!"
					}
				}       
			};
			xhr.send('api=http://truckapi.htb/?id' + encodeURIComponent("=" + truckID));
		}
    </script>
```


