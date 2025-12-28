"""
Test suite for Binance API wrapper
Tests all methods with BTC/USDT and displays results
"""
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from data.binance_client import BinanceClient
from config.settings import settings
import json
from datetime import datetime


def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_data(data, indent=2):
    """Pretty print data"""
    print(json.dumps(data, indent=indent, default=str))


def test_configuration():
    """Test 1: Verify configuration is loaded"""
    print_header("TEST 1: Configuration Verification")

    try:
        settings.validate()
        settings.display_config()
        print("\n✓ Configuration test PASSED")
        return True
    except Exception as e:
        print(f"\n✗ Configuration test FAILED: {e}")
        return False


def test_client_initialization():
    """Test 2: Initialize Binance client"""
    print_header("TEST 2: Binance Client Initialization")

    try:
        client = BinanceClient()
        print("✓ Client initialization test PASSED")
        return client
    except Exception as e:
        print(f"✗ Client initialization test FAILED: {e}")
        return None


def test_futures_ticker(client, symbol='BTCUSDT'):
    """Test 3: Get futures ticker data"""
    print_header(f"TEST 3: Futures Ticker - {symbol}")

    try:
        data = client.get_futures_ticker(symbol)
        print(f"\n📈 Current Price: ${data['last_price']:,.2f}")
        print(f"24h Change: {data['price_change_percent']:+.2f}%")
        print(f"24h High: ${data['high_price']:,.2f}")
        print(f"24h Low: ${data['low_price']:,.2f}")
        print(f"24h Volume: {data['volume']:,.2f} BTC")
        print(f"24h Quote Volume: ${data['quote_volume']:,.2f}")

        print(f"\n✓ Futures ticker test PASSED")
        return True
    except Exception as e:
        print(f"\n✗ Futures ticker test FAILED: {e}")
        return False


def test_open_interest(client, symbol='BTCUSDT'):
    """Test 4: Get open interest data"""
    print_header(f"TEST 4: Open Interest - {symbol}")

    try:
        data = client.get_open_interest(symbol)
        print(f"\n📊 Open Interest: {data['open_interest']:,.2f} BTC")
        print(f"OI Value: ${data['open_interest_value']:,.2f}")
        print(f"Current Price: ${data['current_price']:,.2f}")

        print(f"\n✓ Open interest test PASSED")
        return True
    except Exception as e:
        print(f"\n✗ Open interest test FAILED: {e}")
        return False


def test_funding_rate(client, symbol='BTCUSDT'):
    """Test 5: Get funding rate"""
    print_header(f"TEST 5: Funding Rate - {symbol}")

    try:
        data = client.get_funding_rate(symbol)
        print(f"\n💰 Current Funding Rate: {data['funding_rate_percent']:.4f}%")
        print(f"Annualized Rate: {data['annualized_rate']:.2f}%")
        print(f"Funding Time: {datetime.fromtimestamp(data['funding_time']/1000)}")

        # Interpret funding rate
        if data['funding_rate'] > 0:
            print(f"📊 Analysis: Longs pay shorts (bullish sentiment)")
        else:
            print(f"📊 Analysis: Shorts pay longs (bearish sentiment)")

        print(f"\n✓ Funding rate test PASSED")
        return True
    except Exception as e:
        print(f"\n✗ Funding rate test FAILED: {e}")
        return False


def test_long_short_ratio(client, symbol='BTCUSDT'):
    """Test 6: Get long/short ratio"""
    print_header(f"TEST 6: Long/Short Ratio - {symbol}")

    try:
        data = client.get_long_short_ratio(symbol, period='5m')
        print(f"\n⚖️  Long Ratio: {data['long_ratio']:.2f}")
        print(f"Short Ratio: {data['short_ratio']:.2f}")
        print(f"Long/Short Ratio: {data['long_short_ratio']:.2f}")

        # Interpret ratio
        if data['long_short_ratio'] > 1:
            print(f"📊 Analysis: More traders are long ({data['long_ratio']*100:.1f}% vs {data['short_ratio']*100:.1f}%)")
        else:
            print(f"📊 Analysis: More traders are short ({data['short_ratio']*100:.1f}% vs {data['long_ratio']*100:.1f}%)")

        print(f"\n✓ Long/short ratio test PASSED")
        return True
    except Exception as e:
        print(f"\n✗ Long/short ratio test FAILED: {e}")
        return False


def test_orderbook(client, symbol='BTCUSDT'):
    """Test 7: Get orderbook data"""
    print_header(f"TEST 7: Orderbook Liquidity - {symbol}")

    try:
        data = client.get_orderbook(symbol, limit=20)
        print(f"\n📖 Best Bid: ${data['best_bid']:,.2f}")
        print(f"Best Ask: ${data['best_ask']:,.2f}")
        print(f"Spread: ${data['spread']:.2f} ({data['spread_percent']:.4f}%)")
        print(f"\nTotal Bid Volume: {data['total_bid_volume']:,.2f} BTC (${data['total_bid_value']:,.2f})")
        print(f"Total Ask Volume: {data['total_ask_volume']:,.2f} BTC (${data['total_ask_value']:,.2f})")
        print(f"Bid/Ask Ratio: {data['bid_ask_ratio']:.2f}")

        print(f"\nTop 5 Bids:")
        for price, qty in data['bids']:
            print(f"  ${price:,.2f} -> {qty:.4f} BTC")

        print(f"\nTop 5 Asks:")
        for price, qty in data['asks']:
            print(f"  ${price:,.2f} -> {qty:.4f} BTC")

        # Interpret orderbook
        if data['bid_ask_ratio'] > 1:
            print(f"\n📊 Analysis: More buy liquidity (bid-heavy orderbook)")
        else:
            print(f"\n📊 Analysis: More sell liquidity (ask-heavy orderbook)")

        print(f"\n✓ Orderbook test PASSED")
        return True
    except Exception as e:
        print(f"\n✗ Orderbook test FAILED: {e}")
        return False


def run_all_tests():
    """Run all tests and display summary"""
    print("\n" + "🚀" * 40)
    print("  QUANTRA-950 BINANCE API WRAPPER TEST SUITE")
    print("🚀" * 40)

    results = []
    symbol = 'BTCUSDT'

    # Test 1: Configuration
    results.append(('Configuration', test_configuration()))

    # Test 2: Client initialization
    client = test_client_initialization()
    if client:
        results.append(('Client Initialization', True))

        # Test 3-7: API methods
        results.append(('Futures Ticker', test_futures_ticker(client, symbol)))
        results.append(('Open Interest', test_open_interest(client, symbol)))
        results.append(('Funding Rate', test_funding_rate(client, symbol)))
        results.append(('Long/Short Ratio', test_long_short_ratio(client, symbol)))
        results.append(('Orderbook', test_orderbook(client, symbol)))
    else:
        results.append(('Client Initialization', False))

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
        print("\n🎉 All tests passed! Binance API wrapper is working correctly.")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
