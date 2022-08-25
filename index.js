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

global.guilds = [];

async function deployAll() {
	for (const guild of guilds) {
		const deploy = require('./deploy-commands.js').deployCommands;
		await deploy(guild);
	}
}

client.once('ready', () => {
	DiscordRiot.sync();
	client.user.setActivity('League Of Legends', { type: ActivityType.Watching });
	console.log(`Logged in as ${client.user.tag}`.green);

	const guildsReboot = client.guilds.cache.map(guild => guild.id);
	guilds = guildsReboot;
	console.log(`Guilds: ${guilds}`.magenta);

	//#region Deploy all commands
	deployAll();
	//#endregion

	//#region Clear all commands
	// const clear = require('./deploy-commands.js').clearCommands;
	// clear(client);
	//#endregion
});

client.on("guildCreate", guild => {
	console.log(`Guild add `.red + ` (id: ${guild.id})`.blue);

	guilds.push(guild.id);

	const deploy = require('./deploy-commands.js').deployCommands;
	deploy(guild.id);
}).on("guildDelete", guild => {
	console.log(`I have been removed from ${guild.name}`.red + ` (id: ${guild.id})`.blue);

	guilds.splice(guilds.indexOf(guild.id), 1);
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