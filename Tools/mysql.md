# MySQL: conexión y consultas

| **Command**                                 | **Description**            |
| ------------------------------------------- | -------------------------- |
| `mysql -u <user> -p<password> -h <FQDN/IP>` | Login to the MySQL server. |

| Command                                            | Description                                                          |
| -------------------------------------------------- | -------------------------------------------------------------------- |
| `mysql -u <user> -p<password> -h <IP>`             | Connect to the MySQL server. There should not be a space after `-p`. |
| `show databases;`                                  | Show all databases.                                                  |
| `use <database>;`                                  | Select one of the existing databases.                                |
| `show tables;`                                     | Show all available tables in the selected database.                  |
| `show columns from <table>;`                       | Show all columns in the selected table.                              |
| `select * from <table>;`                           | Show everything in the desired table.                                |
| `select * from <table> where <column>="<string>";` | Search for the specified string in the desired table.                |

## Cliente local

```bash
mysql -u root -p
```

## Selección de una base de datos

```sql
show databases;
use moodle;
```

`moodle` es el nombre de la base de datos del ejemplo.

## Relacionado

- [MongoDB](mongodb.md)
- [Cliente MSSQL](mssql-client.md)
