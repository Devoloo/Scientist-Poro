const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('help')
        .setDescription('Get some help.'),
	async execute(interaction) {
        const commands = interaction.client.commands.map(c => c.data)
            .map(c => { return { name: `:arrow_right: ${c.name}`, value: c.description } });

        const embed = new EmbedBuilder()
            .setTitle('Commands')
            .setColor(0x000000)
            .addFields(commands)
            .setTimestamp()
            .setFooter({ text: '❤️' });

		return interaction.reply({ embeds: [embed] });
	},
}