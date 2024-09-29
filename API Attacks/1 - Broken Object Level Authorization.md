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

