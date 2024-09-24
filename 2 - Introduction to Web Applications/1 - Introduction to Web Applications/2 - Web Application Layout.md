____

Web application layouts consist of many different layers that can be summarized with the following three main categories:

|**Category**|**Description**|
|---|---|
|`Web Application Infrastructure`|Describes the structure of required components, such as the database, needed for the web application to function as intended. Since the web application can be set up to run on a separate server, it is essential to know which database server it needs to access.|
|`Web Application Components`|The components that make up a web application represent all the components that the web application interacts with. These are divided into the following three areas: `UI/UX`, `Client`, and `Server` components.|
|`Web Application Architecture`|Architecture comprises all the relationships between the various web application components.|

## Web Application Infrastructure

Web applications can use many different infrastructure setups. These are also called `models`. The most common ones can be grouped into the following four types:

### Client-Server

![[Pasted image 20240924131804.png]]

### One Server

![[Pasted image 20240924131818.png]]

### Many Servers - One Database

![[Pasted image 20240924131845.png]]

### Many Servers - Many Databases

![[Pasted image 20240924131859.png]]

## Web Application Components

1. `Client`
2. `Server`
    - Webserver
    - Web Application Logic
    - Database
3. `Services` (Microservices)
    - 3rd Party Integrations
    - Web Application Integrations
4. `Functions` (Serverless)


## Web Application Architecture

The components of a web application are divided into three different layers (AKA Three Tier Architecture).

|**Layer**|**Description**|
|---|---|
|`Presentation Layer`|Consists of UI process components that enable communication with the application and the system. These can be accessed by the client via the web browser and are returned in the form of HTML, JavaScript, and CSS.|
|`Application Layer`|This layer ensures that all client requests (web requests) are correctly processed. Various criteria are checked, such as authorization, privileges, and data passed on to the client.|
|`Data Layer`|The data layer works closely with the application layer to determine exactly where the required data is stored and can be accessed.|