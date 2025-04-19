import os
from dotenv import load_dotenv

load_dotenv()

# Bot configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Role configuration
AIRDROP_ROLE_NAME = "Airdrop Eligible"

# Default criteria
DEFAULT_CRITERIA = {
    'min_activity_days': 5,  # Minimum activity in the last 5 days
    'min_account_age_days': 10,  # Minimum account age in days
    'check_for_alts': True,  # Check for alternate accounts
    'exclude_bots': True,  # Exclude bot accounts
}

# Preset configurations
PRESET_CONFIGS = {
    'strict': {
        'min_messages': 100,
        'min_account_age_days': 60,
        'requires_verification': True,
        'min_tip_commands': 10,
        'min_tip_amount': 5.0,
    },
    'lax': {
        'min_messages': 20,
        'min_account_age_days': 15,
        'requires_verification': True,
        'min_tip_commands': 3,
        'min_tip_amount': 0.5,
    }
}
