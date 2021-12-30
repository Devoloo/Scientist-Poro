import discord
from utils.riot_game_acces import get_champion_stat, foot_msg, latest


async def champion_stat_function(message, msg_content):
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
    # endregion

    champion = get_champion_stat(args)

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

    # Add footer
    embed.set_footer(
        text=foot_msg
    )

    # endregion

    await message.channel.send(embed=embed)

    print(f"\033[32mSend {message.channel.id} at {message.guild.id}\033[0m")
