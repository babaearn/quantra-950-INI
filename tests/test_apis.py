#!/usr/bin/env python3
"""
API Connection Test Script
Tests all API keys to ensure they're working correctly
"""

import os
import sys
from pathlib import Path

# Add parent directory to path to import from project
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_test_header(api_name):
    print(f"\n{'='*60}")
    print(f"Testing {api_name}...")
    print('='*60)

def print_success(message="Success!"):
    print(f"✅ {message}")

def print_failure(error):
    print(f"❌ Failed: {error}")

# ============================================================
# Test 1: Gemini API
# ============================================================
def test_gemini():
    print_test_header("Gemini API")
    try:
        import requests

        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print_failure("GEMINI_API_KEY not found in environment")
            return False

        # Use REST API instead of gRPC to avoid SSL issues
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"

        payload = {
            "contents": [{
                "parts": [{
                    "text": "Say 'Hello' in one word"
                }]
            }]
        }

        response = requests.post(url, json=payload, timeout=15)

        if response.status_code == 200:
            data = response.json()
            result = data['candidates'][0]['content']['parts'][0]['text'].strip()
            print_success("Gemini API is working!")
            print(f"📝 Response: {result}")
            return True
        else:
            print_failure(f"HTTP {response.status_code}: {response.text}")
            return False

    except Exception as e:
        print_failure(str(e))
        return False

# ============================================================
# Test 2: Binance API
# ============================================================
def test_binance():
    print_test_header("Binance API")
    try:
        from binance.client import Client

        api_key = os.getenv('BINANCE_API_KEY')
        api_secret = os.getenv('BINANCE_API_SECRET')

        if not api_key or not api_secret:
            print_failure("BINANCE_API_KEY or BINANCE_API_SECRET not found")
            return False

        client = Client(api_key, api_secret)

        # Test 1: Get BTC price
        btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
        print_success("Binance API is working!")
        print(f"💰 BTC Price: ${float(btc_price['price']):,.2f}")

        # Test 2: Check account status
        account = client.get_account_status()
        print(f"📊 Account Status: {account['data']}")

        # Test 3: Get account info (requires valid API permissions)
        try:
            account_info = client.get_account()
            print(f"🔑 API Permissions: OK (Can read account)")
        except Exception as e:
            if "API-key format invalid" in str(e):
                print_failure("Invalid API key format")
                return False
            else:
                print(f"⚠️  Limited permissions (this is OK for price data)")

        return True

    except Exception as e:
        print_failure(str(e))
        return False

# ============================================================
# Test 3: CoinGlass API
# ============================================================
def test_coinglass():
    print_test_header("CoinGlass API")
    try:
        import requests

        api_key = os.getenv('COINGLASS_API_KEY')
        if not api_key:
            print_failure("COINGLASS_API_KEY not found in environment")
            return False

        # Test with supported coins endpoint
        url = "https://open-api.coinglass.com/public/v2/indicator/supported_coins"
        headers = {
            "accept": "application/json",
            "coinglassSecret": api_key
        }

        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                coins = data.get('data', [])
                print_success("CoinGlass API is working!")
                print(f"📊 Supported coins count: {len(coins)}")
                print(f"📈 Sample coins: {', '.join(coins[:5])}")
                return True
            else:
                print_failure(f"API returned: {data}")
                return False
        else:
            print_failure(f"HTTP {response.status_code}: {response.text}")
            return False

    except Exception as e:
        print_failure(str(e))
        return False

# ============================================================
# Test 4: Telegram Bot API
# ============================================================
def test_telegram():
    print_test_header("Telegram Bot API")
    try:
        from telegram import Bot
        import asyncio

        token = os.getenv('TELEGRAM_BOT_TOKEN')
        user_id = os.getenv('TELEGRAM_USER_ID')

        if not token:
            print_failure("TELEGRAM_BOT_TOKEN not found in environment")
            return False

        if not user_id:
            print_failure("TELEGRAM_USER_ID not found in environment")
            return False

        async def test_bot():
            bot = Bot(token=token)

            # Get bot info
            me = await bot.get_me()
            print_success("Telegram Bot API is working!")
            print(f"🤖 Bot Username: @{me.username}")
            print(f"📛 Bot Name: {me.first_name}")

            # Send test message
            try:
                message = await bot.send_message(
                    chat_id=user_id,
                    text="🧪 API Test Successful!\n\nYour Quantra-950 bot is ready to trade! 🚀"
                )
                print(f"💬 Test message sent successfully!")
                return True
            except Exception as e:
                print(f"⚠️  Could not send message: {e}")
                print(f"   (Bot credentials are valid, but may need to start chat first)")
                return True  # Bot is still valid even if message fails

        # Run async function
        return asyncio.run(test_bot())

    except Exception as e:
        print_failure(str(e))
        return False

# ============================================================
# Main Test Runner
# ============================================================
def main():
    print("\n" + "="*60)
    print("🔧 QUANTRA-950 API CONNECTION TESTS")
    print("="*60)

    results = {
        "Gemini": test_gemini(),
        "Binance": test_binance(),
        "CoinGlass": test_coinglass(),
        "Telegram": test_telegram()
    }

    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)

    for api, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{api:15} {status}")

    total = len(results)
    passed = sum(results.values())

    print(f"\n{'='*60}")
    print(f"Results: {passed}/{total} APIs working")
    print('='*60)

    if passed == total:
        print("\n🎉 All APIs are configured correctly!")
        return 0
    else:
        print("\n⚠️  Some APIs failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
