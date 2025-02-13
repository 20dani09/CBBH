___
IP=192.168.0.20

express.nyx

# API

```js
function getMusicList() {
    fetch('/api/music/list')
        .then(response => response.json())
        .then(data => {
            console.log('Music genre list:', data);
        })
        .catch(error => {
            console.error('Error fetching the music list:', error);
        });
}

function getMusicSongs() {
    fetch('/api/music/songs')
        .then(response => response.json())
        .then(data => {
            console.log('List of songs:', data);
        })
        .catch(error => {
            console.error('Error fetching the list of songs:', error);
        });
}

function getUsersWithKey() {
    fetch(`/api/users?key=${secretKey}`)
        .then(response => response.json())
        .then(data => {
            console.log('User list (with key):', data);
        })
        .catch(error => {
            console.error('Error fetching the user list:', error);
        });
}

function checkUrlAvailability() {
    const data = {
        id: 1,
        url: 'http://example.com',
        token: '1234-1234-1234'
    };

    fetch('/api/admin/availability', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('URL status:', data);
    })
    .catch(error => {
        console.error('Error checking the URL availability:', error);
    });
}
```