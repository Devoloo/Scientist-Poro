const fs = require('node:fs');
const path = require('node:path');
const colors = require('colors');

colors.enable();

const { Client, Collection, GatewayIntentBits, ActivityType  } = require('discord.js');
const { token } = require('./config.json');

const client = new Client({ intents: [GatewayIntentBits.Guilds] });

client.commands = new Collection();
const commandsPath = path.join(__dirname, 'commands');
const commandFiles = fs.readdirSync(commandsPath).filter(file => file.endsWith('.js'));

for (const file of commandFiles) {
	const filePath = path.join(commandsPath, file);
	const command = require(filePath);
	client.commands.set(command.data.name, command);
}

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

module.exports = {
	DiscordRiot: DiscordRiot,
	sequelize: sequelize,
};
//#endregion

client.once('ready', () => {
	DiscordRiot.sync();
	client.user.setActivity('League Of Legends', { type: ActivityType.Watching });
	console.log(`Logged in as ${client.user.tag}`.green);
});

client.on('interactionCreate', async interaction => {
	if (!interaction.isChatInputCommand()) return;

	const command = client.commands.get(interaction.commandName);

	if (!command) return;

	try {
		await command.execute(interaction);
	} catch (error) {
		console.error(error);
		await interaction.reply({ content: 'There was an error while executing this command!', ephemeral: true });
	}
});

client.login(token);