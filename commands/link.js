const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');
const { RiotAPI, RiotAPITypes, PlatformId } =  require('@fightmegg/riot-api');
const { riotkey } = require('../config.json');

//#region Create table
const Sequelize = require('sequelize');

const sequelize = new Sequelize('database', 'user', 'password', {
	host: 'localhost',
	dialect: 'sqlite',
	logging: false,
	// SQLite only
	storage: 'database.sqlite',
});

const DiscordRiot = sequelize.define('DiscordRiot', {
	discordId: {
		type: Sequelize.STRING,
		primaryKey: true,
		unique: true,
	},
	riotId: {
		type: Sequelize.STRING,
		primaryKey: true,
		unique: true,
	},
});
//#endregion

module.exports = {
    data: new SlashCommandBuilder()
        .setName('link')
        .setDescription('Link your Discord account to your League of Legends account.')
        .addStringOption(option =>
            option.setName('player')
                .setDescription('The player to link.')
                .setRequired(true)),
	async execute(interaction) {
        const rAPI = new RiotAPI(riotkey);

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

        const discordId = `${interaction.user.id}`;
        const riotId = `${summoner.accountId}`;

        try {
            await DiscordRiot.create({
                discordId: discordId,
                riotId: riotId,
            });

            const embed = new EmbedBuilder()
                .setTitle('Linked!')
                .setColor(0x000000)
                .setDescription(`> You have been linked to ${summoner.name} :link:`)
                .setTimestamp()
                .setFooter({ text: '❤️' });

		    return interaction.reply({ embeds: [embed] });
        } catch (error) {
            if (error.name === 'SequelizeUniqueConstraintError')
                return interaction.reply({ content: 'You are already linked.', ephemeral: true });
            return interaction.reply({ content: 'There was an error while linking your account!', ephemeral: true });
        }
	},
}