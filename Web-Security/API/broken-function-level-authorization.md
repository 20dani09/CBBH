# Broken Function Level Authorization

```json
{
  "errorMessage": "User does not have any roles assigned"
}
```

![Pasted image 20241001194701.png](../../assets/images/d1c4b7601da2121f2448.png)


```bash
curl -X 'GET' \ 'http://83.136.254.37:40649/api/v1/customers/billing-addresses' \ -H 'accept: application/json' \ -H 'Authorization: Bearer <REDACTED_JWT>'
```

![Pasted image 20241001194859.png](../../assets/images/d0d2616e82ac5b5453ad.png)
