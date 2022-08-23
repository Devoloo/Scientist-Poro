const { SlashCommandBuilder, EmbedBuilder} = require('discord.js');
const { RiotAPI, RiotAPITypes, PlatformId } =  require('@fightmegg/riot-api');
const { riotkey } = require('../config.json');
const fetch = require('node-fetch');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('search')
        .setDescription('Search a player (EUW for now).')
        .addStringOption(option =>
            option.setName('player')
                .setDescription('The player to search.')
                .setRequired(true)),
	async execute(interaction) {
        const rAPI = new RiotAPI(riotkey);
        const latestV = await rAPI.ddragon.versions.latest();

        //#region Summoner Lookup
        var summoner;

        try {
            summoner = await rAPI.summoner.getBySummonerName({
                region: PlatformId.EUW1,
                summonerName: interaction.options.getString('player')
            });
        } catch (error) {
            return interaction.reply({ content: `${interaction.options.getString('player')} not found.`, ephemeral: true });
        }
        //#endregion

        //#region Summoner Rankeds Lookup
        var summonerData;

        try {
            const summonerUrl = `https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/${summoner.id}`;

            const headers = {
                'X-Riot-Token': riotkey
            };

            const response = await fetch(summonerUrl, { headers });
            summonerData = await response.json();
        } catch (error) {
            return interaction.reply({ content: `${interaction.options.getString('player')} stats not found.`, ephemeral: true });
        }
        //#endregion

        //#region Summoner Rank Stats Lookup
        var rankedData = summonerData.find(x => x.queueType === 'RANKED_SOLO_5x5');
        var rank;
        var win, loss, winrate;

        if (!rankedData)
            rank = { name: 'Rank', value: 'UNRANKED', inline: true };
        else {
            rank = { name: `Rank :trophy:`, value: `${rankedData.tier} ${rankedData.rank} ${rankedData.leaguePoints} LP`, inline: false };
            win = { name: `Wins :green_circle:`, value: `${rankedData.wins}`, inline: true };
            loss = { name: `Losses :red_circle:`, value: `${rankedData.losses}`, inline: true };
            winrate = { name: `Winrate :scales:`, value: `${((rankedData.wins / (rankedData.wins + rankedData.losses)) * 100).toFixed(2)}%`, inline: true };
        }

        const fields = [
            { name: 'Level :level_slider:', value: `${summoner.summonerLevel}`, inline: true },
            rank,
        ];

        if (rankedData)
            fields.push(win, loss, winrate);
        //#endregion

        //#region Summoner Last Ranked Lookup
        var lastGame;

        try {
            var historyUrl = `https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/${summoner.puuid}/ids?start=0&count=1`;

            const headers = {
                'X-Riot-Token': riotkey
            };

            const response = await fetch(historyUrl, { headers });
            lastGame = await response.json();
        } catch (error) {
            return interaction.reply({ content: `${interaction.options.getString('player')} stats not found.`, ephemeral: true });
        }

        lastGame = lastGame[0];

        var lastGameData;

        try {
            const lastGameUrl = `https://europe.api.riotgames.com/lol/match/v5/matches/${lastGame}`;

            const headers = {
                'X-Riot-Token': riotkey
            };

            const response = await fetch(lastGameUrl, { headers });
            lastGameData = await response.json();
        } catch (error) {
            return interaction.reply({ content: `${interaction.options.getString('player')} stats not found.`, ephemeral: true });
        }
        
        var blueTeam = lastGameData['metadata']['participants'].slice(0, 5);
        var redTeam = lastGameData['metadata']['participants'].slice(5, 10);

        var team;

        if (blueTeam.includes(summoner.puuid))
            team = 0;
        if (redTeam.includes(summoner.puuid))
            team = 1;
        
        var gameResult = lastGameData['info']['teams'][team]['win'];

        const gameResultField = { name: 'Last game result :video_game:', value: `${(gameResult) ? 'Win' : 'Loss'}`, inline: true };

        fields.push(gameResultField);
        //#endregion

        const icon = `http://ddragon.leagueoflegends.com/cdn/${latestV}/img/profileicon/${summoner.profileIconId}.png`

		const embed = new EmbedBuilder()
            .setTitle(`${summoner.name}'s profile`)
            .setColor(0x000000)
            .setThumbnail(icon)
            .addFields(fields)
            .setTimestamp()
            .setFooter({ text: '❤️' });

		return interaction.reply({ embeds: [embed] });
	},
}