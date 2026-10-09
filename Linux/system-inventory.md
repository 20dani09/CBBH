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
