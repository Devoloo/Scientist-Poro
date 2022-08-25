const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('invite')
        .setDescription('Invite the bot to your server.'),
	async execute(interaction) {
        const embed = new EmbedBuilder()
            .setTitle('Click here to invite the bot to your server.')
            .setURL('https://discord.com/oauth2/authorize?client_id=1004408086779416697&permissions=8&scope=bot')
            .setColor(0x000000)
            .setTimestamp()
            .setFooter({ text: '❤️' });

		return interaction.reply({ embeds: [embed] });
	},
}