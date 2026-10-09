# MongoDB: bases de datos, colecciones y BSON

Ejemplos para el cliente `mongo`.

MongoDB is _an open source NoSQL database management program_. NoSQL (Not only SQL) is used as an alternative to traditional relational databases.

- Port: 27017

```console
mongo
> show dbs
> use blog
> show collections
> db.users.find()
```

Another way to get to this same information would be with `mongodump`

```bash
bsondump dump/blog/users.bson
```
