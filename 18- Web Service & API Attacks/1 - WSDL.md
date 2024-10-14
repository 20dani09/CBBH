___

WSDL stands for Web Service Description Language. WSDL is an XML-based file exposed by web services that informs clients of the provided services/methods, including where they reside and the method-calling convention.

```bash
curl http://10.129.202.133:3002/wsdl
```

The response is empty. 

```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt -u  http://10.129.202.133:3002/wsdl -fs 0 -mc 200
`````