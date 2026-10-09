# Linux: procesos, versión y permisos

| Comando | Descripción |
| --- | --- |
|  `ps aux \| grep root`                                                              | See processes running as root                         |
| `ps au`                                                                             | See processes associated with terminals, including those of other users                                   |
| `ls /home`                                                                          | View user home directories                            |
| `ls -la /etc/cron.daily`                                                            | Check for daily Cron jobs                             |
| `lsblk`                                                                             | Check for unmounted file systems/drives               |
| `find / -path /proc -prune -o -type d -perm -o+w 2>/dev/null`                       | Find world-writeable directories                      |
| `find / -path /proc -prune -o -type f -perm -o+w 2>/dev/null`                       | Find world-writeable files                            |
| `uname -a`                                                                          | Check the Kernel versiion                             |
| `cat /etc/lsb-release`                                                              | Check the OS version                                  |
| `screen -v`                                                                         | Check the installed version of `Screen`               |
| `./pspy64 -pf -i 1000`                                                              | View running processes with `pspy`                    |
| `find / -user root -perm -4000 -exec ls -ldb {} \; 2>/dev/null`                     | Find binaries with the SUID bit set                   |
| `find / -user root -perm -6000 -exec ls -ldb {} \; 2>/dev/null`                     | Find root-owned binaries with both SUID and SGID bits set                 |
| `echo $PATH`                                                                        | Check the current user's PATH variable contents       |
| `ldd /bin/ls`                                                                       | View the shared objects required by a binary          |
| `readelf -d payroll \| grep PATH`                                                   | Check the RUNPATH of a binary                         |
| `./lynis audit system`                                                              | Perform a system audit with `Lynis`                   |

## Relacionado

- [Procesos y procfs](process-enumeration.md)
- [Permisos y enlaces simbólicos](symlink-permissions.md)
- [Herramientas de revisión](../Resources/system-audit-tools.md)

## Conexiones y un servicio local

```bash
netstat -nat
```

To take an initial look,
```bash
curl localhost:8000
```

## Consulta de capabilities

```bash
getcap -r / 2>/dev/null
```

## Rutas de importación de Python

When a Python script calls `import`, it has a series of paths it checks for the module. I can see this with the `sys` module:

```bash
python3 -c "import sys; print('\n'.join(sys.path))"
```

```bash
echo $PYTHONPATH
```

## Permisos y cambio autorizado de usuario con sudo

```bash
sudo -l

User ---- may run the following commands on ----:
	(root) NOPASSWD: /usr/bin/perl
```

## Change user

```bash
sudo -u user -i
```

## Consulta de archivos con SUID

```bash
find \ -perm -4000 2>/dev/null
```

```bash
find / -type f -perm /4000 2>/dev/null | grep -vE "snap|lib"
```

El primer ejemplo de `find` tiene un error de escapado y no apunta a `/`; se conserva como referencia incompleta. El segundo ejemplo sí recorre `/`.

## Perfiles de AppArmor

Apparmor is a way to define access controls much more granularly to various binaries in Linux. There are a series of binary-specific profiles in `/etc/apparmor.d`

## Consulta del journal

```bash
sudo journalctl
```

## Indicios observados en un contenedor

`ifconfig` shows an IP of 172.19.0.2 on eth0.

There’s a `.dockerenv` file in the filesystem root

## Interfaces, rutas y conexiones

| Comando | Descripción |
| --- | --- |
| `ifconfig`                                                                                                                                                                                                         | Linux-based command that displays all current network configurations of a system.                                                                                                                                                                                       |
| `netstat -r`                                                                                                                                                                                                       | Command used to display the routing table for all IPv4-based protocols.                                                                                                                                                                                                 |
| `netstat -antp \| grep 1234`                                                                                                                                                                                       | Netstat option used to display network connections associated with a tunnel created. Using `grep` to filter based on local port `1234` .                                                                                                                                |
| `netstat -antp`                                                                                                                                                                                                    | Used to display all (`-a`) active network connections with associated process IDs. `-t` displays only TCP connections.`-n` displays only numerical addresses. `-p` displays process IDs associated with each displayed connection.                                      |
