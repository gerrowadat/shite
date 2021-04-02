A simple discord bot for showing what people are up to (even away from regular discord integrations). Mainly just me fiddling with discord bots.

To get it working, you need 4 files::
  - discord.key - [Set up a discord bot](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/) and put your API key in discord.key
  - xapi.key - Set up xapi.us (the free tier will do). Put your api key in xapi.key
  - steam.key - Set up a [Steam Web API key](https://steamcommunity.com/dev/apikey)  (you can do this with your existing steam ID). Put your API key in steam.key
  - users.txt

The users.txt file contains a set of players, one per line, in the following form:

```
steamid:dicordnick:xbox_gamertag
```

The steam ID is in the URL bar when someone looks at their steam profile on web. Discord nick and xbox gamertag should be obvious.

Them run playerbot.py --config_dir=/path/to/where/above/files/are
