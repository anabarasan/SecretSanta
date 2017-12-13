# SecretSanta

use the web page or the cli.

configure the MATTERMOST SERVER URL WEBHOOK and CHANNEL NAME to post to.

cli syntax

```
$ cli/secretsanta -h
usage: secretsanta [-h] -@ MENTION -m MESSAGE

optional arguments:
  -h, --help            show this help message and exit

required arguments:
  -@ MENTION, --mention MENTION
                        which user to tag in the message
  -m MESSAGE, --message MESSAGE
                        The message you want to pass alonguse double quotes
                        for multi line
```

