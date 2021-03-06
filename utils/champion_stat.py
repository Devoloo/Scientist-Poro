import discord
from utils.riot_game_acces import get_champion_stat, foot_msg, latest
from utils.error import error_riot, error_wrong_args

async def champion_stat_function(message, msg_content):
    if len(msg_content) == 1:
        await error_wrong_args(message)
        return

    args = ""
    for arg in msg_content[1:]:
        args += f"{arg} "
    args = args[:len(args) - 1]

    champion = get_champion_stat(args)

    if type(champion) != dict:
        await error_riot(message, champion)
        return

    champion_name = args.lower()
    champion_name = champion_name.replace(" ", "%20")
    url = f"https://www.leagueofgraphs.com/champions/builds/{champion_name}"

    embed = discord.Embed(
        title=f"{champion['name']} :link:",
        url=url,
        description=f"\"*{champion['title']}*\"",
        color=0x7CFC00
    )

    embed.set_author(
        name=message.author.display_name,
        icon_url=message.author.avatar_url
    )

    champion_name = champion['name']
    champion_name = champion_name.replace(" ", "")

    embed.set_thumbnail(
        url=f"https://ddragon.leagueoflegends.com/cdn/img/champion/tiles/{champion_name}_0.jpg"
    )

    embed.add_field(
        name="Short history :book:",
        value=champion['blurb'],
        inline=False
    )

    embed.add_field(
        name="<:health:926031096540430367> Health",
        value=champion['hp'],
        inline=True
    )

    embed.add_field(
        name="<:attackspeed:926031096502710272> Attack speed",
        value=champion['attackspeed'],
        inline=True
    )

    embed.add_field(
        name="<:armor:926031096121024564> Armor",
        value=champion['armor'],
        inline=True
    )

    embed.add_field(
        name="<:spellblock:926031096574013460> Magic resit",
        value=champion['spellblock'],
        inline=True
    )

    embed.add_field(
        name="<:range:926031096540438528> Attack range",
        value=champion['attackrange'],
        inline=True
    )

    embed.add_field(
        name="<:damage:926031096246849577> Attack damage",
        value=champion['attackdamage'],
        inline=True
    )

    embed.set_footer(
        text=foot_msg
    )

    await message.channel.send(embed=embed)

    print(f"\033[32mSend {message.channel.id} at {message.guild.id}\033[0m")
