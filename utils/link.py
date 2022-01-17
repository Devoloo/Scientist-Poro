import discord
from utils.riot_game_acces import foot_msg


async def link_function(message):
    embed = discord.Embed(
        title="Link",
        color=0x7CFC00
    )

    embed.add_field(
        name="Click on the link to add the bot to your server",
        value="[Add !](https://discord.com/api/oauth2/authorize?client_id=875781797651316819&permissions=8&scope=bot)",
        inline=False
    )

    embed.set_footer(
        text=foot_msg
    )

    await message.channel.send(embed=embed)
    print(f"\033[32mSend {message.channel.id} at {message.guild.id}\033[0m")
