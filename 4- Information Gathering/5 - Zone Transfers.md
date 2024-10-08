___
DNS zone transfers, also known as AXFR (Asynchronous Full Transfer) requests, offer a potential goldmine of information for web reconnaissance. A zone transfer is a mechanism for replicating DNS data across servers. When a zone transfer is successful, it provides a complete copy of the DNS zone file, which contains a wealth of details about the target domain.

This zone file lists all the domain's subdomains, their associated IP addresses, mail server configurations, and other DNS records. This is akin to obtaining a blueprint of the target's DNS infrastructure for a reconnaissance expert.

To attempt a zone transfer, you can use the `dig` command with the `axfr` (full zone transfer) option. For example, to request a zone transfer from the DNS server `ns1.example.com` for the domain `example.com`, you would execute:

```bash
dig @ns1.example.com example.com axfr
```

However, zone transfers are not always permitted. Many DNS servers are configured to restrict zone transfers to authorized secondary servers only. Misconfigured servers, though, may allow zone transfers from any source, inadvertently exposing sensitive information.

![](https://mermaid.ink/svg/pako:eNqNkc9qwzAMxl9F-JSx7gV8KISWXcY2aHYYwxdjK39obGWKvBFK333ukg5aGNQnW9b3Q_q-g3LkUWk14mfC6HDb2YZtMBHyGdFR9JanCvkL-WG9vh-4C38FDeX74w52J-0oUHxQRHhjG8ca-W5mXAgy4YqpoXotM8EReygqsSxANZRJWuJOpoXSEw0gC3ku3QTfvlQLfBZh9DeOdbELbCgMPQr-58u1LZsnKEq3j_Tdo28wYJS8iVqpgBxs57PjhxPLKGnzr1E6XzNxb5SJx9xnk1A1Rae0cMKVYkpNq3Rt-zG_0uCtnLM6t6DvhPh5zvM31uMPG8qm-A)

> After performing a zone transfer for the domain inlanefreight.htb on the target system, how many DNS records are retrieved from the target system's name server? Provide your answer as an integer, e.g, 123.

```bash
dig axfr inlanefreight.htb @10.129.79.224
```

![[Pasted image 20240925184319.png]]

The command `dig axfr inlanefreight.htb @10.129.79.224` is asking the DNS server at the IP address `10.129.79.224` to perform a zone transfer for the domain `inlanefreight.htb`.

> Within the zone record transferred above, find the ip address for ftp.admin.inlanefreight.htb. Respond only with the IP address, eg 127.0.0.1

![[Pasted image 20240925184531.png]]

> Within the same zone record, identify the largest IP address allocated within the 10.10.200 IP range. Respond with the full IP address, eg 10.10.200.1

![[Pasted image 20240925184612.png]]


