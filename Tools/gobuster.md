# Gobuster: directorios y hosts virtuales

```bash
gobuster dir -u http://$IP -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 200 -b 403,404 -x php,html,txt
```

```bash
gobuster vhost -v -u http://$IP -w /usr/share/secLists/Discovery/DNS/subdomains-top1million-5000.txt -t 20 | grep -v "403"
```

## Relacionado

- [Subdominios](../Enumeration/Reconnaissance/subdomains.md)
- [Hosts virtuales](../Enumeration/Reconnaissance/virtual-hosts.md)
