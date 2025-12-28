"""
Test suite for Telegram bot
Tests bot initialization and message formatting
"""
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from bot.formatters import (
    format_analysis_message,
    format_error_message,
    format_welcome_message,
    format_help_message
)
from bot.telegram_bot import QuantraBot
from config.settings import settings


def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def test_telegram_configuration():
    """Test 1: Verify Telegram bot configuration"""
    print_header("TEST 1: Telegram Bot Configuration")

    try:
        if not settings.TELEGRAM_BOT_TOKEN:
            print("⚠️  Warning: TELEGRAM_BOT_TOKEN not found in environment")
            print("   This is okay for testing formatters, but bot won't run")
            return True

        print(f"✓ Telegram Bot Token: {'*' * 8}{settings.TELEGRAM_BOT_TOKEN[-4:] if len(settings.TELEGRAM_BOT_TOKEN) > 4 else '****'}")

        if settings.TELEGRAM_USER_ID:
            print(f"✓ Telegram User ID: {settings.TELEGRAM_USER_ID}")

        print("✓ Telegram configuration test PASSED")
        return True
    except Exception as e:
        print(f"✗ Telegram configuration test FAILED: {e}")
        return False


def test_formatters():
    """Test 2: Test message formatters"""
    print_header("TEST 2: Message Formatters")

    try:
        # Test welcome message
        print("\n📝 Testing welcome message formatter...")
        welcome = format_welcome_message()
        assert len(welcome) > 0
        assert "QUANTRA-950" in welcome
        assert "/q1" in welcome
        print(f"✓ Welcome message: {len(welcome)} characters")

        # Test help message
        print("\n📝 Testing help message formatter...")
        help_msg = format_help_message()
        assert len(help_msg) > 0
        assert "COMMANDS" in help_msg
        print(f"✓ Help message: {len(help_msg)} characters")

        # Test error message
        print("\n📝 Testing error message formatter...")
        error = format_error_message("Test error", "BTCUSDT")
        assert len(error) > 0
        assert "ERROR" in error
        assert "Test error" in error
        print(f"✓ Error message: {len(error)} characters")

        print("\n✓ Message formatters test PASSED")
        return True
    except Exception as e:
        print(f"\n✗ Message formatters test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_analysis_formatter_long():
    """Test 3: Test analysis formatter with LONG signal"""
    print_header("TEST 3: Analysis Formatter (LONG Signal)")

    try:
        # Create sample LONG analysis
        sample_analysis = {
            "signal": "LONG",
            "confidence": 85,
            "entry_price": 95450.00,
            "stop_loss": 94200.00,
            "targets": {
                "tp1": 96800.00,
                "tp2": 98500.00,
                "tp3": 101200.00
            },
            "risk_reward_ratio": 3.45,
            "timeframe_alignment": {
                "8h": "BULLISH",
                "4h": "BULLISH",
                "1h": "NEUTRAL"
            },
            "key_levels": {
                "resistance": [96800, 98500, 101000],
                "support": [94200, 92500, 90000]
            },
            "market_regime": "TRENDING",
            "narrative": "Bitcoin showing strong bullish momentum with rising OI. Entry on pullback.",
            "warnings": ["Watch for funding rate spike"],
            "_metadata": {
                "model": "gemini-2.5-flash-lite",
                "analyzed_at": "2024-01-15T14:32:45",
                "symbol": "BTCUSDT"
            }
        }

        message = format_analysis_message(sample_analysis, "BTCUSDT")

        # Validate message content
        assert "🟢" in message  # LONG emoji
        assert "LONG" in message
        assert "85/100" in message
        assert "$95,450.00" in message
        assert "$94,200.00" in message
        assert "TP1" in message
        assert "gemini-2.5-flash-lite" in message

        print("\n📊 Sample LONG Signal Message:")
        print("-" * 80)
        print(message)
        print("-" * 80)

        print(f"\n✓ Message length: {len(message)} characters")
        print("✓ Analysis formatter (LONG) test PASSED")
        return True
    except Exception as e:
        print(f"\n✗ Analysis formatter (LONG) test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_analysis_formatter_neutral():
    """Test 4: Test analysis formatter with NEUTRAL signal"""
    print_header("TEST 4: Analysis Formatter (NEUTRAL Signal)")

    try:
        # Create sample NEUTRAL analysis (with null values)
        sample_analysis = {
            "signal": "NEUTRAL",
            "confidence": 45,
            "entry_price": None,
            "stop_loss": None,
            "targets": None,
            "risk_reward_ratio": None,
            "timeframe_alignment": {
                "8h": "NEUTRAL",
                "4h": "BULLISH",
                "1h": "BEARISH"
            },
            "key_levels": {
                "resistance": [96500, 98000],
                "support": [94000, 92000]
            },
            "market_regime": "RANGING",
            "narrative": "Conflicting signals across timeframes. No clear edge detected. Wait for better setup.",
            "warnings": ["Choppy price action", "High risk of whipsaws"],
            "_metadata": {
                "model": "gemini-2.5-flash-lite",
                "analyzed_at": "2024-01-15T14:35:20",
                "symbol": "BTCUSDT"
            }
        }

        message = format_analysis_message(sample_analysis, "BTCUSDT")

        # Validate message content
        assert "🟡" in message  # NEUTRAL emoji
        assert "NEUTRAL" in message
        assert "45/100" in message
        assert "N/A" in message  # Should show N/A for null values
        assert "n/a" in message.lower()  # Check for N/A values

        print("\n📊 Sample NEUTRAL Signal Message:")
        print("-" * 80)
        print(message)
        print("-" * 80)

        print(f"\n✓ Message length: {len(message)} characters")
        print("✓ Analysis formatter (NEUTRAL) test PASSED")
        return True
    except Exception as e:
        print(f"\n✗ Analysis formatter (NEUTRAL) test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_bot_initialization():
    """Test 5: Test bot initialization"""
    print_header("TEST 5: Bot Initialization")

    try:
        if not settings.TELEGRAM_BOT_TOKEN:
            print("⚠️  Skipping bot initialization test (no token configured)")
            print("   This is expected in test environments")
            return True

        print("\n🤖 Initializing bot...")
        bot = QuantraBot()

        assert bot.token is not None
        assert bot.binance_client is None  # Lazy loading
        assert bot.gemini_analyzer is None  # Lazy loading

        print("✓ Bot initialized successfully")
        print("✓ Clients set to lazy loading (initialized on first use)")
        print("✓ Bot initialization test PASSED")
        return True
    except Exception as e:
        print(f"\n✗ Bot initialization test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests and display summary"""
    print("\n" + "📱" * 40)
    print("  QUANTRA-950 TELEGRAM BOT TEST SUITE")
    print("📱" * 40)

    results = []

    # Test 1: Configuration
    results.append(('Telegram Configuration', test_telegram_configuration()))

    # Test 2: Formatters
    results.append(('Message Formatters', test_formatters()))

    # Test 3: LONG signal formatter
    results.append(('Analysis Formatter (LONG)', test_analysis_formatter_long()))

    # Test 4: NEUTRAL signal formatter
    results.append(('Analysis Formatter (NEUTRAL)', test_analysis_formatter_neutral()))

    # Test 5: Bot initialization
    results.append(('Bot Initialization', test_bot_initialization()))

    # Print summary
    print_header("TEST SUMMARY")
    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status} - {test_name}")

    print("\n" + "=" * 80)
    print(f"  Results: {passed}/{total} tests passed")
    print("=" * 80)

    if passed == total:
        print("\n🎉 All tests passed! Telegram bot is ready to use.")
        print("\n💡 Next Steps:")
        print("   1. Set TELEGRAM_BOT_TOKEN in .env")
        print("   2. Run: python main.py")
        print("   3. Send /start to your bot on Telegram")
        print("   4. Send /q1 BTC to get AI analysis")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
