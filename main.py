import discord
import yaml
from riotwatcher import ApiError, LolWatcher

from utils.champion_stat import champion_stat_function
from utils.help import help_function
from utils.link import link_function
from utils.player_champ_stat import player_champ_stat_function
from utils.player_ranked_stat import player_ranked_stat_function
from utils.challenger_top import challenger_top_function


def parse_message(message):
    """
    Parse the given message and return a list with all word
    """
    result = []
    current = ""
    for c in message:
        if c != ' ':
            current += c
        else:
            result.append(current)
            current = ""
    result.append(current)
    return result


def recive_msg(message, msg_content):
    print(f"\033[34mRecieve message from {message.author} in channel" +
          f"{message.channel.id} from server {message.guild.id}, content: {msg_content}\033[0m")


class MyClient(discord.Client):
    # Ready to use
    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!help"))
        print(f"\033[32mLogged in as {self.user.name}\033[0m")

    # check when a message is send
    async def on_message(self, message):
        # if message don't start with token just ignore
        if not message.content.startswith('!'):
            return

        # if message is send by bot we don't want to respond
        if message.author.id == self.user.id:
            return
        else:
            msg_content = parse_message(message.content)
            recive_msg(message, msg_content)

        if msg_content[0] == "!help" or msg_content[0] == "!h":
            await help_function(message)

        if msg_content[0] == "!link" or msg_content[0] == "!l":
            await link_function(message)

        if msg_content[0] == '!player' or msg_content[0] == '!p':
            await player_ranked_stat_function(message, msg_content)

        if msg_content[0] == "!player_best" or msg_content[0] == "!pb":
            await player_champ_stat_function(message, msg_content)

        if msg_content[0] == "!champion" or msg_content[0] == "!c":
            await champion_stat_function(message, msg_content)

        if msg_content[0] == "!top":
            await challenger_top_function(message)


with open('config.yaml', 'r') as stream:
    token_list = yaml.safe_load(stream)

discord_token = token_list['discord']


# Create client and run it
client = MyClient()
client.run(discord_token)
