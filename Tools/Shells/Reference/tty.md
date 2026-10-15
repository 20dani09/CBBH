
***

```shell
script /dev/null -c bash
```

**Ctrl+Z**

```shell
stty raw -echo;fg
reset xterm
```

```shell
export TERM=xterm
export SHELL=bash
```

```bash
Error opening terminal: xterm-kitty.
export TERM=xterm
```

```shell
python -c 'import pty;pty.spawn("/bin/bash")'
```


# Python 

```bash
python3 -c 'import pty;pty.spawn("bash")'
```
