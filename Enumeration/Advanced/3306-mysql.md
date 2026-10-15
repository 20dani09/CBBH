# 3306 MySQL

***

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

```bash
sudo nmap $IP -sCV -p3306 --script mysql\*
```

https://dev.mysql.com/doc/refman/8.0/en/system-schema.html#:\~:text=The%20mysql%20schema%20is%20the,used%20for%20other%20operational%20purposes
