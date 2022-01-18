import discord
from utils.riot_game_acces import foot_msg, get_player_history
from utils.error import error_riot, error_wrong_args


async def history_function(message, msg_content):
    if len(msg_content) == 1:
        await error_wrong_args(message)
        return

    args = ""
    for arg in msg_content[1:]:
        args += f"{arg} "
    args = args[:len(args) - 1]

    game_history, game_id = get_player_history('europe', args)

    if type(game_history) != dict:
        await error_riot(message, game_history)
        return

    url = f"https://www.leagueofgraphs.com/match/euw/{game_id[5:]}"

    if game_history["team1"]['win']:
        embed = discord.Embed(
            title="Team :blue_square: win :link: !",
            url=url,
            color=0x00FFFF
        )
    else:
        embed = discord.Embed(
            title="Team :red_square: win :link: !",
            url=url,
            color=0xFF0000
        )

    embed.set_author(
        name=message.author.display_name,
        icon_url=message.author.avatar_url
    )

    embed.set_footer(
        text=foot_msg
    )

    embed.add_field(
        name="Team :blue_square:",
        value='** **',
        inline=False
    )

    for blue_player in game_history["team1"]['player']:
        player_name = blue_player
        player_name = player_name.replace(" ", "%20")

        embed.add_field(
            name=f"{blue_player}",
            value=f"[{blue_player} stats.](https://www.leagueofgraphs.com/summoner/euw/{player_name})\
            \n:robot: **Champion: `{game_history['team1']['player'][blue_player][0]}`**\
            \n:skull_crossbones: **K/D/A: `{game_history['team1']['player'][blue_player][1]}`**\
            \n:crossed_swords: **Damage dealt: `{game_history['team1']['player'][blue_player][2]}`**\
            \n:shield: **Damage taken: `{game_history['team1']['player'][blue_player][3]}`**\
            \n:heart_on_fire: **Total heal: `{game_history['team1']['player'][blue_player][4]}`**\
            \n:farmer: **Farming: `{game_history['team1']['player'][blue_player][5]}`**\
            \n:bulb: **Vision score: `{game_history['team1']['player'][blue_player][6]}`**\
            \n:moneybag: **Gold earned: `{game_history['team1']['player'][blue_player][7]}`**",
            inline=True
        )

    embed.add_field(
        name='\u200B',
        value='\u200B',
        inline=True
    )

    embed.add_field(
        name="Team :red_square:",
        value='** **',
        inline=False
    )

    for red_player in game_history["team2"]['player']:
        player_name = red_player
        player_name = player_name.replace(" ", "%20")

        embed.add_field(
            name=f"{red_player}",
            value=f"[{red_player} stats.](https://www.leagueofgraphs.com/summoner/euw/{player_name})\
            \n:robot: **Champion: `{game_history['team2']['player'][red_player][0]}`**\
            \n:skull_crossbones: **K/D/A: `{game_history['team2']['player'][red_player][1]}`**\
            \n:crossed_swords: **Damage dealt: `{game_history['team2']['player'][red_player][2]}`**\
            \n:shield: **Damage taken: `{game_history['team2']['player'][red_player][3]}`**\
            \n:heart_on_fire: **Total heal: `{game_history['team2']['player'][red_player][4]}`**\
            \n:farmer: **Farming: `{game_history['team2']['player'][red_player][5]}`**\
            \n:bulb: **Vision score: `{game_history['team2']['player'][red_player][6]}`**\
            \n:moneybag: **Gold earned: `{game_history['team2']['player'][red_player][7]}`**",
            inline=True
        )

    embed.add_field(
        name='\u200B',
        value='\u200B',
        inline=True
    )

    await message.channel.send(embed=embed)
