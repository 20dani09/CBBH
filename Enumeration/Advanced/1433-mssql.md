# 1433 - MSSQL

***

| **Command**                                     | **Description**                                          |
| ----------------------------------------------- | -------------------------------------------------------- |
| `mssqlclient.py <user>@<FQDN/IP> -windows-auth` | Log in to the MSSQL server using Windows authentication. |

| Default System Database | Description                                                                                                                                                                                            |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| master                  | Tracks all system information for an SQL server instance                                                                                                                                               |
| model                   | Template database that acts as a structure for every new database created. Any setting changed in the model database will be reflected in any new database created after changes to the model database |
| msdb                    | The SQL Server Agent uses this database to schedule jobs & alerts                                                                                                                                      |
| tempdb                  | Stores temporary objects                                                                                                                                                                               |
| resource                | Read-only database containing system objects included with SQL server                                                                                                                                  |

When an admin initially installs and configures MSSQL to be network accessible, the SQL service will likely run as `NT SERVICE\MSSQLSERVER`.

```bash
sudo nmap --script ms-sql-info,ms-sql-empty-password,ms-sql-xp-cmdshell,ms-sql-config,ms-sql-ntlm-info,ms-sql-tables,ms-sql-hasdbaccess,ms-sql-dac,ms-sql-dump-hashes --script-args mssql.instance-port=1433,mssql.username=sa,mssql.password=,mssql.instance-name=MSSQLSERVER -sV -p 1433 $IP
```

```bash
msf6 auxiliary(scanner/mssql/mssql_ping)
```

```bash
impacket-mssqlclient backdoor@10.129.99.209 -windows-auth
enum db

select name from sys.databases
SELECT * FROM <databaseName>.INFORMATION_SCHEMA.TABLES;
```

#### Example

```sql
select name from sys.databases
SELECT * FROM accounts.INFORMATION_SCHEMA.TABLES;
```

| table\_catalog | table\_schema | table\_name | table\_type |
| -------------- | ------------- | ----------- | ----------- |
| accounts       | dbo           | devsacc     | BASE TABLE  |

```sql
select * from accounts.dbo.devsacc where name = 'HTB'
```

https://learn.microsoft.com/en-us/sql/relational-databases/views/modify-data-through-a-view?view=sql-server-ver16
