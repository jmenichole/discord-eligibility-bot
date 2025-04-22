AirdropGatekeeper

A Discord bot that verifies users as eligible for airdrops and assigns them the "Airdrop Eligible" role based on configurable criteria.

## Setup

1. Create a `.env` file with your Discord bot token:
   ```
   DISCORD_TOKEN=your-bot-token
   ```

2. Configure eligibility criteria in `qualifierConfig.json`:
   - `min_messages`: Minimum number of messages in the last 30 days.
   - `min_account_age_days`: Minimum account age in days.
   - `min_tip_commands`: Minimum number of tip commands used.
   - `min_tip_amount`: Minimum amount tipped.
   - `min_activity_days`: Minimum activity in the last X days.
   - `check_for_alts`: Whether to exclude alt accounts.
   - `exclude_bots`: Whether to exclude bots.

3. Run the bot:
   ```
   node index.js
   ```

## Troubleshooting

1. **Bot Not Responding**:
   - Ensure the bot is online and has the correct token in the `.env` file.
   - Check if the bot has the necessary permissions (e.g., `Manage Roles`, `Read Messages`, `Send Messages`).

2. **Eligibility Issues**:
   - Verify that the criteria in `qualifierConfig.json` or `config.py` match your requirements.
   - Ensure the user activity data is being logged correctly.

3. **Alt Account Detection**:
   - The bot uses basic logic to detect alt accounts (e.g., account age). For advanced detection, implement additional checks (e.g., shared IPs).

4. **Role Assignment Errors**:
   - Ensure the bot has permission to manage roles in the server.
   - Check if the "Airdrop Eligible" role exists or can be created by the bot.

5. **Logging**:
   - Logs for eligibility checks and airdrop claims are printed to the console. Redirect output to a file if needed:
     ```
     node index.js > bot.log
     ```
