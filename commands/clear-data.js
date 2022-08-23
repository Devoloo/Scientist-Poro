const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');

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
        .setName('clear-data')
        .setDescription('(Admin) Clears all data from the database.'),
	async execute(interaction) {
        if (!interaction.member.roles.cache.some(role => role.name === '*')) {
            return interaction.reply({ content: 'You do not have permission to use this command.', ephemeral: true });
        }

        DiscordRiot.sync({ force: true });

		return interaction.reply({ content: 'Data cleared!', ephemeral: true });
	},
}