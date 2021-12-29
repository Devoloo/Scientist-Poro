import discord
import yaml
from riotwatcher import ApiError, LolWatcher

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
    player = player.lower()

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
            rate = (int(d['wins']) / (int(d['wins']) + int(d['losses']))) * 100
            stat['RANKED_FLEX_SR_RATE'] = f"{format(rate, '.2f')} %"
        if queueType == 'RANKED_SOLO_5x5':
            stat['RANKED_SOLO_5x5'] = f"{d['tier'][0]}{d['tier'][1:].lower()} {d['rank']}"
            stat['RANKED_SOLO_5x5_WIN'] = f"{d['wins']}"
            stat['RANKED_SOLO_5x5_LOSSE'] = f"{d['losses']}"
            rate = (int(d['wins']) / (int(d['wins']) + int(d['losses']))) * 100
            stat['RANKED_SOLO_5x5_RATE'] = f"{format(rate, '.2f')} %"

    return stat


def get_most_played_champion(region, player):
    player = player.lower()

    # Check error while searching player in euw1
    try:
        current_player = watcher.summoner.by_name(region, player)
    except ApiError as err:
        print(f"\033[31mError {err}\033[0m")
        return None

    champion_mastery = watcher.champion_mastery.by_summoner(
        region, current_player['id'])
    most_played = champion_mastery[0]

    latest = watcher.data_dragon.versions_for_region(region)['n']['champion']
    static_champ_list = watcher.data_dragon.champions(latest, False, 'en_US')

    champ_dict = {}
    for key in static_champ_list['data']:
        current_champ = static_champ_list['data'][key]
        champ_dict[f"{static_champ_list['data'][key]['key']}"] = current_champ

    champ_stat = champ_dict[f"{most_played['championId']}"]

    most_played_dict = {
        'name': champ_stat['name'],
        'title': champ_stat['title'],
        'blurb': champ_stat['blurb'],
        'championLevel': most_played['championLevel'],
        'championPoints': most_played['championPoints']
    }

    return most_played_dict


def champion_stat(champion):
    latest = watcher.data_dragon.versions_for_region('euw1')['n']['champion']
    static_champ_list = watcher.data_dragon.champions(latest, False, 'en_US')

    champ_dict = {}
    for key in static_champ_list['data']:
        current_champ_stat = static_champ_list['data'][key]
        champ_dict[f"{key.lower()}"] = current_champ_stat

    champion = champion.lower()

    if not (champion[:len(champion) - 1] in champ_dict):
        print(
            f"\033[31mError {champion[:len(champion) - 1]} not in dict\033[0m")
        return None

    current_champion = champ_dict[champion[:len(champion) - 1]]
    current_champion_stat = current_champion['stats']

    champ_dict_stat = {
        'name': current_champion['name'],
        'title': current_champion['title'],
        'blurb': current_champion['blurb'],
        'hp': current_champion_stat['hp'],
        'movespeed': current_champion_stat['movespeed'],
        'armor': current_champion_stat['armor'],
        'spellblock': current_champion_stat['spellblock'],
        'attackrange': current_champion_stat['attackrange'],
        'attackdamage': current_champion_stat['attackdamage'],
    }

    return champ_dict_stat


"""
Main function for the Discord bot
Actually bot can handle:
!help
!link
!player/!p <player_name>
!most_played/!mp <player_name>
!champion/!c <champion_name>
"""

latest = watcher.data_dragon.versions_for_region('euw1')['n']['champion']


foot_msg = f"Developed with ♥ by mattyeux (patch {latest})."


class MyClient(discord.Client):
    # Ready to use
    async def on_ready(self):
        print(f"\033[32mLogged in as {self.user.name}\033[0m")

    # check when a message is send
    async def on_message(self, message):
        # region init_message
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
        # endregion

        # region Help
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

            embed.add_field(
                name="Player best champion",
                value="`!player_best <player_name>` or `!pb <player_name>` display player most played champion",
                inline=False
            )

            embed.add_field(
                name="Champion stats",
                value="`!champion <champion_name>` or `!c <champion_name>` display champion stats",
                inline=False
            )

            # Add footer
            embed.set_footer(
                text=foot_msg
            )

            await message.channel.send(embed=embed)
            print(
                f"\033[32mSend {message.channel.id} at {message.guild.id}\033[0m")
        # endregion

        # region Link
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
                text=foot_msg
            )

            await message.channel.send(embed=embed)
            print(
                f"\033[32mSend {message.channel.id} at {message.guild.id}\033[0m")
        # endregion

        # region Player
        if msg_content[0] == '!player' or msg_content[0] == '!p':
            # region Error
            if len(msg_content) == 1:
                embed = discord.Embed(
                    title='Error',
                    description=f"Usage: `!player/!p <player_name>`",
                    color=0xFF5733
                )

                embed.set_footer(
                    text=foot_msg
                )

                await message.channel.send(embed=embed)
                print(
                    f"\033[32mSend {message.channel.id} at {message.guild.id}\033[0m")
                return
            # endregion

            # region Get full name
            args = ""
            for arg in msg_content[1:]:
                args += f"{arg} "
            # endregion

            player_stat = get_stat("euw1", args)

            # region Player not found
            if player_stat == None:
                embed = discord.Embed(
                    title='Error',
                    description=f"Player **{args}**not found on euw region...\nMaybe username is not wrong or the player is not in euw.",
                    color=0xFF5733
                )

                embed.set_footer(
                    text=foot_msg
                )

                await message.channel.send(embed=embed)
                print(
                    f"\033[32mSend {message.channel.id} at {message.guild.id}\033[0m")
                return
            # endregion

            # region General creation
            # Create player opgg url
            player_url = ""
            for w in msg_content[1:]:
                player_url += f"{w}%20"

            opgg_url = f"https://euw.op.gg/summoner/userName={player_url}"

            embed = discord.Embed(
                title=f"OPGG link for {player_stat['username']}",
                url=opgg_url,
                color=0xFF5733
            )

            embed.set_author(
                name=message.author.display_name,
                icon_url=message.author.avatar_url
            )

            embed.set_thumbnail(
                url=f"https://raw.githubusercontent.com/Devoloo/Scientist-Poro/main/riot_data/11.24.1/img/profileicon/{player_stat['icon']}"
            )

            embed.add_field(
                name="Level :level_slider:",
                value=player_stat['level'],
                inline=False
            )
            # endregion

            # region RANKED_FLEX_SR
            if 'RANKED_FLEX_SR' in player_stat:
                embed.add_field(
                    name=">>> Ranked Flex",
                    value="Here stats for ranked flex !",
                    inline=True
                )

                embed.add_field(
                    name="Rank :trophy:",
                    value=player_stat['RANKED_FLEX_SR'],
                    inline=False
                )

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

                embed.add_field(
                    name="Rate :computer:",
                    value=player_stat['RANKED_FLEX_SR_RATE'],
                    inline=True
                )
            # endregion

            # region RANKED_SOLO_5x5
            if 'RANKED_SOLO_5x5' in player_stat:
                embed.add_field(
                    name=">>> Ranked Solo/Duo",
                    value="Here stats for ranked solo/duo !",
                    inline=True
                )

                embed.add_field(
                    name="Rank :military_medal:",
                    value=player_stat['RANKED_SOLO_5x5'],
                    inline=False
                )

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

                embed.add_field(
                    name="Rate :computer:",
                    value=player_stat['RANKED_SOLO_5x5_RATE'],
                    inline=True
                )
            # endregion

            embed.set_footer(
                text=foot_msg
            )

            await message.channel.send(embed=embed)

            print(
                f"\033[32mSend {message.channel.id} at {message.guild.id}\033[0m")
        # endregion

        # region Most played champion
        if msg_content[0] == "!player_best" or msg_content[0] == "!pb":
            # region Error
            if len(msg_content) == 1:
                embed = discord.Embed(
                    title='Error',
                    description=f"Usage: `!most_played/!mp <player_name>`",
                    color=0xFF5733
                )

                embed.set_footer(
                    text=foot_msg
                )

                await message.channel.send(embed=embed)
                print(
                    f"\033[32mSend {message.channel.id} at {message.guild.id}\033[0m")
                return
            # endregion

            # region Get full name
            args = ""
            for arg in msg_content[1:]:
                args += f"{arg} "
            player_stat = get_stat("euw1", args)
            # endregion

            most_played = get_most_played_champion('euw1', args)

            # region Player not found
            if most_played == None:
                embed = discord.Embed(
                    title='Error',
                    description=f"Player **{args}**not found on euw region...\nMaybe username is not wrong or the player is not in euw.",
                    color=0xFF5733
                )

                embed.set_footer(
                    text=foot_msg
                )

                await message.channel.send(embed=embed)
                print(
                    f"\033[32mSend {message.channel.id} at {message.guild.id}\033[0m")
                return
            # endregion

            # region General creation
            champion_name = most_played['name'].lower()
            champion_name = champion_name.replace(" ", "%20")
            opgg_url = f"https://euw.op.gg/champion/{champion_name}"

            embed = discord.Embed(
                title=f"{args}most played champion: {most_played['name']}",
                url=opgg_url,
                description=f"\"*{most_played['title']}*\"",
                color=0xFF5733
            )

            embed.set_author(
                name=message.author.display_name,
                icon_url=message.author.avatar_url
            )

            champion_name = most_played['name']
            champion_name = champion_name.replace(" ", "")

            embed.set_thumbnail(
                url=f"https://raw.githubusercontent.com/Devoloo/Scientist-Poro/main/riot_data/11.24.1/img/champion/{champion_name}.png"
            )

            embed.add_field(
                name="Short history :book:",
                value=most_played['blurb'],
                inline=False
            )

            embed.add_field(
                name="Champion mastery :unlock:",
                value=most_played['championLevel'],
                inline=True
            )

            embed.add_field(
                name="Champion point :first_place:",
                value=most_played['championPoints'],
                inline=True
            )

            # Add footer
            embed.set_footer(
                text=foot_msg
            )

            await message.channel.send(embed=embed)

            print(
                f"\033[32mSend {message.channel.id} at {message.guild.id}\033[0m")
            # endregion
        # endregion

        # region Champion stat
        if msg_content[0] == "!champion" or msg_content[0] == "!c":
            # region Error
            if len(msg_content) == 1:
                embed = discord.Embed(
                    title='Error',
                    description=f"Usage: `!champion/!c <champion_name>`",
                    color=0xFF5733
                )

                embed.set_footer(
                    text=foot_msg
                )

                await message.channel.send(embed=embed)
                print(
                    f"\033[32mSend {message.channel.id} at {message.guild.id}\033[0m")
                return
            # endregion

            # region Get full name
            args = ""
            for arg in msg_content[1:]:
                args += f"{arg} "
            player_stat = get_stat("euw1", args)
            # endregion

            champion = champion_stat(args)

            # region champion not found
            if champion == None:
                embed = discord.Embed(
                    title='Error',
                    description=f"Champion **{args}**not found...",
                    color=0xFF5733
                )

                embed.set_footer(
                    text=foot_msg
                )

                await message.channel.send(embed=embed)
                print(
                    f"\033[32mSend {message.channel.id} at {message.guild.id}\033[0m")
                return
            # endregion

            # region General creation
            champion_name = champion['name'].lower()
            champion_name = champion_name.replace(" ", "%20")
            print(champion_name)
            opgg_url = f"https://euw.op.gg/champion/{champion_name}"

            embed = discord.Embed(
                title=f"{champion['name']}",
                url=opgg_url,
                description=f"\"*{champion['title']}*\"",
                color=0xFF5733
            )

            embed.set_author(
                name=message.author.display_name,
                icon_url=message.author.avatar_url
            )

            champion_name = champion['name']
            champion_name = champion_name.replace(" ", "")

            embed.set_thumbnail(
                url=f"https://raw.githubusercontent.com/Devoloo/Scientist-Poro/main/riot_data/11.24.1/img/champion/{champion_name}.png"
            )

            embed.add_field(
                name="Short history :book:",
                value=champion['blurb'],
                inline=False
            )

            embed.add_field(
                name=":two_hearts: Health",
                value=champion['hp'],
                inline=True
            )

            embed.add_field(
                name=":roller_skate: Speed",
                value=champion['movespeed'],
                inline=True
            )

            embed.add_field(
                name=":martial_arts_uniform: Armor",
                value=champion['armor'],
                inline=True
            )

            embed.add_field(
                name=":closed_book: Magic resit",
                value=champion['spellblock'],
                inline=True
            )

            embed.add_field(
                name=":bow_and_arrow: Attack range",
                value=champion['attackrange'],
                inline=True
            )

            embed.add_field(
                name=":muscle_tone2: Attack damage",
                value=champion['attackdamage'],
                inline=True
            )

            # Add footer
            embed.set_footer(
                text=foot_msg
            )

            await message.channel.send(embed=embed)

            print(
                f"\033[32mSend {message.channel.id} at {message.guild.id}\033[0m")
            # endregion
        # endregion


# Create client and run it
client = MyClient()
client.run(discord_token)
