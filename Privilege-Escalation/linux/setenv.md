____

Checking the [sudoers man page](https://linux.die.net/man/5/sudoers) against what’s in this configuration, in the flags, there’s `env_reset`, which basically says that, because there’s no `env_keep` setting, none of waldo’s environment will be passed:

> If set, **sudo** will run the command in a minimal environment containing the TERM, PATH, HOME, MAIL, SHELL, LOGNAME, USER, USERNAME and SUDO_* variables. Any variables in the caller’s environment that match the env_keep and env_check lists are then added, followed by any variables present in the file specified by the _env_file_ option (if any). The default contents of the env_keep and env_check lists are displayed when **sudo** is run by root with the **-V** option. If the _secure_path_ option is set, its value will be used for the PATH environment variable. This flag is _on_ by default.

Next the `SETENV` tag says that as the caller, I can override `env_reset` using `-E` or by setting variables on the command line when I call `sudo`:

> _SETENV and NOSETENV_
> 
> These tags override the value of the _setenv_ option on a per-command basis. Note that if SETENV has been set for a command, the user may disable the _env_reset_ option from the command line via the **-E** option. Additionally, environment variables set on the command line are not subject to the restrictions imposed by _env_check_, _env_delete_, or _env_keep_. As such, only trusted users should be allowed to set variables in this manner. If the command matched is **ALL**, the SETENV tag is implied for that command; this default may be overridden by use of the NOSETENV tag.

`secure_path` was also mentioned in the `env_reset` page, and is set here. It prevents the `sudo` caller from setting the `$PATH` variable:

> secure_path Path used for every command run from **sudo**. If you don’t trust the people running **sudo** to have a sane PATH environment variable you may want to use this. Another use is if you want to have the ‘‘root path’’ be separate from the ‘‘user path’’. Users in the group specified by the _exempt_group_ option are not affected by _secure_path_. This option is not set by default.

One last thing I learned about how `sudo` handles environment variables - I has a list of “bad” variables that don’t carry into the new command even with `-E`, as explained [here](https://stackoverflow.com/questions/35824788/sudo-e-does-not-pass-pythonpath). What that post doesn’t show is that it doesn’t seem to apply to variables passed inline:

One last thing I learned about how `sudo` handles environment variables - I has a list of “bad” variables that don’t carry into the new command even with `-E`, as explained [here](https://stackoverflow.com/questions/35824788/sudo-e-does-not-pass-pythonpath). What that post doesn’t show is that it doesn’t seem to apply to variables passed inline:

```
# $TESTVAR enters through sudo with -E
$ TESTVAR=testValue sudo -E bash -c 'echo $TESTVAR'
testValue

# $PYTHONPATH does not
$ PYTHONPATH=testValue sudo -E bash -c 'echo $PYTHONPATH'

# Passing $PYTHONPATH as part of the command does work
$ sudo PYTHONPATH=testValue bash -c 'echo $PYTHONPATH'
testValue
```
