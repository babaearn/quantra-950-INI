"""
Binance API Client Wrapper for Quantra-950
Provides methods to fetch futures market data from Binance
"""
from binance.client import Client
from binance.exceptions import BinanceAPIException
from config.settings import settings
from typing import Dict, Optional, List
import time


class BinanceClient:
    """Wrapper for Binance Futures API with market data methods"""

    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None):
        """
        Initialize Binance client

        Args:
            api_key: Binance API key (defaults to settings)
            api_secret: Binance API secret (defaults to settings)
        """
        self.api_key = api_key or settings.BINANCE_API_KEY
        self.api_secret = api_secret or settings.BINANCE_API_SECRET

        if not self.api_key or not self.api_secret:
            raise ValueError("Binance API credentials not found. Check your .env file.")

        self.client = Client(self.api_key, self.api_secret)
        print(f"✓ Binance client initialized")

    def get_futures_ticker(self, symbol: str = 'BTCUSDT') -> Dict:
        """
        Get current futures ticker price and stats

        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')

        Returns:
            Dict with price, volume, and price change data
        """
        try:
            ticker = self.client.futures_ticker(symbol=symbol)

            return {
                'symbol': ticker['symbol'],
                'last_price': float(ticker['lastPrice']),
                'price_change': float(ticker['priceChange']),
                'price_change_percent': float(ticker['priceChangePercent']),
                'high_price': float(ticker['highPrice']),
                'low_price': float(ticker['lowPrice']),
                'volume': float(ticker['volume']),
                'quote_volume': float(ticker['quoteVolume']),
                'timestamp': ticker['closeTime']
            }
        except BinanceAPIException as e:
            print(f"✗ Error fetching futures ticker: {e}")
            raise

    def get_open_interest(self, symbol: str = 'BTCUSDT') -> Dict:
        """
        Get open interest data for a symbol

        Args:
            symbol: Trading pair symbol

        Returns:
            Dict with open interest amount and value
        """
        try:
            oi_data = self.client.futures_open_interest(symbol=symbol)
            ticker = self.client.futures_ticker(symbol=symbol)

            oi_amount = float(oi_data['openInterest'])
            current_price = float(ticker['lastPrice'])
            oi_value = oi_amount * current_price

            return {
                'symbol': symbol,
                'open_interest': oi_amount,
                'open_interest_value': oi_value,
                'current_price': current_price,
                'timestamp': oi_data['time']
            }
        except BinanceAPIException as e:
            print(f"✗ Error fetching open interest: {e}")
            raise

    def get_funding_rate(self, symbol: str = 'BTCUSDT') -> Dict:
        """
        Get current and next funding rate

        Args:
            symbol: Trading pair symbol

        Returns:
            Dict with funding rate info
        """
        try:
            funding_info = self.client.futures_funding_rate(symbol=symbol, limit=1)

            if not funding_info:
                raise ValueError(f"No funding rate data available for {symbol}")

            latest = funding_info[0]

            return {
                'symbol': latest['symbol'],
                'funding_rate': float(latest['fundingRate']),
                'funding_rate_percent': float(latest['fundingRate']) * 100,
                'funding_time': latest['fundingTime'],
                'annualized_rate': float(latest['fundingRate']) * 3 * 365 * 100  # 8-hour funding, annualized
            }
        except BinanceAPIException as e:
            print(f"✗ Error fetching funding rate: {e}")
            raise

    def get_long_short_ratio(self, symbol: str = 'BTCUSDT', period: str = '5m') -> Dict:
        """
        Get top trader long/short ratio (accounts)

        Args:
            symbol: Trading pair symbol
            period: Time period ('5m', '15m', '30m', '1h', '2h', '4h', '6h', '12h', '1d')

        Returns:
            Dict with long/short ratio data
        """
        try:
            # Get top trader long/short ratio (by accounts)
            ratio_data = self.client.futures_top_longshort_account_ratio(
                symbol=symbol,
                period=period,
                limit=1
            )

            if not ratio_data:
                raise ValueError(f"No long/short ratio data available for {symbol}")

            latest = ratio_data[0]
            long_ratio = float(latest['longAccount'])
            short_ratio = float(latest['shortAccount'])

            return {
                'symbol': symbol,
                'period': period,
                'long_ratio': long_ratio,
                'short_ratio': short_ratio,
                'long_short_ratio': long_ratio / short_ratio if short_ratio > 0 else 0,
                'timestamp': latest['timestamp']
            }
        except BinanceAPIException as e:
            print(f"✗ Error fetching long/short ratio: {e}")
            raise

    def get_orderbook(self, symbol: str = 'BTCUSDT', limit: int = 20) -> Dict:
        """
        Get orderbook depth data

        Args:
            symbol: Trading pair symbol
            limit: Depth limit (5, 10, 20, 50, 100, 500, 1000)

        Returns:
            Dict with orderbook bids/asks and liquidity analysis
        """
        try:
            orderbook = self.client.futures_order_book(symbol=symbol, limit=limit)

            bids = [[float(price), float(qty)] for price, qty in orderbook['bids']]
            asks = [[float(price), float(qty)] for price, qty in orderbook['asks']]

            # Calculate liquidity metrics
            total_bid_volume = sum(qty for _, qty in bids)
            total_ask_volume = sum(qty for _, qty in asks)
            total_bid_value = sum(price * qty for price, qty in bids)
            total_ask_value = sum(price * qty for price, qty in asks)

            best_bid = bids[0][0] if bids else 0
            best_ask = asks[0][0] if asks else 0
            spread = best_ask - best_bid if best_bid and best_ask else 0
            spread_percent = (spread / best_ask * 100) if best_ask else 0

            return {
                'symbol': symbol,
                'timestamp': orderbook['lastUpdateId'],
                'best_bid': best_bid,
                'best_ask': best_ask,
                'spread': spread,
                'spread_percent': spread_percent,
                'total_bid_volume': total_bid_volume,
                'total_ask_volume': total_ask_volume,
                'total_bid_value': total_bid_value,
                'total_ask_value': total_ask_value,
                'bid_ask_ratio': total_bid_volume / total_ask_volume if total_ask_volume > 0 else 0,
                'bids': bids[:5],  # Top 5 bids
                'asks': asks[:5],  # Top 5 asks
            }
        except BinanceAPIException as e:
            print(f"✗ Error fetching orderbook: {e}")
            raise

    def get_market_overview(self, symbol: str = 'BTCUSDT') -> Dict:
        """
        Get comprehensive market overview combining all data sources

        Args:
            symbol: Trading pair symbol

        Returns:
            Dict with complete market data
        """
        print(f"\n📊 Fetching market overview for {symbol}...")

        overview = {
            'symbol': symbol,
            'timestamp': int(time.time() * 1000)
        }

        try:
            overview['ticker'] = self.get_futures_ticker(symbol)
            print(f"✓ Ticker data fetched")
        except Exception as e:
            print(f"✗ Ticker fetch failed: {e}")
            overview['ticker'] = None

        try:
            overview['open_interest'] = self.get_open_interest(symbol)
            print(f"✓ Open interest data fetched")
        except Exception as e:
            print(f"✗ Open interest fetch failed: {e}")
            overview['open_interest'] = None

        try:
            overview['funding_rate'] = self.get_funding_rate(symbol)
            print(f"✓ Funding rate data fetched")
        except Exception as e:
            print(f"✗ Funding rate fetch failed: {e}")
            overview['funding_rate'] = None

        try:
            overview['long_short_ratio'] = self.get_long_short_ratio(symbol)
            print(f"✓ Long/short ratio data fetched")
        except Exception as e:
            print(f"✗ Long/short ratio fetch failed: {e}")
            overview['long_short_ratio'] = None

        try:
            overview['orderbook'] = self.get_orderbook(symbol)
            print(f"✓ Orderbook data fetched")
        except Exception as e:
            print(f"✗ Orderbook fetch failed: {e}")
            overview['orderbook'] = None

        return overview
