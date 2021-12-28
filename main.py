import discord
from riotwatcher import LolWatcher, ApiError
import yaml

with open('config.yaml', 'r') as stream:
    token_list = yaml.safe_load(stream)

discord_token = token_list['discord']
riot_token = token_list['riot']

# Optionnal function


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


# Riot api key
api_key = riot_token
watcher = LolWatcher(api_key)

# Return stat and icon of player


def get_stat(region, player):
    """
    Return a dict with all player stat (for solor_duo actually)
    Player username
    Player account icon
    Player current rank
    Player wins losses
    """
    # Check error while searching player in euw1
    try:
        current_player = watcher.summoner.by_name(region, player)
    except ApiError as err:
        print(f"\033[31mError {err}\033[0m")
        return None

    ranked_stats = watcher.league.by_summoner(region, current_player['id'])

    player_icon = f"{current_player['profileIconId']}.png"
    player_level = current_player['summonerLevel']

    stat = {'username': f"{player}",
            'icon': f"{player_icon}", 'level': f"{player_level}"}

    for d in ranked_stats:
        queueType = d['queueType']
        if queueType == 'RANKED_FLEX_SR':
            stat['RANKED_FLEX_SR'] = f"{d['tier'][0]}{d['tier'][1:].lower()} {d['rank']}"
            stat['RANKED_FLEX_SR_WIN'] = f"{d['wins']}"
            stat['RANKED_FLEX_SR_LOSSE'] = f"{d['losses']}"
        if queueType == 'RANKED_SOLO_5x5':
            stat['RANKED_SOLO_5x5'] = f"{d['tier'][0]}{d['tier'][1:].lower()} {d['rank']}"
            stat['RANKED_SOLO_5x5_WIN'] = f"{d['wins']}"
            stat['RANKED_SOLO_5x5_LOSSE'] = f"{d['losses']}"

    return stat


"""
Main function for the Discord bot
Actually bot can handle:
!help
!link
!player <player_name> (give stat for solo_duo)
"""


class MyClient(discord.Client):
    # Ready to use
    async def on_ready(self):
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
            # get the current message is a list
            msg_content = parse_message(message.content)
            # send information in console
            print(
                f"\033[34mRecieve message from {message.author} in channel {message.channel.id} from server {message.guild.id}, content: {msg_content}\033[0m")

        # Help function
        if msg_content[0] == "!help" or msg_content[0] == "!h":
            embed = discord.Embed(
                title="Help",
                color=0xFF5733
            )

            embed.add_field(
                name="Help",
                value="`!help` or `!h` display this panel",
                inline=False
            )

            embed.add_field(
                name="Link",
                value="`!link` or `!l` give link to invite on your server",
                inline=False
            )

            embed.add_field(
                name="Player ranked stats",
                value="`!player <player_name>` or `!p <player_name>` display player ranked stats in solo duo",
                inline=False
            )

            # Add footer
            embed.set_footer(
                text="Information provided by mattyeux.Inc."
            )

            await message.channel.send(embed=embed)

        # Link function
        if msg_content[0] == "!link" or msg_content[0] == "!l":
            embed = discord.Embed(
                title="Link",
                color=0xFF5733
            )

            embed.add_field(
                name="Click on the link to add the bot to your server",
                value="[Add !](https://discord.com/api/oauth2/authorize?client_id=875781797651316819&permissions=8&scope=bot)",
                inline=False
            )

            # Add footer
            embed.set_footer(
                text="Information provided by mattyeux.Inc."
            )

            await message.channel.send(embed=embed)

        # Give stat of player for ranked solo duo function
        if msg_content[0] == '!player' or msg_content[0] == '!p':
            # Region is euw1
            args = ""
            for arg in msg_content[1:]:
                args += f" {arg}"
            player_stat = get_stat("euw1", args)

            """
            Player not found
            """
            if player_stat == None:
                embed = discord.Embed(
                    title='Error',
                    description=f"Player **{args}** not found on euw region...\nMaybe username is not wrong or the player is not in euw.",
                    color=0xFF5733
                )

                # Add footer
                embed.set_footer(
                    text="Information provided by mattyeux.Inc."
                )

                await message.channel.send(embed=embed)
                print(
                    f"\033[32mMessage send in {message.channel.id} at {message.guild.id}\033[0m")
                return

            player_url = ""
            for w in msg_content[1:]:
                player_url += f"{w}%20"

            opgg_url = f"https://euw.op.gg/summoner/userName={player_url}"
            icon = discord.File(
                f"riot_data\\11.24.1\\img\\profileicon\\{player_stat['icon']}", filename=player_stat['icon'])

            # Create embed message
            embed = discord.Embed(
                title=f"OPGG link for{player_stat['username']}",
                url=opgg_url,
                color=0xFF5733
            )

            # Author of message
            embed.set_author(
                name=message.author.display_name,
                icon_url=message.author.avatar_url
            )

            # Add player icon
            embed.set_thumbnail(
                url=f"attachment://{player_stat['icon']}"
            )

            # Add player stat
            embed.add_field(
                name="Level :level_slider:",
                value=player_stat['level'],
                inline=False
            )

            """
                RANKED_FLEX_SR
                """
            if 'RANKED_FLEX_SR' in player_stat:
                embed.add_field(
                    name="Ranked flex :military_medal:",
                    value=player_stat['RANKED_FLEX_SR'],
                    inline=True
                )

                if player_stat['RANKED_FLEX_SR'] != 'Unranked':
                    embed.add_field(
                        name="Wins :white_check_mark:",
                        value=player_stat['RANKED_FLEX_SR_WIN'],
                        inline=True
                    )

                    embed.add_field(
                        name="Losses :x:",
                        value=player_stat['RANKED_FLEX_SR_LOSSE'],
                        inline=True
                    )

            """ 
                RANKED_SOLO_5x5
                """
            if 'RANKED_SOLO_5x5' in player_stat:
                embed.add_field(
                    name="Rank solo/duo :trophy:",
                    value=player_stat['RANKED_SOLO_5x5'],
                    inline=True
                )

                if player_stat['RANKED_SOLO_5x5'] != 'Unranked':
                    embed.add_field(
                        name="Wins :white_check_mark:",
                        value=player_stat['RANKED_SOLO_5x5_WIN'],
                        inline=True
                    )

                    embed.add_field(
                        name="Losses :x:",
                        value=player_stat['RANKED_SOLO_5x5_LOSSE'],
                        inline=True
                    )

            # Add footer
            embed.set_footer(
                text="Information provided by mattyeux.Inc."
            )

            await message.channel.send(
                file=icon,
                embed=embed
            )
            print(
                f"\033[32mMessage send in {message.channel.id} at {message.guild.id}\033[0m")

        # Champion stat function
        # TODO


# Create client and run it
client = MyClient()
client.run(discord_token)
