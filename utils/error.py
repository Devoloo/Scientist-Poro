import discord
from utils.riot_game_acces import foot_msg


async def error_wrong_args(message):
    embed = discord.Embed(
        title='Error',
        description=f"Usage: `!champion/!c <champion_name>`",
        color=0x7CFC00
    )

    embed.set_footer(
        text=foot_msg
    )

    await message.channel.send(embed=embed)
    print(
        f"\033[32mSend {message.channel.id} at {message.guild.id}\033[0m")


async def error_riot(message, err):
    if err == 666:
        err = "Champion not found"

    embed = discord.Embed(
        title='Error',
        description=f"{err}",
        color=0x7CFC00
    )

    embed.set_footer(
        text=foot_msg
    )

    await message.channel.send(embed=embed)
    print(
        f"\033[32mSend {message.channel.id} at {message.guild.id}\033[0m")
