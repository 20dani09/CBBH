____

https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/

```bash
curl -X 'POST' \ 'http://83.136.254.37:40649/api/v1/authentication/customers/passwords/resets/sms-otps' \ -H 'accept: application/json' \ -H 'Content-Type: application/json' \ -d '{ "Email": "htbpentester8@pentestercompany.com" }'
```

The SMS provider we are working with charges us a significant amount per message. We need to request a discount from them; otherwise, our revenues will decrease.

Use another customer's e-mail address and make the request multiple times 