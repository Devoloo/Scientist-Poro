import discord
from utils.riot_game_acces import get_player_stat, foot_msg, latest
from utils.error import error_riot, error_wrong_args


async def player_ranked_stat_function(message, msg_content):
    if len(msg_content) == 1:
        await error_wrong_args(message)
        return

    args = ""
    for arg in msg_content[1:]:
        args += f"{arg} "
    args = args[:len(args) - 1]

    player_stat = get_player_stat("euw1", args)

    if type(player_stat) != dict:
        await error_riot(message, player_stat)
        return

    player_url = args.lower()
    player_url = player_url.replace(" ", "%20")

    url = f"https://www.leagueofgraphs.com/summoner/euw/{player_url}"

    embed = discord.Embed(
        title=f"Link for {player_stat['username']} :link:",
        url=url,
        color=0xFF5733
    )

    embed.set_author(
        name=message.author.display_name,
        icon_url=message.author.avatar_url
    )

    embed.set_thumbnail(
        url=f"http://ddragon.leagueoflegends.com/cdn/{latest}/img/profileicon/{player_stat['icon']}"
    )

    embed.add_field(
        name="Level :level_slider:",
        value=player_stat['level'],
        inline=False
    )

    embed.set_footer(
        text=foot_msg
    )

    # region RANKED_FLEX_SR
    embed.add_field(
        name=">>> Ranked Flex",
        value="Here stats for ranked flex !",
        inline=True
    )

    if 'RANKED_FLEX_SR' in player_stat:
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
    else:
        embed.add_field(
            name="Rank :trophy:",
            value="Unranked",
            inline=False
        )
    # endregion

    # region RANKED_SOLO_5x5
    embed.add_field(
        name=">>> Ranked Solo/Duo",
        value="Here stats for ranked solo/duo !",
        inline=True
    )

    if 'RANKED_SOLO_5x5' in player_stat:
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
    else:
        embed.add_field(
            name="Rank :military_medal:",
            value="Unranked",
            inline=False
        )
    # endregion

    await message.channel.send(embed=embed)

    print(f"\033[32mSend {message.channel.id} at {message.guild.id}\033[0m")
