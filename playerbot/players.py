#!/usr/bin/python3

import requests
from absl import app
from absl import flags
from absl import logging


FLAGS = flags.FLAGS
flags.DEFINE_string('config_dir', '/config/', 'Path to config and key file dir')


class Player(object):
    def __init__(self, steamid, discordname, xbox, xapi_key=None, steam_key=None):
      self._s = steamid
      self._d = discordname
      self._x = xbox
      self._xuid = None
      self._x_key = xapi_key
      self._s_key = steam_key

    @property
    def steamid(self):
        return self._s

    @property
    def discordname(self):
        return self._d

    @property
    def xbox_gamertag(self):
        return self._x

    def xbox_xuid(self):
        if self._xuid:
            return self._xuid
        url = 'https://xapi.us/v2/xuid/%s' % (self._x)
        r = requests.get(url, headers={'X-AUTH': self._x_key})
        self._xuid = r.text
        return self._xuid

    def get_steam_status(self):
        url = 'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=%s&steamids=%s' % (self._s_key, self._s)
        r = requests.get(url)
        j = r.json()
        if 'gameextrainfo' in j['response']['players'][0]:
            return j['response']['players'][0]['gameextrainfo']
        return None

    def get_xbox_status(self):
        url = 'https://xapi.us/v2/%s/presence' % (self.xbox_xuid(), )
        r = requests.get(url, headers={'X-AUTH': self._x_key})
        logging.debug(r.text)
        return r.json()['state']


class PlayerRoster(object):
    def __init__(self, playerfile, xapi_key, steam_key):
        self._x_key = xapi_key
        self._s_key = steam_key
        self._p = []
        with open(playerfile) as f:
            lines = f.readlines()

        for l in lines:
            if l.startswith('#'):
                continue
            (steam, discord, xbox) = l.strip('\n').split(':')
            logging.debug('Steam ID %s is %s in discord and %s in xbox' % (steam, discord, xbox))
            self._p.append(Player(steam, discord, xbox, xapi_key=self._x_key, steam_key=self._s_key))

    @property
    def players(self):
        return self._p


def main(_):

    with open(FLAGS.config_dir + '/steam.key') as f:
        steam_key = f.read().strip('\n')

    with open(FLAGS.config_dir + '/xapi.key') as f:
        xapi_key = f.read().strip('\n')

    roster = PlayerRoster(FLAGS.config_dir + '/users.txt', xapi_key=xapi_key, steam_key=steam_key)
    for p in roster.players:
       print('%s: [steam] %s: [xbox] %s' % (p.discordname, p.get_steam_status(), p.get_xbox_status()))


if __name__ == '__main__':
    app.run(main)
