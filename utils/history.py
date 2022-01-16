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

    embed = discord.Embed(
        title=f"{args}'s last game :link:",
        url=url,
        color=0xFF5733
    )

    embed.set_author(
        name=message.author.display_name,
        icon_url=message.author.avatar_url
    )

    embed.set_footer(
        text=foot_msg
    )

    team = 1

    embed.add_field(
        name="Team :blue_square:",
        value="**------------------------------------------------------------------------**",
        inline=False
    )

    for player in game_history:
        if player == "team1" or player == "team2":
            continue
        team += 1

        player_name = player
        player_name = player_name.replace(" ", "%20")

        embed.add_field(
            name=f"{player}",
            value=f"[{player} stats.](https://www.leagueofgraphs.com/summoner/euw/{player_name})\
            \n:robot: **Champion: `{game_history[player][0]}`**, :skull_crossbones: **K/D/A: `{game_history[player][1]}`**\
            \n:crossed_swords: **Damage dealt: `{game_history[player][2]}`**, :shield: **Damage taken: `{game_history[player][3]}`**, :heart_on_fire: **Total heal: `{game_history[player][4]}`**\
            \n:farmer: **Farming: `{game_history[player][5]}`**, :bulb: **Vision score: `{game_history[player][6]}`**, :moneybag: **Gold earned: `{game_history[player][7]}`**",
            inline=False
        )

        if team == 6:
            embed.add_field(
            name="Team :red_square:",
            value="**------------------------------------------------------------------------**",
            inline=False
            )
    
    if game_history["team1"] == "true":
        embed.add_field(
            name="Team :blue_square: win !",
            value="** **",
            inline=False
        )
    else:
        embed.add_field(
            name="**------------------------------------------------------------------------**",
            value="**Team :red_square: win !**",
            inline=False
        )

    await message.channel.send(embed=embed)