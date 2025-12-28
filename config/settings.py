"""
Configuration settings for Quantra-950
Loads environment variables and provides configuration access
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    """Application settings loaded from environment variables"""

    # Binance API Configuration
    BINANCE_API_KEY = os.getenv('BINANCE_API_KEY', '')
    BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET', '')

    # Gemini AI Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

    # CoinGlass API Configuration
    COINGLASS_API_KEY = os.getenv('COINGLASS_API_KEY', '')

    # Telegram Configuration
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_USER_ID = os.getenv('TELEGRAM_USER_ID', '')

    # Trading Configuration
    DEFAULT_SYMBOL = 'BTCUSDT'
    TESTNET = os.getenv('BINANCE_TESTNET', 'False').lower() == 'true'

    @classmethod
    def validate(cls):
        """Validate that required settings are present"""
        required_fields = {
            'BINANCE_API_KEY': cls.BINANCE_API_KEY,
            'BINANCE_API_SECRET': cls.BINANCE_API_SECRET,
        }

        missing = [key for key, value in required_fields.items() if not value]

        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}\n"
                f"Please create a .env file based on .env.example"
            )

        return True

    @classmethod
    def display_config(cls):
        """Display current configuration (safely, without exposing secrets)"""
        print("=" * 50)
        print("Quantra-950 Configuration")
        print("=" * 50)
        print(f"Binance API Key: {'*' * 8}{cls.BINANCE_API_KEY[-4:] if cls.BINANCE_API_KEY else 'NOT SET'}")
        print(f"Binance Secret: {'*' * 8}{cls.BINANCE_API_SECRET[-4:] if cls.BINANCE_API_SECRET else 'NOT SET'}")
        print(f"Testnet Mode: {cls.TESTNET}")
        print(f"Default Symbol: {cls.DEFAULT_SYMBOL}")
        print("=" * 50)


# Create a singleton instance
settings = Settings()
