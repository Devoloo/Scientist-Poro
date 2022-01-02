import discord
from utils.riot_game_acces import get_most_played_champion, foot_msg, latest
from utils.error import error_riot, error_wrong_args


async def player_champ_stat_function(message, msg_content):
    if len(msg_content) == 1:
        await error_wrong_args(message)
        return

    args = ""
    for arg in msg_content[1:]:
        args += f"{arg} "
    args = args[:len(args) - 1]

    most_played = get_most_played_champion('euw1', args)

    if type(most_played) != dict:
        await error_riot(message, most_played)
        return

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
        url=f"https://ddragon.leagueoflegends.com/cdn/img/champion/tiles/{champion_name}_0.jpg"
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

    embed.set_footer(
        text=foot_msg
    )

    await message.channel.send(embed=embed)

    print(f"\033[32mSend {message.channel.id} at {message.guild.id}\033[0m")
