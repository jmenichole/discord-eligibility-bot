const { Client, GatewayIntentBits } = require('discord.js');
const { ButtonBuilder, ActionRowBuilder } = require('@discordjs/button-builder');
const fs = require('fs');
require('dotenv').config();

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
    GatewayIntentBits.GuildMembers
  ],
});

let userActivity = {};
const config = JSON.parse(fs.readFileSync('./qualifierConfig.json', 'utf8'));

// Load user activity from file
function loadUserActivity() {
  if (fs.existsSync('./userActivity.json')) {
    userActivity = JSON.parse(fs.readFileSync('./userActivity.json', 'utf8'));
  }
}

// Save user activity to file
function saveUserActivity() {
  fs.writeFileSync('./userActivity.json', JSON.stringify(userActivity, null, 2));
}

// Function to detect alt accounts
function isAltAccount(userId) {
  const user = userActivity[userId];
  if (!user) return false;

  // Example logic: Check if the account was created recently
  const accountAgeDays = (new Date() - new Date(user.accountCreatedAt)) / (1000 * 60 * 60 * 24);
  if (accountAgeDays < 30) return true; // Consider accounts younger than 30 days as alts

  // Example logic: Check for shared IPs or suspicious activity (placeholder)
  // Add actual implementation if possible

  return false;
}

// Bot login
client.once('ready', () => {
  console.log('✅ Bot is online!');
  loadUserActivity();
});

// Command for airdrop
client.on('messageCreate', async (message) => {
  if (message.author.bot) return;

  if (message.content.startsWith('!airdrop')) {
    try {
      const [command, currency, amount] = message.content.split(' ');

      const collectButton = new ButtonBuilder()
        .setCustomId('collect_airdrop')
        .setLabel('Collect Airdrop')
        .setStyle('PRIMARY');

      const row = new ActionRowBuilder().addComponents(collectButton);

      message.channel.send({
        content: `💸 Airdrop for ${amount} ${currency.toUpperCase()} has arrived!`,
        components: [row]
      });
    } catch (error) {
      console.error('Error handling airdrop command:', error);
      message.reply('❌ An error occurred while processing the airdrop.');
    }
  }
});

// Handle button clicks (Collect Airdrop)
client.on('interactionCreate', async (interaction) => {
  if (!interaction.isButton()) return;

  const userId = interaction.user.id;

  if (interaction.customId === 'collect_airdrop') {
    const user = userActivity[userId];

    if (!user) {
      return interaction.reply({
        content: '❌ You are not eligible for the airdrop!',
        ephemeral: true
      });
    }

    const isQualified = checkEligibility(userId);

    if (isQualified) {
      interaction.reply(`✅ You have collected your airdrop!`);
      // Simulate sending the tip
      console.log(`Airdrop collected by ${userId}`);
    } else {
      interaction.reply({
        content: `❌ You do not meet the qualifications for this airdrop.`,
        ephemeral: true
      });
    }
  }
});

// Updated eligibility criteria with alt account detection
function checkEligibility(userId) {
  const user = userActivity[userId];
  if (!user) return false;

  const now = new Date();

  // Check account age
  const accountAgeDays = (now - new Date(user.accountCreatedAt)) / (1000 * 60 * 60 * 24);
  if (accountAgeDays < config.minAccountAgeDays) return false;

  // Check recent activity
  const lastActivity = new Date(user.lastActivity);
  const activityThreshold = new Date();
  activityThreshold.setDate(activityThreshold.getDate() - config.minActivityTimeframe);
  if (lastActivity < activityThreshold) return false;

  // Check for alt accounts or bots
  if (isAltAccount(userId) || user.isBot) return false;

  return true;
}

// Log user activity
client.on('messageCreate', (message) => {
  if (message.author.bot) return;

  const userId = message.author.id;
  if (!userActivity[userId]) {
    userActivity[userId] = {
      accountCreatedAt: message.author.createdAt,
      lastActivity: new Date(),
      isAlt: false, // Replace with actual logic to detect alts
      isBot: message.author.bot,
    };
  } else {
    userActivity[userId].lastActivity = new Date();
  }

  saveUserActivity();
});

// Log eligibility checks
client.on('messageCreate', (message) => {
  if (message.content.startsWith('!check_eligibility')) {
    const userId = message.author.id;
    const isEligible = checkEligibility(userId);

    console.log(`Eligibility check for user ${userId}: ${isEligible ? 'Eligible' : 'Not Eligible'}`);
  }
});

client.login(process.env.BOT_TOKEN);
