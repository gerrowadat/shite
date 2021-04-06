#!/usr/bin/python3

import discord
import players
from absl import app
from absl import flags
from absl import logging

FLAGS = flags.FLAGS

def main(_):
    logging.set_verbosity(logging.DEBUG)
    with open(FLAGS.config_dir + '/discord.key') as f:
        discord_key = f.read().strip('\n')

    with open(FLAGS.config_dir + '/steam.key') as f:
        steam_key = f.read().strip('\n')

    with open(FLAGS.config_dir + '/xapi.key') as f:
        xapi_key = f.read().strip('\n')

    client = discord.Client()
    r = players.PlayerRoster(FLAGS.config_dir + '/users.txt', steam_key=steam_key, xapi_key=xapi_key)


    @client.event
    async def on_ready():
        logging.info('Logged in as %s' % (client.user, ))

    @client.event
    async def on_message(message):
        logging.info('Message from %s' % (message.author, ))
        logging.info(message.content)
        if message.content == '#soundoff':
            logging.info('Sounding off...')
            rep = []
            for p in r.players:
                p_rep = []
                steam = p.get_steam_status()
                (x_on, x_playing) = p.get_xbox_status()
                if steam:
                    p_rep.append('playing %s on PC' % (steam,))
                if x_on != 'Offline':
                    if x_playing == 'Home':
                        p_rep.append('sitting at the dashboard on the xbox')
                    else:
                        p_rep.append('playing %s on the xbox' % (x_playing,))
                if len(p_rep) == 0:
                    p_rep.append('offline')
                rep.append('%s is %s' % (p.discordname, ' and '.join(p_rep)))
            logging.info(', '.join(rep))
            await message.channel.send(', '.join(rep))

    client.run(discord_key)


if __name__ == '__main__':
    app.run(main)
