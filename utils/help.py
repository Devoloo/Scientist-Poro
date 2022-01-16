import discord
from utils.riot_game_acces import foot_msg


async def help_function(message):
    embed = discord.Embed(
        title="Help",
        color=0xFF5733
    )

    embed.add_field(
        name="Help",
        value="`!help` display this panel.",
        inline=False
    )

    embed.add_field(
        name="Link",
        value="`!link` give link to invite on your server.",
        inline=False
    )

    embed.add_field(
        name="Player ranked stats",
        value="`!player <player_name>` or `!p <player_name>` display player ranked stats in solo duo.",
        inline=False
    )

    embed.add_field(
        name="Player best champion",
        value="`!player_best <player_name>` or `!pb <player_name>` display player_name most played champion.",
        inline=False
    )

    embed.add_field(
        name="Champion stats",
        value="`!champion <champion_name>` or `!c <champion_name>` display champion stats.",
        inline=False
    )

    embed.add_field(
        name="Player last game",
        value="`!history <player_name>` or `!h <player_name>` display last game.",
        inline=False
    )

    embed.set_footer(
        text=foot_msg
    )

    await message.channel.send(embed=embed)
    print(f"\033[32mSend {message.channel.id} at {message.guild.id}\033[0m")
