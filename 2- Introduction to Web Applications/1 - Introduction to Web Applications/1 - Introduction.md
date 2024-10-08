___

# Introduction

Web applications are interactive applications that run on web browsers. They usually adopt a client-server architecture to handle interactions. These applications have front-end components (i.e., the website interface, or "what the user sees") running on the client-side (browser) and back-end components (web application source code) running on the server-side (back end server/databases).

This setup allows organizations to host powerful applications with real-time control over their design and functionality while being accessible worldwide. Examples include online email services like Gmail, online retailers like Amazon, and online word processors like Google Docs.

Web applications can be developed by any web developer and hosted on common hosting services, used by anyone on the internet. Today, there are millions of web applications globally, with billions of users interacting with them daily.

## Web Applications vs. Websites

Previously, we interacted with static websites that couldn't be changed in real-time (Web 1.0). Traditional static websites were designed to display specific information, which could only be altered by developers manually. These websites lacked real-time interactivity and functionality.

In contrast, modern websites running web applications (Web 2.0) present dynamic content based on user interaction. Key differences between websites and web applications include:
- Modularity
- Cross-device compatibility
- Platform independence without optimization requirements

![[Pasted image 20240924131509.png]]

## Web Applications vs. Native OS Applications

Web applications are platform-independent and run in browsers, making them accessible on any operating system without installation. Their functionality is executed on remote servers, saving space on the user's hard drive. Another advantage is version unity—users always access the same version, which can be updated centrally without requiring individual updates.

However, native OS applications offer faster operation, deeper integration with the operating system, and local hardware utilization. Despite this, hybrid and progressive web applications now use modern frameworks to achieve performance close to native applications.

## Web Application Distribution

Organizations utilize both open-source and proprietary web applications. Common open-source examples include:
- WordPress
- OpenCart
- Joomla

Proprietary web applications, typically offered via subscription models, include:
- Wix
- Shopify
- DotNetNuke

## Security Risks of Web Applications

Web application attacks are common and pose significant risks. Since these applications are accessible from anywhere, they offer a large attack surface. Many tools for scanning and attacking web applications are readily available, making them attractive targets for malicious actors.

A successful attack can lead to business disruptions, compromised data, and financial losses. Web applications often store sensitive data on the same server hosting the application, so if an attacker breaches the application, they could access sensitive user or corporate data. 

This makes vulnerability testing critical. Regular penetration testing and secure coding practices throughout the development lifecycle are necessary for protecting web applications. The OWASP Web Security Testing Guide provides one of the most current methodologies for testing web applications.

Penetration testing begins with analyzing front-end components (HTML, CSS, JavaScript) for vulnerabilities like Sensitive Data Exposure and Cross-Site Scripting (XSS). Then, testers review the core functionality and server-side interactions, assessing the web application from both unauthenticated and authenticated perspectives.

## Attacking Web Applications

Many companies, regardless of size, host web applications. These can range from static websites to dynamic applications with sign-up/login functionalities. Web applications provide a vast attack surface and can be vulnerable due to overlooked security flaws. A small code change might introduce catastrophic vulnerabilities or allow for attack chaining to exploit sensitive data or execute code remotely.

Common vulnerabilities in web applications include:
- **SQL Injection**: This flaw occurs when user input is unsafely handled, potentially leading to unauthorized data access or remote code execution.
- **File Inclusion**: Attackers can exploit poorly validated file paths to read sensitive files or execute code on the server.
- **Unrestricted File Upload**: Allows attackers to upload malicious files, leading to remote code execution.
- **Insecure Direct Object Referencing (IDOR)**: Occurs when user-controlled parameters can access unauthorized data or functionality.
- **Broken Access Control**: Attackers can exploit weak access control mechanisms to escalate privileges or access unauthorized features.

Understanding these vulnerabilities is key to web application penetration testing and can set apart security professionals who can uncover flaws others might miss.

## Real-World Examples of Web Application Attacks

| **Flaw**                      | **Real-world Scenario**                                                                                                                                   |
|-------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| **SQL Injection**              | Obtaining Active Directory usernames and performing a password spray attack against a VPN or email portal.                                                 |
| **File Inclusion**             | Reading source code to find a hidden page or directory, exposing functionality that can lead to remote code execution.                                      |
| **Unrestricted File Upload**   | Uploading malicious code to gain control of the web application server.                                                                                    |
| **Insecure Direct Object Reference (IDOR)** | Changing a URL parameter to access another user’s files or account functionality.                                                              |
| **Broken Access Control**      | Manipulating account registration parameters to escalate privileges and register as an admin user.                                                        |

It’s important to familiarize yourself with these attacks as you progress in your penetration testing journey. Developing a deep understanding of web applications and attack techniques will help you stand out in the field of security testing and discover vulnerabilities others may overlook.
