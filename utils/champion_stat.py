import discord
from utils.riot_game_acces import get_champion_stat, foot_msg


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

    # endregion

    await message.channel.send(embed=embed)

    print(f"\033[32mSend {message.channel.id} at {message.guild.id}\033[0m")
