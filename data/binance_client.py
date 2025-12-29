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

    def get_recent_trades(self, symbol: str = 'BTCUSDT', limit: int = 1000) -> List[Dict]:
        """
        Get recent trades for CVD calculation

        Args:
            symbol: Trading pair symbol
            limit: Number of recent trades (max 1000)

        Returns:
            List of recent trades with time, price, qty, isBuyerMaker
        """
        try:
            trades = self.client.futures_recent_trades(symbol=symbol, limit=limit)
            return trades
        except BinanceAPIException as e:
            print(f"✗ Error fetching recent trades: {e}")
            raise

    def calculate_cvd_trend(self, symbol: str = 'BTCUSDT') -> Dict:
        """
        Calculate CVD (Cumulative Volume Delta) trend from recent trades

        Args:
            symbol: Trading pair symbol

        Returns:
            Dict with CVD values for 1h, 4h, 24h and trend directions
        """
        try:
            trades = self.get_recent_trades(symbol, limit=1000)
            now = time.time() * 1000  # Current time in milliseconds

            cvd_1h = 0
            cvd_4h = 0
            cvd_24h = 0

            for trade in trades:
                timestamp = trade['time']
                volume = float(trade['qty'])

                # If buyer is maker = sell pressure (negative)
                # If buyer is taker = buy pressure (positive)
                delta = -volume if trade['isBuyerMaker'] else volume

                # Accumulate based on timeframe
                if now - timestamp < 3600000:  # 1 hour
                    cvd_1h += delta
                if now - timestamp < 14400000:  # 4 hours
                    cvd_4h += delta
                cvd_24h += delta  # All trades

            return {
                '1h': round(cvd_1h, 2),
                '4h': round(cvd_4h, 2),
                '24h': round(cvd_24h, 2),
                'trend_1h': 'rising' if cvd_1h > 0 else 'falling',
                'trend_4h': 'rising' if cvd_4h > 0 else 'falling',
                'trend_24h': 'rising' if cvd_24h > 0 else 'falling'
            }
        except Exception as e:
            print(f"✗ Error calculating CVD trend: {e}")
            return {
                '1h': 0, '4h': 0, '24h': 0,
                'trend_1h': 'neutral', 'trend_4h': 'neutral', 'trend_24h': 'neutral'
            }

    def calculate_orderbook_depth(self, symbol: str = 'BTCUSDT') -> Dict:
        """
        Calculate orderbook depth at 1%, 2%, and 5% price levels

        Args:
            symbol: Trading pair symbol

        Returns:
            Dict with bid/ask volumes at each price level
        """
        try:
            orderbook = self.client.futures_order_book(symbol=symbol, limit=1000)
            ticker = self.get_futures_ticker(symbol)
            current_price = ticker['last_price']

            bids = [[float(price), float(qty)] for price, qty in orderbook['bids']]
            asks = [[float(price), float(qty)] for price, qty in orderbook['asks']]

            # Calculate price thresholds
            levels = {
                '1%': {'bid': current_price * 0.99, 'ask': current_price * 1.01},
                '2%': {'bid': current_price * 0.98, 'ask': current_price * 1.02},
                '5%': {'bid': current_price * 0.95, 'ask': current_price * 1.05}
            }

            depth = {}
            for level_name, thresholds in levels.items():
                bid_volume = sum(qty for price, qty in bids if price >= thresholds['bid'])
                ask_volume = sum(qty for price, qty in asks if price <= thresholds['ask'])
                imbalance = (bid_volume - ask_volume) / (bid_volume + ask_volume) * 100 if (bid_volume + ask_volume) > 0 else 0

                depth[level_name] = {
                    'bid_volume': round(bid_volume, 2),
                    'ask_volume': round(ask_volume, 2),
                    'imbalance': round(imbalance, 2)
                }

            return depth
        except Exception as e:
            print(f"✗ Error calculating orderbook depth: {e}")
            return {
                '1%': {'bid_volume': 0, 'ask_volume': 0, 'imbalance': 0},
                '2%': {'bid_volume': 0, 'ask_volume': 0, 'imbalance': 0},
                '5%': {'bid_volume': 0, 'ask_volume': 0, 'imbalance': 0}
            }

    def calculate_oi_delta(self, symbol: str = 'BTCUSDT') -> Dict:
        """
        Calculate Open Interest delta (requires historical storage)

        NOTE: This is a simplified version. For accurate OI delta tracking,
        you need to store historical OI values in a database and compare them.

        Args:
            symbol: Trading pair symbol

        Returns:
            Dict with current OI and a note about historical tracking
        """
        try:
            oi_data = self.get_open_interest(symbol)

            return {
                'current_oi': oi_data['open_interest'],
                'note': 'Historical OI delta requires database storage',
                'delta_1h': 'N/A (requires historical data)',
                'delta_4h': 'N/A (requires historical data)',
                'delta_24h': 'N/A (requires historical data)'
            }
        except Exception as e:
            print(f"✗ Error calculating OI delta: {e}")
            return {
                'current_oi': 0,
                'note': 'Error calculating OI',
                'delta_1h': 'N/A',
                'delta_4h': 'N/A',
                'delta_24h': 'N/A'
            }

    def get_market_overview(self, symbol: str = 'BTCUSDT', include_advanced: bool = False) -> Dict:
        """
        Get comprehensive market overview combining all data sources

        Args:
            symbol: Trading pair symbol
            include_advanced: Include CVD, orderbook depth, OI delta calculations (for /q3)

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

        # Advanced calculations (for /q3 command)
        if include_advanced:
            try:
                overview['cvd_trend'] = self.calculate_cvd_trend(symbol)
                print(f"✓ CVD trend calculated")
            except Exception as e:
                print(f"✗ CVD calculation failed: {e}")
                overview['cvd_trend'] = None

            try:
                overview['orderbook_depth'] = self.calculate_orderbook_depth(symbol)
                print(f"✓ Orderbook depth calculated")
            except Exception as e:
                print(f"✗ Orderbook depth calculation failed: {e}")
                overview['orderbook_depth'] = None

            try:
                overview['oi_delta'] = self.calculate_oi_delta(symbol)
                print(f"✓ OI delta calculated")
            except Exception as e:
                print(f"✗ OI delta calculation failed: {e}")
                overview['oi_delta'] = None

        return overview
