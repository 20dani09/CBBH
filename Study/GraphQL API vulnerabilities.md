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

