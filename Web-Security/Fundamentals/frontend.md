# HTML, CSS y JavaScript



## HTML

```html
<!DOCTYPE html>
<html>
    <head>
        <title>Page Title</title>
    </head>
    <body>
        <h1>A Heading</h1>
        <p>A Paragraph</p>
    </body>
</html>
```

The `<head>` element usually contains elements that are not directly printed on the page, like the page title, while all main page elements are located under `<body>`. Other important elements include the `<style>`, which holds the page's CSS code, and the `<script>`, which holds the JS code of the page, as we will see in the next section.

## CSS

```css
body {
  background-color: black;
}

h1 {
  color: white;
  text-align: center;
}

p {
  font-family: helvetica;
  font-size: 10px;
}
```

At a fundamental level, CSS is used to define the style of each class or type of HTML elements (i.e., `body` or `h1`), such that any element within that page would be represented as defined in the CSS file. This could include the font family, font size, background color, text color and alignment, and more.

## Javascript

[JavaScript](https://en.wikipedia.org/wiki/JavaScript) is one of the most used languages in the world. It is mostly used for web development and mobile development. `JavaScript` is usually used on the front end of an application to be executed within a browser. Still, there are implementations of back end JavaScript used to develop entire web applications, like [NodeJS](https://nodejs.org/en/about/).

While `HTML` and `CSS` are mainly in charge of how a web page looks, `JavaScript` is usually used to control any functionality that the front end web page requires. Without `JavaScript`, a web page would be mostly static and would not have much functionality or interactive elements.


```html
<script type="text/javascript">
..JavaScript code..
</script>
```

```javascript
document.getElementById("button1").innerHTML = "Changed Text!";
```

Some of the most common front end `JavaScript` frameworks are:

- [Angular](https://www.w3schools.com/angular/angular_intro.asp)
- [React](https://www.w3schools.com/react/react_intro.asp)
- [Vue](https://www.w3schools.com/whatis/whatis_vue.asp)
- [jQuery](https://www.w3schools.com/jquery/)

## Procedencia

| Repositorio | Archivo original | Commit de origen |
| --- | --- | --- |
| CBBH | 2- Introduction to Web Applications/2 - Front End Components/1 - HTML.md | 284a0a42d23a00f2b47b7460371a517a14cb6261 |
| CBBH | 2- Introduction to Web Applications/2 - Front End Components/2 - CSS.md | 284a0a42d23a00f2b47b7460371a517a14cb6261 |
| CBBH | 2- Introduction to Web Applications/2 - Front End Components/3 - Javascript.md | 284a0a42d23a00f2b47b7460371a517a14cb6261 |

[Índice de categoría](../README.md) · [Inicio](../../README.md)
