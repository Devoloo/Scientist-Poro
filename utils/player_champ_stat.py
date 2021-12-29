import discord
from utils.riot_game_acces import get_most_played_champion, foot_msg


async def player_champ_stat_function(message, msg_content):
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

    embed.set_footer(
        text=foot_msg
    )
    # endregion

    await message.channel.send(embed=embed)

    print(f"\033[32mSend {message.channel.id} at {message.guild.id}\033[0m")
