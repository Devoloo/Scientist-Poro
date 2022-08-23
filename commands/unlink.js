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
        .setName('unlink')
        .setDescription('Unlink your Discord account and your League of Legends.'),
	async execute(interaction) {
        const discordId = interaction.user.id;

        const link = await DiscordRiot.destroy({ where: { discordId: discordId } });

        if (!link) return interaction.reply({ content: `You are not linked.`, ephemeral: true });

        const embed = new EmbedBuilder()
            .setTitle('Unlinked!')
            .setColor(0x000000)
            .setDescription('> You have been unlinked. :link: :hammer:')
            .setTimestamp()
			.setFooter({ text: '❤️' });

		return interaction.reply({ embeds: [embed] });
	},
}