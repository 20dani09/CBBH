___

|Tool|Description|Features|
|---|---|---|
|`Wappalyzer`|Browser extension and online service for website technology profiling.|Identifies a wide range of web technologies, including CMSs, frameworks, analytics tools, and more.|
|`BuiltWith`|Web technology profiler that provides detailed reports on a website's technology stack.|Offers both free and paid plans with varying levels of detail.|
|`WhatWeb`|Command-line tool for website fingerprinting.|Uses a vast database of signatures to identify various web technologies.|
|`Nmap`|Versatile network scanner that can be used for various reconnaissance tasks, including service and OS fingerprinting.|Can be used with scripts (NSE) to perform more specialised fingerprinting.|
|`Netcraft`|Offers a range of web security services, including website fingerprinting and security reporting.|Provides detailed reports on a website's technology, hosting provider, and security posture.|
|`wafw00f`|Command-line tool specifically designed for identifying Web Application Firewalls (WAFs).|Helps determine if a WAF is present and, if so, its type and configuration.|
# Banner Grabbing

```bash
curl -I inlanefreight.com
```

# Wafw00f

```bash
wafw00f inlanefreight.com
```

# Nikto

```bash
nikto -h inlanefreight.com -Tuning b
```

> Determine the Apache version running on app.inlanefreight.local on the target system. (Format: 0.0.0)

![[Pasted image 20240926135645.png]]

> Which CMS is used on app.inlanefreight.local on the target system? Respond with the name only, e.g., WordPress.

![[Pasted image 20240926135722.png]]

> On which operating system is the dev.inlanefreight.local webserver running in the target system? Respond with the name only, e.g., Debian.

![[Pasted image 20240926135907.png]]

![[Pasted image 20240926135929.png]]



