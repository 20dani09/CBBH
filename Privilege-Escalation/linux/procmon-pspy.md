____

```bash
ps -eo command
```


```bash
cd /tmp
touch procmon.sh
chmod +x procmon.sh
```

```bash
#!/bin/bash

old_process=$(ps -eo command)

while true; do 
	new_process=$(ps -eo command)
	diff <(echo "$old_process") <(echo "$new_process") | grep "[\>\<]" | grep -vE "procmon|command|kworker"
	old_process=$new_process
done
```

# pspy

https://github.com/DominicBreuker/pspy

# Cronjobs

```bash
crontab -l
```
