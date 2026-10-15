___

https://jwt.io/

https://github.com/wallarm/jwt-secrets/blob/master/jwt.secrets.list
# JWT authentication bypass via unverified signature

![Captura](../../../../assets/images/reference/00b7076f9ed2a2a568c1.png)

# JWT authentication bypass via flawed signature verification

![Captura](../../../../assets/images/reference/302adcc2c0d8cf2ef6a1.png)

# JWT authentication bypass via weak signing key


```bash
hashcat -m 16500 -a 0 eyJraWQiOiI4ZjMyMTg4Mi1iM2ViLTRlYjItYTg0ZS05YTYyMGMzOTc5MjAiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTcyNTk4NDIwNSwic3ViIjoid2llbmVyIn0.r2jYw6UNai3aiU23kDltRmrTu_Epoysi-xv4Su7HnBM /usr/share/wordlists/rockyou.txt
```
![Captura](../../../../assets/images/reference/ebf4e18c7428e12bef04.png)

# JWT authentication bypass via jwk header injection

- Go to JWT Editor Keys - New RSA Key - Generate  
- Get Request with JWT token - Repeater - JSON Web Token tab - Attack (at the bottom) 
- Embedded JWK - Select your previously generated key - OK

# JWT authentication bypass via jku header injection

- Go to your exploit server and paste the next payload in Body:

```
{
    "keys": [

    ]
}
```
- JWT Editor Keys - New RSA Key - Generate - right-click on key - Copy Public Key as JWK  
- In "keys" section paste your previously copied JWK:

```
{
    "keys": [
        {
            "kty": "RSA",
            "e": "AQAB",
            "kid": "893d8f0b-061f-42c2-a4aa-5056e12b8ae7",
            "n": "yy1wpYmffgXBxhAUJzHHocCuJolwDqql75ZWuCQ_cb33K2vh9mk6GPM9gNN4Y_qTVX67WhsN3JvaFYw"
        }
    ]
}
```

- Back to our JWT, replace the current value of the kid parameter with the kid of the JWK that you uploaded to the exploit server.  
 - Add a new jku parameter to the header of the JWT. Set its value to the URL of your JWK Set on the exploit server.  
- Change "sub" to administrator  
 - Click "Sign" at the bottom of JSON Web Token tab in repeater and select your previously generated key

# JWT authentication bypass via kid header path traversal

- JWT Editor Keys - New Symmetric Key - Generate - replace the value of "k" parameter to AA== - OK  
- Back to our JWT, replace "kid" parameter with ../../../../../dev/null  
- Change "sub" to administrator  
- Click "Sign" at the bottom of JSON Web Token tab in repeater and select your previously generated key
