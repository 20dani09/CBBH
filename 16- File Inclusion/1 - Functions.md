___

|**Function**|**Read Content**|**Execute**|**Remote URL**|
|---|:-:|:-:|:-:|
|**PHP**||||
|`include()`/`include_once()`|Yes|Yes|Yes|
|`require()`/`require_once()`|Yes|Yes|No|
|`file_get_contents()`|Yes|No|Yes|
|`fopen()`/`file()`|Yes|No|No|
|**NodeJS**||||
|`fs.readFile()`|Yes|No|No|
|`fs.sendFile()`|Yes|No|No|
|`res.render()`|Yes|Yes|No|
|**Java**||||
|`include`|Yes|No|No|
|`import`|Yes|Yes|Yes|
|**.NET**||||
|`@Html.Partial()`|Yes|No|No|
|`@Html.RemotePartial()`|Yes|No|Yes|
|`Response.WriteFile()`|Yes|No|No|
|`include`|Yes|Yes|Yes|
