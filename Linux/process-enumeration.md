# Procesos locales y procfs

Se ha extraído la consulta local de /proc. El bucle que utiliza una vulnerabilidad remota no se ha importado.

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

## Procedencia

| Repositorio | Archivo original | Commit de origen |
| --- | --- | --- |
| pentestNotes | Linux/Process Enumeration.md | ea46064dea8893ed6d54216151ae1bb0ef3661ba |

[Índice de categoría](README.md) · [Inicio](../README.md)
