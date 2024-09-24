___

# Relational (SQL)

[Relational](https://en.wikipedia.org/wiki/Relational_database) (SQL) databases store their data in tables, rows, and columns. Each table can have unique keys, which can link tables together and create relationships between tables.

![[Pasted image 20240924170151.png]]

|Type|Description|
|---|---|
|[MySQL](https://en.wikipedia.org/wiki/MySQL)|The most commonly used database around the internet. It is an open-source database and can be used completely free of charge|
|[MSSQL](https://en.wikipedia.org/wiki/Microsoft_SQL_Server)|Microsoft's implementation of a relational database. Widely used with Windows Servers and IIS web servers|
|[Oracle](https://en.wikipedia.org/wiki/Oracle_Database)|A very reliable database for big businesses, and is frequently updated with innovative database solutions to make it faster and more reliable. It can be costly, even for big businesses|
|[PostgreSQL](https://en.wikipedia.org/wiki/PostgreSQL)|Another free and open-source relational database. It is designed to be easily extensible, enabling adding advanced new features without needing a major change to the initial database design|

# Non-relational (NoSQL)

A [non-relational database](https://en.wikipedia.org/wiki/NoSQL) does not use tables, rows, columns, primary keys, relationships, or schemas. Instead, a `NoSQL` database stores data using various storage models, depending on the type of data stored.

There are 4 common storage models for `NoSQL` databases:

- Key-Value
- Document-Based
- Wide-Column
- Graph

![[Pasted image 20240924170234.png]]

|Type|Description|
|---|---|
|[MongoDB](https://en.wikipedia.org/wiki/MongoDB)|The most common `NoSQL` database. It is free and open-source, uses the `Document-Based` model, and stores data in `JSON` objects|
|[ElasticSearch](https://en.wikipedia.org/wiki/Elasticsearch)|Another free and open-source `NoSQL` database. It is optimized for storing and analyzing huge datasets. As its name suggests, searching for data within this database is very fast and efficient|
|[Apache Cassandra](https://en.wikipedia.org/wiki/Apache_Cassandra)|Also free and open-source. It is very scalable and is optimized for gracefully handling faulty values|

# Use in Web Applications

Connect to the database server: 
```php
$conn = new mysqli("localhost", "user", "pass");
```

Create a new database:
```php
$sql = "CREATE DATABASE database1";
$conn->query($sql)
```

Connect to our new database, and start using the `MySQL` database through `MySQL` syntax
```php
$conn = new mysqli("localhost", "user", "pass", "database1");
$query = "select * from table_1";
$result = $conn->query($query);
```

Web applications usually use user-input when retrieving data. For example, when a user uses the search function to search for other users, their search input is passed to the web application, which uses the input to search within the database(s).
```php
$searchInput =  $_POST['findUser'];
$query = "select * from users where name like '%$searchInput%'";
$result = $conn->query($query);
```

Finally, the web application sends the result back to the user:
```php
while($row = $result->fetch_assoc() ){
	echo $row["name"]."<br>";
}
```