"""
Test suite for Gemini AI Analyzer
Tests AI market analysis with real Bitcoin data
"""
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from intelligence.gemini_analyzer import GeminiAnalyzer
from data.binance_client import BinanceClient
from config.settings import settings
import json
from datetime import datetime


def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def test_gemini_configuration():
    """Test 1: Verify Gemini API configuration"""
    print_header("TEST 1: Gemini API Configuration")

    try:
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment")

        print(f"✓ Gemini API Key: {'*' * 8}{settings.GEMINI_API_KEY[-4:] if len(settings.GEMINI_API_KEY) > 4 else '****'}")
        print("✓ Gemini configuration test PASSED")
        return True
    except Exception as e:
        print(f"✗ Gemini configuration test FAILED: {e}")
        return False


def test_gemini_initialization():
    """Test 2: Initialize Gemini analyzer"""
    print_header("TEST 2: Gemini Analyzer Initialization")

    try:
        analyzer = GeminiAnalyzer()
        print("✓ Gemini analyzer initialization test PASSED")
        return analyzer
    except Exception as e:
        print(f"✗ Gemini analyzer initialization test FAILED: {e}")
        return None


def test_fetch_market_data():
    """Test 3: Fetch real BTC market data"""
    print_header("TEST 3: Fetching Real Bitcoin Market Data")

    try:
        client = BinanceClient()
        print("\n📊 Fetching comprehensive market data for BTCUSDT...")

        market_data = client.get_market_overview('BTCUSDT')

        # Display summary of fetched data
        print("\n✓ Market data fetched successfully:")
        if market_data.get('ticker'):
            print(f"   • Price: ${market_data['ticker']['last_price']:,.2f}")
            print(f"   • 24h Change: {market_data['ticker']['price_change_percent']:+.2f}%")
        if market_data.get('open_interest'):
            print(f"   • Open Interest: {market_data['open_interest']['open_interest']:,.2f} BTC")
        if market_data.get('funding_rate'):
            print(f"   • Funding Rate: {market_data['funding_rate']['funding_rate_percent']:.4f}%")
        if market_data.get('long_short_ratio'):
            print(f"   • L/S Ratio: {market_data['long_short_ratio']['long_short_ratio']:.2f}")
        if market_data.get('orderbook'):
            print(f"   • Spread: ${market_data['orderbook']['spread']:.2f}")

        print("\n✓ Market data fetch test PASSED")
        return market_data
    except Exception as e:
        print(f"\n✗ Market data fetch test FAILED: {e}")
        return None


def test_ai_analysis(analyzer, market_data):
    """Test 4: Generate AI analysis from market data"""
    print_header("TEST 4: AI Market Analysis Generation")

    try:
        print("\n🤖 Sending market data to Gemini AI for analysis...")
        print("⏳ This may take 5-10 seconds...\n")

        # Generate analysis
        analysis = analyzer.analyze_market(market_data)

        print("\n✓ AI analysis generation test PASSED")
        return analysis
    except Exception as e:
        print(f"\n✗ AI analysis generation test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_analysis_structure(analysis):
    """Test 5: Validate analysis JSON structure"""
    print_header("TEST 5: Analysis Structure Validation")

    try:
        # Required fields
        required_fields = {
            'signal': str,
            'confidence': (int, float),
            'entry_price': (int, float),
            'stop_loss': (int, float),
            'targets': dict,
            'narrative': str
        }

        print("\n🔍 Validating JSON structure...\n")

        # Check required fields
        for field, expected_type in required_fields.items():
            if field not in analysis:
                raise ValueError(f"Missing required field: {field}")

            if not isinstance(analysis[field], expected_type):
                raise ValueError(f"Field '{field}' has wrong type. Expected {expected_type}, got {type(analysis[field])}")

            print(f"✓ {field}: {type(analysis[field]).__name__}")

        # Validate signal value
        if analysis['signal'] not in ['LONG', 'SHORT', 'NEUTRAL']:
            raise ValueError(f"Invalid signal value: {analysis['signal']}")
        print(f"✓ Signal value is valid: {analysis['signal']}")

        # Validate confidence range
        if not 0 <= analysis['confidence'] <= 100:
            raise ValueError(f"Confidence out of range: {analysis['confidence']}")
        print(f"✓ Confidence in valid range: {analysis['confidence']}/100")

        # Validate targets structure
        if 'targets' in analysis:
            required_targets = ['tp1', 'tp2', 'tp3']
            for target in required_targets:
                if target not in analysis['targets']:
                    print(f"⚠️  Warning: Missing target {target}")
        print(f"✓ Targets structure validated")

        # Check optional fields
        optional_fields = ['timeframe_alignment', 'key_levels', 'warnings', 'market_regime', 'risk_reward_ratio']
        for field in optional_fields:
            if field in analysis:
                print(f"✓ Optional field present: {field}")

        print("\n✓ Analysis structure validation test PASSED")
        return True
    except Exception as e:
        print(f"\n✗ Analysis structure validation test FAILED: {e}")
        return False


def test_display_analysis(analyzer, analysis):
    """Test 6: Display formatted analysis"""
    print_header("TEST 6: Display Formatted Analysis")

    try:
        analyzer.display_analysis(analysis)
        print("\n✓ Display analysis test PASSED")
        return True
    except Exception as e:
        print(f"\n✗ Display analysis test FAILED: {e}")
        return False


def test_export_json(analysis):
    """Test 7: Export analysis as JSON"""
    print_header("TEST 7: JSON Export")

    try:
        json_output = json.dumps(analysis, indent=2, default=str)
        print("\n📄 JSON Output (first 500 chars):")
        print(json_output[:500])
        print(f"...\n\nTotal JSON size: {len(json_output)} characters")

        print("\n✓ JSON export test PASSED")
        return True
    except Exception as e:
        print(f"\n✗ JSON export test FAILED: {e}")
        return False


def run_all_tests():
    """Run all tests and display summary"""
    print("\n" + "🧠" * 40)
    print("  QUANTRA-950 GEMINI AI ANALYZER TEST SUITE")
    print("🧠" * 40)

    results = []

    # Test 1: Configuration
    results.append(('Gemini Configuration', test_gemini_configuration()))

    # Test 2: Analyzer initialization
    analyzer = test_gemini_initialization()
    if analyzer:
        results.append(('Gemini Initialization', True))

        # Test 3: Fetch market data
        market_data = test_fetch_market_data()
        if market_data:
            results.append(('Market Data Fetch', True))

            # Test 4: Generate AI analysis
            analysis = test_ai_analysis(analyzer, market_data)
            if analysis:
                results.append(('AI Analysis Generation', True))

                # Test 5: Validate structure
                results.append(('Structure Validation', test_analysis_structure(analysis)))

                # Test 6: Display analysis
                results.append(('Display Analysis', test_display_analysis(analyzer, analysis)))

                # Test 7: JSON export
                results.append(('JSON Export', test_export_json(analysis)))
            else:
                results.append(('AI Analysis Generation', False))
                results.append(('Structure Validation', False))
                results.append(('Display Analysis', False))
                results.append(('JSON Export', False))
        else:
            results.append(('Market Data Fetch', False))
    else:
        results.append(('Gemini Initialization', False))

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
        print("\n🎉 All tests passed! Gemini AI integration is working correctly.")
        print("\n💡 Next Steps:")
        print("   1. Test with different market conditions")
        print("   2. Validate AI analysis accuracy over time")
        print("   3. Integrate with trading execution system")
        print("   4. Add performance tracking and backtesting")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
