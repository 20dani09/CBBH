____

>chmod never changes the permissions of symbolic links; the chmod system call cannot change their permissions. This is not a problem since the permissions of symbolic links are never used. However, for each symbolic link listed on the command line, chmod changes the permissions of the pointed-to file. In contrast, chmod ignores symbolic links encountered during recursive directory traversals


Cronjob script with,

```bash
chmod 777 * -R;
```

Create symlink

```bash
touch test
ln -s -f /usr/bin/backup.sh test
```

![Captura](../../assets/images/reference/f7e968d073850ef3cf37.png)

```bash
ls -l /usr/bin/backup.sh
```

![Captura](../../assets/images/reference/19bbbe2ad0422c0c5004.png)

and now i can modify the script
