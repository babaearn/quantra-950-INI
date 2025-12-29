"""
Telegram Bot for Quantra-950
Provides AI trading signals via Telegram
"""
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode
from config.settings import settings
from data.binance_client import BinanceClient
from intelligence.gemini_analyzer import GeminiAnalyzer
from bot.formatters import (
    format_analysis_message,
    format_error_message,
    format_welcome_message,
    format_help_message,
    format_educational_analysis,
    format_advanced_analysis
)
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class QuantraBot:
    """Telegram bot for Quantra-950 trading signals"""

    def __init__(self, token: str = None):
        """
        Initialize Quantra bot

        Args:
            token: Telegram bot token (defaults to settings)
        """
        self.token = token or settings.TELEGRAM_BOT_TOKEN

        if not self.token:
            raise ValueError("Telegram bot token not found. Check your .env file.")

        # Initialize clients
        self.binance_client = None
        self.gemini_analyzer = None

        logger.info("✓ Quantra bot initialized")

    def _init_clients(self):
        """Initialize Binance and Gemini clients (lazy loading)"""
        if self.binance_client is None:
            logger.info("Initializing Binance client...")
            self.binance_client = BinanceClient()

        if self.gemini_analyzer is None:
            logger.info("Initializing Gemini analyzer...")
            self.gemini_analyzer = GeminiAnalyzer()

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /start command

        Args:
            update: Telegram update object
            context: Callback context
        """
        logger.info(f"User {update.effective_user.id} started the bot")

        welcome_msg = format_welcome_message()
        await update.message.reply_text(
            welcome_msg,
            parse_mode=ParseMode.MARKDOWN
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /help command

        Args:
            update: Telegram update object
            context: Callback context
        """
        logger.info(f"User {update.effective_user.id} requested help")

        help_msg = format_help_message()
        await update.message.reply_text(
            help_msg,
            parse_mode=ParseMode.MARKDOWN
        )

    async def q1_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /q1 command - Get AI analysis for a symbol

        Usage: /q1 BTC or /q1 BTCUSDT

        Args:
            update: Telegram update object
            context: Callback context
        """
        user_id = update.effective_user.id
        logger.info(f"User {user_id} requested analysis: {' '.join(context.args)}")

        try:
            # Parse symbol from command
            if not context.args:
                await update.message.reply_text(
                    "❌ Please specify a symbol!\n\n"
                    "Example: /q1 BTC or /q1 BTCUSDT",
                    parse_mode=ParseMode.MARKDOWN
                )
                return

            symbol = context.args[0].upper()

            # Normalize symbol (add USDT if needed)
            if not symbol.endswith('USDT'):
                symbol = f"{symbol}USDT"

            # Send processing message
            processing_msg = await update.message.reply_text(
                f"🔄 Analyzing {symbol}...\n"
                f"Fetching market data and generating AI analysis...",
                parse_mode=ParseMode.MARKDOWN
            )

            # Initialize clients if needed
            self._init_clients()

            # Step 1: Fetch market data from Binance
            logger.info(f"Fetching market data for {symbol}")
            market_data = self.binance_client.get_market_overview(symbol)

            # Step 2: Analyze with Gemini AI
            logger.info(f"Generating AI analysis for {symbol}")
            analysis = self.gemini_analyzer.analyze_market(market_data)

            # Step 3: Format and send response
            message = format_analysis_message(analysis, symbol)

            # Delete processing message
            await processing_msg.delete()

            # Send analysis
            await update.message.reply_text(
                message,
                parse_mode=ParseMode.MARKDOWN
            )

            logger.info(f"Successfully sent analysis for {symbol} to user {user_id}")

        except ValueError as e:
            # Handle validation errors
            error_msg = format_error_message(str(e), symbol if 'symbol' in locals() else 'UNKNOWN')
            await update.message.reply_text(
                error_msg,
                parse_mode=ParseMode.MARKDOWN
            )
            logger.error(f"Validation error for user {user_id}: {e}")

        except Exception as e:
            # Handle unexpected errors
            error_msg = format_error_message(
                f"An unexpected error occurred: {str(e)}",
                symbol if 'symbol' in locals() else 'UNKNOWN'
            )
            await update.message.reply_text(
                error_msg,
                parse_mode=ParseMode.MARKDOWN
            )
            logger.error(f"Error processing /q1 for user {user_id}: {e}", exc_info=True)

    async def q2_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /q2 command - Educational market analysis

        Usage: /q2 BTC or /q2 BTCUSDT

        Args:
            update: Telegram update object
            context: Callback context
        """
        user_id = update.effective_user.id
        logger.info(f"User {user_id} requested educational analysis: {' '.join(context.args)}")

        try:
            # Parse symbol from command
            if not context.args:
                await update.message.reply_text(
                    "❌ Please specify a symbol!\n\n"
                    "Example: /q2 BTC or /q2 BTCUSDT",
                    parse_mode=ParseMode.MARKDOWN
                )
                return

            symbol = context.args[0].upper()

            # Normalize symbol (add USDT if needed)
            if not symbol.endswith('USDT'):
                symbol = f"{symbol}USDT"

            # Send processing message
            processing_msg = await update.message.reply_text(
                f"🎓 Generating educational analysis for {symbol}...\n"
                f"Deep dive into market psychology and smart money insights...",
                parse_mode=ParseMode.MARKDOWN
            )

            # Initialize clients if needed
            self._init_clients()

            # Fetch market data from Binance
            logger.info(f"Fetching market data for {symbol}")
            market_data = self.binance_client.get_market_overview(symbol)

            # Analyze with QUANTRA-2 (Educational)
            logger.info(f"Generating educational analysis for {symbol}")
            analysis = self.gemini_analyzer.analyze_educational(market_data)

            # Format and send response
            message = format_educational_analysis(analysis, symbol)

            # Delete processing message
            await processing_msg.delete()

            # Send analysis
            await update.message.reply_text(
                message,
                parse_mode=ParseMode.MARKDOWN
            )

            logger.info(f"Successfully sent educational analysis for {symbol} to user {user_id}")

        except ValueError as e:
            error_msg = format_error_message(str(e), symbol if 'symbol' in locals() else 'UNKNOWN')
            await update.message.reply_text(error_msg, parse_mode=ParseMode.MARKDOWN)
            logger.error(f"Validation error for user {user_id}: {e}")

        except Exception as e:
            error_msg = format_error_message(
                f"An unexpected error occurred: {str(e)}",
                symbol if 'symbol' in locals() else 'UNKNOWN'
            )
            await update.message.reply_text(error_msg, parse_mode=ParseMode.MARKDOWN)
            logger.error(f"Error processing /q2 for user {user_id}: {e}", exc_info=True)

    async def q3_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /q3 command - Advanced technical analysis

        Usage: /q3 BTC or /q3 BTCUSDT

        Args:
            update: Telegram update object
            context: Callback context
        """
        user_id = update.effective_user.id
        logger.info(f"User {user_id} requested advanced analysis: {' '.join(context.args)}")

        try:
            # Parse symbol from command
            if not context.args:
                await update.message.reply_text(
                    "❌ Please specify a symbol!\n\n"
                    "Example: /q3 BTC or /q3 BTCUSDT",
                    parse_mode=ParseMode.MARKDOWN
                )
                return

            symbol = context.args[0].upper()

            # Normalize symbol (add USDT if needed)
            if not symbol.endswith('USDT'):
                symbol = f"{symbol}USDT"

            # Send processing message
            processing_msg = await update.message.reply_text(
                f"📊 Generating advanced technical analysis for {symbol}...\n"
                f"Analyzing orderbook depth, CVD trends, funding history...",
                parse_mode=ParseMode.MARKDOWN
            )

            # Initialize clients if needed
            self._init_clients()

            # Fetch market data from Binance
            logger.info(f"Fetching market data for {symbol}")
            market_data = self.binance_client.get_market_overview(symbol)

            # Analyze with QUANTRA-3 (Advanced)
            logger.info(f"Generating advanced technical analysis for {symbol}")
            analysis = self.gemini_analyzer.analyze_advanced(market_data)

            # Format and send response
            message = format_advanced_analysis(analysis, symbol)

            # Delete processing message
            await processing_msg.delete()

            # Send analysis
            await update.message.reply_text(
                message,
                parse_mode=ParseMode.MARKDOWN
            )

            logger.info(f"Successfully sent advanced analysis for {symbol} to user {user_id}")

        except ValueError as e:
            error_msg = format_error_message(str(e), symbol if 'symbol' in locals() else 'UNKNOWN')
            await update.message.reply_text(error_msg, parse_mode=ParseMode.MARKDOWN)
            logger.error(f"Validation error for user {user_id}: {e}")

        except Exception as e:
            error_msg = format_error_message(
                f"An unexpected error occurred: {str(e)}",
                symbol if 'symbol' in locals() else 'UNKNOWN'
            )
            await update.message.reply_text(error_msg, parse_mode=ParseMode.MARKDOWN)
            logger.error(f"Error processing /q3 for user {user_id}: {e}", exc_info=True)

    def run(self):
        """
        Start the bot and begin polling for messages
        """
        logger.info("Starting Quantra-950 Telegram bot...")

        # Create application
        application = Application.builder().token(self.token).build()

        # Add command handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("q1", self.q1_command))
        application.add_handler(CommandHandler("q2", self.q2_command))
        application.add_handler(CommandHandler("q3", self.q3_command))

        logger.info("✓ Bot commands registered")
        logger.info("Commands: /start, /help, /q1, /q2, /q3")

        # Start polling
        logger.info("🚀 Bot is now running. Press Ctrl+C to stop.")
        application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """Main entry point for running the bot"""
    try:
        bot = QuantraBot()
        bot.run()
    except KeyboardInterrupt:
        logger.info("\n👋 Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        raise


if __name__ == '__main__':
    main()
