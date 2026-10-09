# Procesos locales y procfs

Consulta de procesos locales y sus líneas de ejecución mediante procfs.

I’d like to get a list of the processes running on the system. I can take a look at `/proc`, which has a directory for each process id (pid) currently running

```bash
ls /proc
```

There’s also the `self` folder, which is a symbolic link to the pid of the current process.

```bash
ls -l /proc/self
```

In each numbered folder, the `cmdline` file has the command line user to run the process

```bash
cat /proc/self/cmdline | xxd
```

## Observar cambios en los procesos

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

## pspy

https://github.com/DominicBreuker/pspy

## Cronjobs

```bash
crontab -l
```

## Relacionado

- [Permisos y enlaces simbólicos](symlink-permissions.md)
