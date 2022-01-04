from riotwatcher import ApiError, LolWatcher
import yaml

with open('config.yaml', 'r') as stream:
    token_list = yaml.safe_load(stream)

riot_token = token_list['riot']

# Riot api key
api_key = riot_token
watcher = LolWatcher(api_key)

# Global
latest = watcher.data_dragon.versions_for_region('euw1')['n']['champion']
foot_msg = f"Developed with ♥ by mattyeux (patch {latest})."


def get_player_stat(region, player):
    """
    Return a dict with all player stat (for solor_duo actually)
    Player username
    Player account icon
    Player current rank
    Player wins losses
    """
    player = player.lower()

    # Check error while searching player in euw1
    try:
        current_player = watcher.summoner.by_name(region, player)
    except ApiError as err:
        print(f"\033[31mError {err}\033[0m")
        return err

    ranked_stats = watcher.league.by_summoner(region, current_player['id'])

    player_icon = f"{current_player['profileIconId']}.png"
    player_level = current_player['summonerLevel']

    stat = {'username': f"{player}",
            'icon': f"{player_icon}", 'level': f"{player_level}"}

    for d in ranked_stats:
        queueType = d['queueType']
        if queueType == 'RANKED_FLEX_SR':
            stat['RANKED_FLEX_SR'] = f"{d['tier'][0]}{d['tier'][1:].lower()} {d['rank']}"
            stat['RANKED_FLEX_SR_WIN'] = f"{d['wins']}"
            stat['RANKED_FLEX_SR_LOSSE'] = f"{d['losses']}"
            rate = (int(d['wins']) / (int(d['wins']) + int(d['losses']))) * 100
            stat['RANKED_FLEX_SR_RATE'] = f"{format(rate, '.2f')} %"
        if queueType == 'RANKED_SOLO_5x5':
            stat['RANKED_SOLO_5x5'] = f"{d['tier'][0]}{d['tier'][1:].lower()} {d['rank']}"
            stat['RANKED_SOLO_5x5_WIN'] = f"{d['wins']}"
            stat['RANKED_SOLO_5x5_LOSSE'] = f"{d['losses']}"
            rate = (int(d['wins']) / (int(d['wins']) + int(d['losses']))) * 100
            stat['RANKED_SOLO_5x5_RATE'] = f"{format(rate, '.2f')} %"

    return stat


def get_most_played_champion(region, player, best=0):
    player = player.lower()

    # Check error while searching player in euw1
    try:
        current_player = watcher.summoner.by_name(region, player)
    except ApiError as err:
        print(f"\033[31mError {err}\033[0m")
        return err

    champion_mastery = watcher.champion_mastery.by_summoner(
        region, current_player['id'])
    most_played = champion_mastery[best]

    latest = watcher.data_dragon.versions_for_region(region)['n']['champion']
    static_champ_list = watcher.data_dragon.champions(latest, False, 'en_US')

    champ_dict = {}
    for key in static_champ_list['data']:
        current_champ = static_champ_list['data'][key]
        champ_dict[f"{static_champ_list['data'][key]['key']}"] = current_champ

    champ_stat = champ_dict[f"{most_played['championId']}"]

    most_played_dict = {
        'total': watcher.champion_mastery.scores_by_summoner(region, current_player['id']),
        'name': champ_stat['name'],
        'title': champ_stat['title'],
        'blurb': champ_stat['blurb'],
        'championLevel': most_played['championLevel'],
        'championPoints': most_played['championPoints']
    }

    return most_played_dict


def get_champion_stat(champion):
    champion = champion.lower()

    latest = watcher.data_dragon.versions_for_region('euw1')['n']['champion']
    static_champ_list = watcher.data_dragon.champions(latest, False, 'en_US')

    champ_dict = {}
    for key in static_champ_list['data']:
        current_champ_stat = static_champ_list['data'][key]
        champ_dict[f"{key.lower()}"] = current_champ_stat

    if not (champion in champ_dict):
        print(
            f"\033[31mError {champion} not in dict\033[0m")
        return 666

    current_champion = champ_dict[champion]
    current_champion_stat = current_champion['stats']

    champ_dict_stat = {
        'name': current_champion['name'],
        'title': current_champion['title'],
        'blurb': current_champion['blurb'],
        'hp': current_champion_stat['hp'],
        'attackspeed': current_champion_stat['attackspeed'],
        'armor': current_champion_stat['armor'],
        'spellblock': current_champion_stat['spellblock'],
        'attackrange': current_champion_stat['attackrange'],
        'attackdamage': current_champion_stat['attackdamage'],
    }

    return champ_dict_stat


def get_challenger_rank(region):
    try:
        challenger_list = watcher.leagueoflegends.entries(
            region, "RANKED_SOLO_5x5", "CHALLENGER", "I")
    except ApiError as err:
        print(f"\033[31mError {err}\033[0m")
        return err

    challenger_dict = {}

    index = 0
    for player in challenger_list:
        if index == 10:
            break
        index += 1
        challenger_dict[challenger_list['summonerName']] = challenger_list['leaguePoints']

    return challenger_list
