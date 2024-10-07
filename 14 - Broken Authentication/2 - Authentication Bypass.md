___
# Direct Access

This code redirects the user to `/index.php` if the session is not active, i.e., if the user is not authenticated. However, the PHP script does not stop execution, resulting in protected information within the page being sent in the response body:

![[Pasted image 20241007182941.png]]

The entire admin page is contained in the response body. However, if we attempt to access the page in our web browser, the browser follows the redirect and displays the login prompt instead of the protected admin page. We can easily trick the browser into displaying the admin page by intercepting the response and changing the status code from `302` to `200`.

![[Pasted image 20241007183017.png]]

Afterward, forward the request by clicking on `Forward`. Since we intercepted the response, we can now edit it. To force the browser to display the content, we need to change the status code from `302 Found` to `200 OK`:

![[Pasted image 20241007183158.png]]

# Authentication Bypass via Parameter Modification

![[Pasted image 20241007184247.png]]

