# API Tests

## test_apis.py

This script tests all API connections for the Quantra-950 trading bot.

### What it tests:

1. **Gemini API** - Google's Generative AI for market analysis
2. **Binance API** - Cryptocurrency exchange for trading and price data
3. **CoinGlass API** - Advanced crypto market data and metrics
4. **Telegram Bot API** - Notifications and bot communication

### How to run:

```bash
python tests/test_apis.py
```

### Expected Output:

When all APIs are configured correctly, you'll see:

```
============================================================
🔧 QUANTRA-950 API CONNECTION TESTS
============================================================

============================================================
Testing Gemini API...
============================================================
✅ Gemini API is working!
📝 Response: Hello

============================================================
Testing Binance API...
============================================================
✅ Binance API is working!
💰 BTC Price: $XX,XXX.XX
📊 Account Status: Normal
🔑 API Permissions: OK (Can read account)

============================================================
Testing CoinGlass API...
============================================================
✅ CoinGlass API is working!
📊 Supported coins count: XX
📈 Sample coins: BTC, ETH, ...

============================================================
Testing Telegram Bot API...
============================================================
✅ Telegram Bot API is working!
🤖 Bot Username: @your_bot
📛 Bot Name: Your Bot Name
💬 Test message sent successfully!

============================================================
📊 TEST SUMMARY
============================================================
Gemini          ✅ PASS
Binance         ✅ PASS
CoinGlass       ✅ PASS
Telegram        ✅ PASS

============================================================
Results: 4/4 APIs working
============================================================

🎉 All APIs are configured correctly!
```

### Troubleshooting:

- **403 Forbidden / Proxy errors**: This happens in restricted network environments. The script will work fine on your local machine or production server.
- **SSL certificate errors**: Fixed by using REST APIs instead of gRPC
- **API key errors**: Ensure your `.env` file has all required keys
- **Telegram message fails**: Start a chat with your bot first by sending `/start`

### API Key Requirements:

All keys should be in your `.env` file:
- `GEMINI_API_KEY` - From Google AI Studio
- `BINANCE_API_KEY` - From Binance account
- `BINANCE_API_SECRET` - From Binance account
- `COINGLASS_API_KEY` - From CoinGlass
- `TELEGRAM_BOT_TOKEN` - From BotFather
- `TELEGRAM_USER_ID` - Your Telegram user ID
