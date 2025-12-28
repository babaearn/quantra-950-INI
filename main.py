#!/usr/bin/env python3
"""
Quantra-950 - AI-Powered Crypto Trading Intelligence Bot
Main entry point for running the Telegram bot
"""
from bot.telegram_bot import QuantraBot
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point"""
    print("=" * 60)
    print("  🚀 QUANTRA-950")
    print("  AI-Powered Crypto Trading Intelligence Bot")
    print("=" * 60)
    print()

    try:
        # Initialize and run bot
        bot = QuantraBot()
        bot.run()

    except KeyboardInterrupt:
        print("\n")
        print("=" * 60)
        print("  👋 Bot stopped by user")
        print("=" * 60)

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print("\n")
        print("=" * 60)
        print(f"  ❌ Fatal error: {e}")
        print("=" * 60)
        raise


if __name__ == '__main__':
    main()
