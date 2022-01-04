import discord
from utils.riot_game_acces import get_challenger_rank, foot_msg
from utils.error import error_riot, error_wrong_args


async def challenger_top_function(message):
    challenger_dict = get_challenger_rank('euw1')

    if type(challenger_dict) != dict:
        await error_riot(message, challenger_dict)
        return

    embed = discord.Embed(
        title="Challenger EUW top 10",
        color=0xFF5733
    )

    embed.set_author(
        name=message.author.display_name,
        icon_url=message.author.avatar_url
    )

    embed.set_footer(
        text=foot_msg
    )

    for player in challenger_dict:
        embed.add_field(
            name=player,
            value=player[player],
            inline=False
        )

    await message.channel.send(embed=embed)

    print(f"\033[32mSend {message.channel.id} at {message.guild.id}\033[0m")
