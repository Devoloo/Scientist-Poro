import discord
from utils.riot_game_acces import get_player_stat, foot_msg


async def player_ranked_stat_function(message, msg_content):
    # region Error
    if len(msg_content) == 1:
        embed = discord.Embed(
            title='Error',
            description=f"Usage: `!player/!p <player_name>`",
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

    player_stat = get_player_stat("euw1", args)

    # region Player not found
    if player_stat == None:
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
    player_url = ""
    for w in msg_content[1:]:
        player_url += f"{w}%20"

    opgg_url = f"https://euw.op.gg/summoner/userName={player_url}"

    embed = discord.Embed(
        title=f"OPGG link for {player_stat['username']}",
        url=opgg_url,
        color=0xFF5733
    )

    embed.set_author(
        name=message.author.display_name,
        icon_url=message.author.avatar_url
    )

    embed.set_thumbnail(
        url=f"https://raw.githubusercontent.com/Devoloo/Scientist-Poro/main/riot_data/11.24.1/img/profileicon/{player_stat['icon']}"
    )

    embed.add_field(
        name="Level :level_slider:",
        value=player_stat['level'],
        inline=False
    )

    embed.set_footer(
        text=foot_msg
    )
    # endregion

    # region RANKED_FLEX_SR
    if 'RANKED_FLEX_SR' in player_stat:
        embed.add_field(
            name=">>> Ranked Flex",
            value="Here stats for ranked flex !",
            inline=True
        )

        embed.add_field(
            name="Rank :trophy:",
            value=player_stat['RANKED_FLEX_SR'],
            inline=False
        )

        embed.add_field(
            name="Wins :white_check_mark:",
            value=player_stat['RANKED_FLEX_SR_WIN'],
            inline=True
        )

        embed.add_field(
            name="Losses :x:",
            value=player_stat['RANKED_FLEX_SR_LOSSE'],
            inline=True
        )

        embed.add_field(
            name="Rate :computer:",
            value=player_stat['RANKED_FLEX_SR_RATE'],
            inline=True
        )
    # endregion

    # region RANKED_SOLO_5x5
    if 'RANKED_SOLO_5x5' in player_stat:
        embed.add_field(
            name=">>> Ranked Solo/Duo",
            value="Here stats for ranked solo/duo !",
            inline=True
        )

        embed.add_field(
            name="Rank :military_medal:",
            value=player_stat['RANKED_SOLO_5x5'],
            inline=False
        )

        embed.add_field(
            name="Wins :white_check_mark:",
            value=player_stat['RANKED_SOLO_5x5_WIN'],
            inline=True
        )

        embed.add_field(
            name="Losses :x:",
            value=player_stat['RANKED_SOLO_5x5_LOSSE'],
            inline=True
        )

        embed.add_field(
            name="Rate :computer:",
            value=player_stat['RANKED_SOLO_5x5_RATE'],
            inline=True
        )
    # endregion

    await message.channel.send(embed=embed)

    print(f"\033[32mSend {message.channel.id} at {message.guild.id}\033[0m")
