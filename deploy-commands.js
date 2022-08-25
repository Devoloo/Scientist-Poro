const fs = require('node:fs');
const path = require('node:path');
const colors = require('colors');

colors.enable();

const { REST } = require('@discordjs/rest');
const { Routes } = require('discord.js');
const { clientId, token } = require('./config.json');

const commands = [];
const commandsPath = path.join(__dirname, 'commands');
const commandFiles = fs.readdirSync(commandsPath).filter(file => file.endsWith('.js'));

for (const file of commandFiles) {
	const filePath = path.join(commandsPath, file);
	const command = require(filePath);

	console.log(`Registering command ${command.data.name}...`.yellow.bgMagenta);

	commands.push(command.data.toJSON());
}

const rest = new REST({ version: '10' }).setToken(token);

async function deployCommands(guildId) {
	console.log(`Deploying commands for guild ${guildId}...`.yellow.bgRed);
	await rest.put(Routes.applicationGuildCommands(clientId, guildId), { body: commands })
		.then(() => console.log(`Successfully registered application commands on :`.green + `(id: ${guildId})`.blue))
		.catch(console.error);
}

async function clearCommands(client) {
	console.log(`Clearing commands for all guilds...`.yellow.bgRed);
	await client.application.commands.set([]);
}

module.exports = {
	deployCommands: deployCommands,
	clearCommands: clearCommands,
};