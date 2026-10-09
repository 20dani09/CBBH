# Oracle: cliente y consulta de versión

| Comando | Descripción |
| --- | --- |
| `sqlplus <user>/<pass>@<FQDN/IP>/<db>`                                                                               | Log in to the Oracle database.                                                                          |

```text
nmap --script "oracle-tns-version" -p 1521 -T4 -sV $IP
msf> use auxiliary/scanner/oracle/tnslsnr_version
#apt install tnscmd10g
tnscmd10g version -p 1521 -h <IP>
```

## Consultas de SQLplus

```text
SQL> select table_name from all_tables;
SQL> select * from user_role_privs;
```

## Biblioteca del cliente

```bash
sudo sh -c "echo /usr/lib/oracle/12.2/client64/lib > /etc/ld.so.conf.d/oracle-instantclient.conf";sudo ldconfig
```

## Relacionado

- [MySQL](mysql.md)
- [MSSQL](mssql-client.md)
