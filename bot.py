import discord
from discord.ext import commands
import datetime
import config
import re

class AirdropManager(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        super().__init__(command_prefix='!', intents=intents)
        self.criteria = config.DEFAULT_CRITERIA.copy()
        
    async def setup_hook(self):
        await self.add_cog(AirdropCog(self))

class AirdropCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='setup_airdrop')
    @commands.has_permissions(administrator=True)
    async def setup_airdrop(self, ctx, preset: str = None):
        """Set up airdrop criteria using presets or default settings"""
        if preset and preset.lower() in config.PRESET_CONFIGS:
            self.bot.criteria = config.PRESET_CONFIGS[preset.lower()].copy()
            await ctx.send(f"Airdrop criteria set to {preset} preset!")
        else:
            self.bot.criteria = config.DEFAULT_CRITERIA.copy()
            await ctx.send("Airdrop criteria set to default values!")

    @commands.command(name='check_eligibility')
    async def check_eligibility(self, ctx):
        """Check if user is eligible for airdrop"""
        member = ctx.author

        # Check account age
        account_age = (datetime.datetime.now(datetime.UTC) - member.created_at).days
        if account_age < self.bot.criteria['min_account_age_days']:
            await ctx.send(f"Your account is too new. Required age: {self.bot.criteria['min_account_age_days']} days")
            print(f"Eligibility check for {member.id}: Not Eligible (Account too new)")
            return

        # Check recent activity
        last_message_time = (datetime.datetime.now(datetime.UTC) - member.last_message.created_at).days
        if last_message_time > self.bot.criteria['min_activity_days']:
            await ctx.send(f"You need to be active in the last {self.bot.criteria['min_activity_days']} days.")
            print(f"Eligibility check for {member.id}: Not Eligible (Inactive)")
            return

        # Check for alt accounts
        if self.bot.criteria['check_for_alts'] and is_alt_account(member):
            await ctx.send("Alt accounts are not eligible for the airdrop.")
            print(f"Eligibility check for {member.id}: Not Eligible (Alt Account)")
            return

        # Add role if eligible
        try:
            role = discord.utils.get(ctx.guild.roles, name=config.AIRDROP_ROLE_NAME)
            if not role:
                role = await ctx.guild.create_role(name=config.AIRDROP_ROLE_NAME)

            await member.add_roles(role)
            await ctx.send("Congratulations! You are eligible for the airdrop! 🎉")
            print(f"Eligibility check for {member.id}: Eligible")
        except discord.Forbidden:
            await ctx.send("Error: Bot doesn't have permission to manage roles!")
            print(f"Eligibility check for {member.id}: Failed (Permission Error)")

    @commands.Cog.listener()
    async def on_message(self, message):
        """Monitor tip.cc commands and airdrop claims"""
        if message.author.bot:
            return
            
        # Check for tip.cc commands
        if message.content.startswith('$tip') or message.content.startswith('$airdrop'):
            # Future implementation: Track tip amounts and frequency
            pass

        # Check for airdrop claim attempts
        if message.content.startswith('$claim'):
            member = message.author
            role = discord.utils.get(message.guild.roles, name=config.AIRDROP_ROLE_NAME)
            
            if not role or role not in member.roles:
                try:
                    # Send ephemeral message using followup
                    await message.channel.send(
                        content="❌ You are not eligible for the airdrop. Use `!check_eligibility` to check your status.",
                        delete_after=10  # Message will be deleted after 10 seconds
                    )
                    # Delete the claim attempt message if possible
                    try:
                        await message.delete()
                    except discord.Forbidden:
                        pass
                except discord.Forbidden:
                    pass
                print(f"Airdrop claim attempt by {member.id}: Not Eligible")
            else:
                print(f"Airdrop claim attempt by {member.id}: Eligible")

def is_alt_account(member):
    """Detect if a user is an alt account"""
    account_age_days = (datetime.datetime.now(datetime.UTC) - member.created_at).days
    if account_age_days < 30:  # Consider accounts younger than 30 days as alts
        return True

    # Placeholder for additional logic (e.g., shared IP detection)
    return False

def run_bot():
    bot = AirdropManager()
    bot.run(config.DISCORD_TOKEN)

if __name__ == "__main__":
    run_bot()
