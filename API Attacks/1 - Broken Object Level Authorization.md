___

```bash
curl -X 'POST' \  
 'http://94.237.53.113:38585/api/v1/authentication/suppliers/sign-in' \  
 -H 'accept: application/json' \  
 -H 'Content-Type: application/json' \  
 -d '{  
 "Email": "htbpentester1@pentestercompany.com",  
 "Password": "HTBPentester1"  
}'
```

```json
{  
 "jwt": "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6Imh0YnBlbnRlc3RlcjFAcGVudGVzdGVyY29tcGFueS5jb20iLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJTdXBwbGllckNvbXBhbmllc19HZXRZZWFybHlSZXBvcnRCeUlEIiwiZXhwIjoxNzI3NjMzMjQ1LCJpc3MiOiJodHRwOi8vYXBpLmlubGFuZWZyZWlnaHQuaHRiIiwiYXVkIjoiaHR0cDovL2FwaS5pbmxhbmVmcmVpZ2h0Lmh0YiJ9.naKK8qUo9fvcFciW-l7GfNR1PCjJpwrIheA5nklZy0BnV8l_zeppkpzYYnhxlEB1L1bcza12rJ9llLjx04qFsA"  
}
```


```bash
curl -X 'GET' 'http://94.237.53.113:38585/api/v1/suppliers/current-user' -H 'accept: application/json' -H 'Authorization: Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6Imh0YnBlbnRlc3RlcjFAcGVudGVzdGVyY29tcGFueS5jb20iLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJTdXBwbGllckNvbXBhbmllc19HZXRZZWFybHlSZXBvcnRCeUlEIiwiZXhwIjoxNzI3NjMzMjQ1LCJpc3MiOiJodHRwOi8vYXBpLmlubGFuZWZyZWlnaHQuaHRiIiwiYXVkIjoiaHR0cDovL2FwaS5pbmxhbmVmcmVpZ2h0Lmh0YiJ9.naKK8qUo9fvcFciW-l7GfNR1PCjJpwrIheA5nklZy0BnV8l_zeppkpzYYnhxlEB1L1bcza12rJ9llLjx04qFsA'
```

```json
{  
 "supplier": {  
   "id": "c538adbb-2c74-447e-8029-54ecad6c5464",  
   "companyID": "b75a7c76-e149-4ca7-9c55-d9fc4ffa87be",  
   "name": "HTBPentester1",  
   "email": "htbpentester1@pentestercompany.com",  
   "phoneNumber": "+44 9999 999991"  
 }  
}
```

```bash
curl -X 'GET' 'http://94.237.53.113:38585/api/v1/roles/current-user' -H 'accept: application/json' -H 'Authorization: Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6Imh0YnBlbnRlc3RlcjFAcGVudGVzdGVyY29tcGFueS5jb20iLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJTdXBwbGllckNvbXBhbmllc19HZXRZZWFybHlSZXBvcnRCeUlEIiwiZXhwIjoxNzI3NjMzMjQ1LCJpc3MiOiJodHRwOi8vYXBpLmlubGFuZWZyZWlnaHQuaHRiIiwiYXVkIjoiaHR0cDovL2FwaS5pbmxhbmVmcmVpZ2h0Lmh0YiJ9.naKK8qUo9fvcFciW-l7GfNR1PCjJpwrIheA5nklZy0BnV8l_zeppkpzYYnhxlEB1L1bcza12rJ9llLjx04qFsA'
```

```json
{  
 "roles": [  
   "SupplierCompanies_GetYearlyReportByID"  
 ]  
}
```

```bash
curl -X 'GET' 'http://94.237.53.113:38585/api/v1/supplier-companies/yearly-reports/1' -H 'accept: application/json' -H 'Authorization: Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6Imh0YnBlbnRlc3RlcjFAcGVudGVzdGVyY29tcGFueS5jb20iLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJTdXBwbGllckNvbXBhbmllc19HZXRZZWFybHlSZXBvcnRCeUlEIiwiZXhwIjoxNzI3NjMzMjQ1LCJpc3MiOiJodHRwOi8vYXBpLmlubGFuZWZyZWlnaHQuaHRiIiwiYXVkIjoiaHR0cDovL2FwaS5pbmxhbmVmcmVpZ2h0Lmh0YiJ9.naKK8qUo9fvcFciW-l7GfNR1PCjJpwrIheA5nklZy0BnV8l_zeppkpzYYnhxlEB1L1bcza12rJ9llLjx04qFsA'
```

```json
{  
 "supplierCompanyYearlyReport": {  
   "id": 1,  
   "companyID": "f9e58492-b594-4d82-a4de-16e4f230fce1",  
   "year": 2020,  
   "revenue": 794425112,  
   "commentsFromCLevel": "Superb work! The Board is over the moon! All employees will enjoy a dream vacation!"  
 }  
}
```

![[Pasted image 20240929200616.png]]
