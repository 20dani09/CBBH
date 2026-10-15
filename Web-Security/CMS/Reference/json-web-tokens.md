_____

https://jwt.io/


```bash
curl -X POST http://$IP:3000/api/user/login \
-H "Content-Type: application/json" \
-d '{
  "email": "dani@test.com",
  "password": "dani1234"
}'
```

response:

```jwt
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NjQzOTNhZTJhYTA4NzA0N2I2MWE3ZGYiLCJuYW1lIjoiZGFuaXJpbyIsImVtYWlsIjoiZGFuaUB0ZXN0LmNvbSIsImlhdCI6MTcxNTcwNDc4MX0.fiYKazEEsreSFe9hc9Xk2pC-EEUmBOoVj6886bw_5EY
```

![Captura](../../../assets/images/reference/6b9c9da7b527f2a03e52.png)

Change the name and add the secret token 

![Captura](../../../assets/images/reference/45ec3188d0543f88725f.png)
