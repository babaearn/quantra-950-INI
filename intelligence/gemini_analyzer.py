"""
Gemini AI Analyzer for Quantra-950
Advanced market intelligence using Google Gemini 2.5 Flash Lite
"""
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from config.settings import settings
import json
from typing import Dict, Optional, List
from datetime import datetime


class GeminiAnalyzer:
    """
    AI-powered market analyzer using Gemini 2.5 Flash Lite
    Implements evolutionary learning and multi-timeframe analysis
    Free tier: 1,500 requests/day, 30 requests/minute
    """

    # QUANTRA-950 System Prompt - Autonomous Trading Intelligence
    SYSTEM_PROMPT = """You are QUANTRA-950, an advanced autonomous crypto derivatives trading intelligence system.

🎯 CORE MISSION
Analyze Bitcoin futures market data and generate high-conviction trading signals through multi-dimensional quantitative analysis and evolutionary pattern recognition.

🧬 EVOLUTIONARY LOOP
You operate in continuous improvement mode:
1. Analyze current market structure across multiple timeframes
2. Identify divergences between price action and derivatives metrics
3. Generate probabilistic trade scenarios with quantified edge
4. Reflect on previous analysis to refine pattern recognition
5. Adapt your analytical framework based on market regime changes

📊 MULTI-TIMEFRAME TRIANGULATION
Always analyze through three temporal lenses:
- 8H: Macro trend and structural levels
- 4H: Swing context and momentum shifts
- 1H: Entry precision and micro-structure

Cross-validate signals across all timeframes. Higher timeframe alignment = higher confidence.

🔬 QUANTITATIVE ANALYSIS FRAMEWORK

Analyze these derivatives metrics with precision:

1. **Open Interest (OI)**
   - Rising OI + rising price = strong trend (bulls adding)
   - Rising OI + falling price = strong trend (bears adding)
   - Falling OI = position unwinding, trend exhaustion
   - Look for OI divergences vs price

2. **Funding Rate**
   - Positive funding = longs pay shorts (bullish bias)
   - Negative funding = shorts pay longs (bearish bias)
   - Extreme funding (>0.1% or <-0.1%) = potential reversal
   - Funding resets can trigger cascading liquidations

3. **Long/Short Ratio**
   - >1.0 = more traders long (contrarian bearish)
   - <1.0 = more traders short (contrarian bullish)
   - Extreme ratios (>2.0 or <0.5) = crowded trade, reversal setup

4. **Orderbook Liquidity**
   - Bid/ask imbalance shows immediate pressure
   - Large bid walls = support, ask walls = resistance
   - Thin liquidity = high slippage risk
   - Orderbook spoofing detection

5. **Price Action**
   - Volume profile and exhaustion patterns
   - Liquidity sweeps and stop hunts
   - Support/resistance confluence
   - Momentum vs price divergences

🎯 SIGNAL GENERATION RULES

**LONG Setup Requirements:**
- Price showing strength or reversal from support
- OI increasing with price (conviction)
- Funding not extremely positive (no overcrowding)
- Long/short ratio not extremely high
- Orderbook showing bid support
- Multi-timeframe alignment

**SHORT Setup Requirements:**
- Price showing weakness or rejection from resistance
- OI increasing with falling price (conviction)
- Funding not extremely negative (no overcrowding)
- Long/short ratio not extremely low
- Orderbook showing ask resistance
- Multi-timeframe alignment

**NEUTRAL Conditions:**
- Conflicting signals across timeframes
- Low conviction / choppy price action
- Extreme funding with no clear catalyst
- Thin liquidity / high uncertainty
- No clear edge detected

🎲 CONFIDENCE SCORING (0-100)

- 90-100: Extremely high conviction, multiple confluences, rare setup
- 70-89: High conviction, clear edge, good risk/reward
- 50-69: Moderate conviction, some conflicting signals
- 30-49: Low conviction, mostly neutral with slight bias
- 0-29: Very low conviction, stay flat

Confidence = (Signal Strength × Timeframe Alignment × Risk/Reward × Market Regime Fit)

📋 OUTPUT FORMAT

You MUST respond with valid JSON only (no markdown, no explanations):

{
  "signal": "LONG" | "SHORT" | "NEUTRAL",
  "confidence": 0-100,
  "entry_price": number,
  "stop_loss": number,
  "targets": {
    "tp1": number,
    "tp2": number,
    "tp3": number
  },
  "risk_reward_ratio": number,
  "timeframe_alignment": {
    "8h": "BULLISH" | "BEARISH" | "NEUTRAL",
    "4h": "BULLISH" | "BEARISH" | "NEUTRAL",
    "1h": "BULLISH" | "BEARISH" | "NEUTRAL"
  },
  "key_levels": {
    "resistance": [numbers],
    "support": [numbers]
  },
  "narrative": "concise explanation of thesis and key factors",
  "warnings": ["any risks or concerns"],
  "market_regime": "TRENDING" | "RANGING" | "VOLATILE" | "BREAKOUT",
  "timestamp": "ISO format"
}

🧠 ANALYTICAL MINDSET

- Think like a professional derivatives trader
- Quantify everything - avoid vague analysis
- Consider multiple scenarios and assign probabilities
- Identify asymmetric risk/reward setups
- Respect market structure and liquidity
- Adapt to changing market regimes
- Be honest about uncertainty
- Never force trades - wait for high conviction setups

Remember: Your goal is not to always have a signal, but to identify the BEST opportunities with quantifiable edge. Quality over quantity."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini analyzer

        Args:
            api_key: Gemini API key (defaults to settings)
        """
        self.api_key = api_key or settings.GEMINI_API_KEY

        if not self.api_key:
            raise ValueError("Gemini API key not found. Check your .env file.")

        # Configure Gemini
        genai.configure(api_key=self.api_key)

        # Use Gemini 2.5 Flash Lite for free tier (1,500 req/day)
        self.model = genai.GenerativeModel(
            model_name='gemini-2.5-flash-lite',
            generation_config={
                'temperature': 0.3,  # Lower temperature for more consistent analysis
                'top_p': 0.95,
                'top_k': 40,
                'max_output_tokens': 2048,
            }
        )

        print(f"✓ Gemini AI analyzer initialized (Model: gemini-2.5-flash-lite)")
        print(f"✓ Free tier quota: 1,500 requests/day, 30 requests/minute")

    def _format_market_data(self, market_data: Dict) -> str:
        """
        Format market data into a structured prompt for Gemini

        Args:
            market_data: Market data dictionary from BinanceClient

        Returns:
            Formatted string prompt
        """
        ticker = market_data.get('ticker', {})
        oi = market_data.get('open_interest', {})
        funding = market_data.get('funding_rate', {})
        ratio = market_data.get('long_short_ratio', {})
        orderbook = market_data.get('orderbook', {})

        prompt = f"""Analyze this Bitcoin futures market data and generate a trading signal:

📊 CURRENT MARKET DATA
Symbol: {market_data.get('symbol', 'BTCUSDT')}
Timestamp: {datetime.now().isoformat()}

💰 PRICE ACTION (24H)
Current Price: ${ticker.get('last_price', 0):,.2f}
24h Change: {ticker.get('price_change_percent', 0):+.2f}%
24h High: ${ticker.get('high_price', 0):,.2f}
24h Low: ${ticker.get('low_price', 0):,.2f}
24h Volume: {ticker.get('volume', 0):,.2f} BTC
Quote Volume: ${ticker.get('quote_volume', 0):,.2f}

📈 OPEN INTEREST
OI Amount: {oi.get('open_interest', 0):,.2f} BTC
OI Value: ${oi.get('open_interest_value', 0):,.2f}
Price for OI: ${oi.get('current_price', 0):,.2f}

💸 FUNDING RATE
Current Rate: {funding.get('funding_rate_percent', 0):.4f}%
Annualized: {funding.get('annualized_rate', 0):.2f}%
Interpretation: {"Longs pay shorts (bullish sentiment)" if funding.get('funding_rate', 0) > 0 else "Shorts pay longs (bearish sentiment)"}

⚖️ LONG/SHORT RATIO (5m)
Long Ratio: {ratio.get('long_ratio', 0):.2f} ({ratio.get('long_ratio', 0)*100:.1f}%)
Short Ratio: {ratio.get('short_ratio', 0):.2f} ({ratio.get('short_ratio', 0)*100:.1f}%)
L/S Ratio: {ratio.get('long_short_ratio', 0):.2f}
Interpretation: {"More traders long" if ratio.get('long_short_ratio', 0) > 1 else "More traders short"}

📖 ORDERBOOK LIQUIDITY
Best Bid: ${orderbook.get('best_bid', 0):,.2f}
Best Ask: ${orderbook.get('best_ask', 0):,.2f}
Spread: ${orderbook.get('spread', 0):.2f} ({orderbook.get('spread_percent', 0):.4f}%)
Total Bid Volume: {orderbook.get('total_bid_volume', 0):,.2f} BTC (${orderbook.get('total_bid_value', 0):,.2f})
Total Ask Volume: {orderbook.get('total_ask_volume', 0):,.2f} BTC (${orderbook.get('total_ask_value', 0):,.2f})
Bid/Ask Ratio: {orderbook.get('bid_ask_ratio', 0):.2f}
Interpretation: {"More buy liquidity (bid-heavy)" if orderbook.get('bid_ask_ratio', 0) > 1 else "More sell liquidity (ask-heavy)"}

Top 5 Bids:
"""

        # Add orderbook depth
        for price, qty in orderbook.get('bids', [])[:5]:
            prompt += f"  ${price:,.2f} -> {qty:.4f} BTC\n"

        prompt += "\nTop 5 Asks:\n"
        for price, qty in orderbook.get('asks', [])[:5]:
            prompt += f"  ${price:,.2f} -> {qty:.4f} BTC\n"

        prompt += """
🎯 YOUR TASK
Analyze this data through the QUANTRA-950 framework:
1. Apply multi-timeframe triangulation logic
2. Identify key divergences and confluences
3. Calculate conviction level based on signal alignment
4. Generate precise entry, stop, and target levels
5. Provide clear narrative explaining the thesis

Respond with ONLY valid JSON (no markdown formatting, no code blocks, no explanations).
"""

        return prompt

    def analyze_market(self, market_data: Dict) -> Dict:
        """
        Analyze market data and generate trading signal using Gemini AI

        Args:
            market_data: Market data dictionary from BinanceClient.get_market_overview()

        Returns:
            Dict with structured trading analysis including signal, confidence, levels, and narrative

        Raises:
            ValueError: If API call fails or response is invalid
            json.JSONDecodeError: If Gemini response is not valid JSON
        """
        try:
            # Format market data into prompt
            prompt = self._format_market_data(market_data)

            # Generate analysis using Gemini
            print("\n🤖 Generating AI analysis with Gemini 2.5 Flash Lite...")
            response = self.model.generate_content(
                [self.SYSTEM_PROMPT, prompt]
            )

            # Extract text response
            response_text = response.text.strip()

            # Clean response - remove markdown code blocks if present
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            elif response_text.startswith('```'):
                response_text = response_text.replace('```', '').strip()

            # Parse JSON response
            analysis = json.loads(response_text)

            # Validate required fields
            required_fields = ['signal', 'confidence', 'entry_price', 'stop_loss', 'targets', 'narrative']
            missing_fields = [field for field in required_fields if field not in analysis]

            if missing_fields:
                raise ValueError(f"Missing required fields in AI response: {missing_fields}")

            # Validate signal value
            if analysis['signal'] not in ['LONG', 'SHORT', 'NEUTRAL']:
                raise ValueError(f"Invalid signal value: {analysis['signal']}")

            # Add metadata
            analysis['_metadata'] = {
                'model': 'gemini-2.5-flash-lite',
                'analyzed_at': datetime.now().isoformat(),
                'prompt_tokens': len(prompt.split()),
                'symbol': market_data.get('symbol', 'BTCUSDT')
            }

            print(f"✓ AI analysis complete")
            return analysis

        except ResourceExhausted as e:
            print(f"\n⚠️  Rate limit exceeded for Gemini API")
            print(f"   Free tier quota: 1,500 requests/day, 30 requests/minute")
            print(f"   Error: {e}")
            print(f"   Please wait a few minutes and try again.")
            raise ValueError("Gemini API rate limit exceeded. Please wait and retry.") from e

        except json.JSONDecodeError as e:
            print(f"✗ Failed to parse Gemini response as JSON: {e}")
            print(f"Raw response: {response_text[:500]}...")
            raise

        except Exception as e:
            print(f"✗ Error during AI analysis: {e}")
            raise

    def display_analysis(self, analysis: Dict) -> None:
        """
        Display analysis in a formatted, readable way

        Args:
            analysis: Analysis dictionary from analyze_market()
        """
        print("\n" + "=" * 80)
        print("  🧠 QUANTRA-950 AI MARKET ANALYSIS")
        print("=" * 80)

        # Signal and confidence
        signal = analysis['signal']
        confidence = analysis['confidence']

        signal_emoji = {"LONG": "🟢", "SHORT": "🔴", "NEUTRAL": "🟡"}
        print(f"\n{signal_emoji.get(signal, '⚪')} SIGNAL: {signal}")
        print(f"📊 CONFIDENCE: {confidence}/100")

        # Entry and risk management
        if analysis.get('entry_price') is not None:
            print(f"\n💰 ENTRY PRICE: ${analysis['entry_price']:,.2f}")
        else:
            print(f"\n💰 ENTRY PRICE: N/A (No trade signal)")

        if analysis.get('stop_loss') is not None:
            print(f"🛑 STOP LOSS: ${analysis['stop_loss']:,.2f}")
        else:
            print(f"🛑 STOP LOSS: N/A (No trade signal)")

        if 'targets' in analysis and analysis['targets'] is not None:
            targets = analysis['targets']
            print(f"🎯 TARGETS:")
            if targets.get('tp1') is not None:
                print(f"   TP1: ${targets.get('tp1'):,.2f}")
            else:
                print(f"   TP1: N/A")
            if targets.get('tp2') is not None:
                print(f"   TP2: ${targets.get('tp2'):,.2f}")
            else:
                print(f"   TP2: N/A")
            if targets.get('tp3') is not None:
                print(f"   TP3: ${targets.get('tp3'):,.2f}")
            else:
                print(f"   TP3: N/A")
        else:
            print(f"🎯 TARGETS: N/A (No trade signal)")

        if 'risk_reward_ratio' in analysis and analysis['risk_reward_ratio'] is not None:
            print(f"📈 RISK/REWARD: 1:{analysis['risk_reward_ratio']:.2f}")
        else:
            print(f"📈 RISK/REWARD: N/A (No trade signal)")

        # Timeframe alignment
        if 'timeframe_alignment' in analysis:
            tf = analysis['timeframe_alignment']
            print(f"\n⏰ TIMEFRAME ALIGNMENT:")
            print(f"   8H: {tf.get('8h', 'N/A')}")
            print(f"   4H: {tf.get('4h', 'N/A')}")
            print(f"   1H: {tf.get('1h', 'N/A')}")

        # Key levels
        if 'key_levels' in analysis:
            levels = analysis['key_levels']
            if levels.get('resistance'):
                print(f"\n🔺 RESISTANCE LEVELS:")
                for r in levels['resistance']:
                    print(f"   ${r:,.2f}")
            if levels.get('support'):
                print(f"\n🔻 SUPPORT LEVELS:")
                for s in levels['support']:
                    print(f"   ${s:,.2f}")

        # Market regime
        if 'market_regime' in analysis:
            print(f"\n📊 MARKET REGIME: {analysis['market_regime']}")

        # Narrative
        print(f"\n📝 ANALYSIS:")
        print(f"   {analysis['narrative']}")

        # Warnings
        if 'warnings' in analysis and analysis['warnings']:
            print(f"\n⚠️  WARNINGS:")
            for warning in analysis['warnings']:
                print(f"   • {warning}")

        # Metadata
        if '_metadata' in analysis:
            meta = analysis['_metadata']
            print(f"\n🔍 METADATA:")
            print(f"   Model: {meta.get('model', 'N/A')}")
            print(f"   Analyzed: {meta.get('analyzed_at', 'N/A')}")
            print(f"   Symbol: {meta.get('symbol', 'N/A')}")

        print("\n" + "=" * 80)

    def analyze_educational(self, market_data: Dict) -> Dict:
        """
        QUANTRA-2: Educational market analysis
        Focus on understanding, psychology, and smart money insights
        NO trading signals - pure education

        Args:
            market_data: Market data dictionary from BinanceClient

        Returns:
            Dict with educational analysis
        """
        EDUCATIONAL_PROMPT = """You are QUANTRA-2, an educational crypto market analyst focused on teaching traders to understand market dynamics.

🎯 YOUR MISSION
Explain what's happening in the market RIGHT NOW in simple, educational terms. Help traders understand the WHY behind price movements, smart money behavior, and market psychology.

📚 ANALYSIS FRAMEWORK

1. **WHAT'S HAPPENING NOW**
   - Market structure (consolidation, trending, breakout)
   - Volume analysis (increasing, declining, what it means)
   - Volatility assessment (compressed, expanding)
   - Smart money positioning vs retail

2. **SMART MONEY INSIGHTS**
   - What institutions/whales are doing
   - Order book psychology (bid/ask walls)
   - Accumulation vs distribution signals
   - Hidden buying/selling pressure

3. **MARKET PSYCHOLOGY**
   - Crowd behavior (FOMO, fear, greed)
   - Sentiment analysis (bullish, bearish, neutral)
   - Potential traps and manipulation
   - Contrarian indicators

4. **KEY DATA POINTS**
   - Technical metrics explained
   - Derivatives data interpretation
   - Volume profile insights
   - What each metric tells us

5. **EDUCATIONAL INSIGHTS**
   - What this market structure means
   - Things to watch for
   - Historical context
   - Learning opportunities

6. **EVOLUTION NOTES**
   - Patterns being tracked
   - What AI is learning from this
   - Success rate of similar setups
   - Ongoing improvements

🎓 TEACHING STYLE
- Use simple language, avoid jargon
- Explain the "why" behind everything
- Use bullet points for clarity
- Connect data to real market behavior
- Teach pattern recognition
- Build trader intuition

📋 OUTPUT FORMAT (JSON)
{
  "market_structure": "brief description",
  "whats_happening": {
    "price_action": "explanation",
    "volume_trend": "what it means",
    "volatility": "current state",
    "smart_money": "what they're doing"
  },
  "smart_money_insights": {
    "institution_activity": "what big players are doing",
    "orderbook_psychology": "bid/ask analysis",
    "whale_activity": "accumulation or distribution"
  },
  "market_psychology": {
    "crowd_behavior": "FOMO, fear, or greed",
    "sentiment": "current mood",
    "potential_traps": ["trap 1", "trap 2"]
  },
  "key_data": {
    "technical": "RSI, MACD, etc with explanations",
    "derivatives": "OI, funding, L/S ratio explained",
    "volume_profile": "where support/resistance is"
  },
  "educational_insights": {
    "what_this_means": "big picture explanation",
    "things_to_watch": ["point 1", "point 2"],
    "market_context": "where we are in cycle"
  },
  "evolution_notes": {
    "learning": "what AI is tracking",
    "pattern_success": "historical data",
    "improvements": "how analysis is evolving"
  },
  "timestamp": "ISO format"
}

Remember: NO trading signals. Pure education and understanding."""

        try:
            prompt = self._format_market_data(market_data)
            print("\n🎓 Generating educational analysis with QUANTRA-2...")

            response = self.model.generate_content([EDUCATIONAL_PROMPT, prompt])
            response_text = response.text.strip()

            # Clean response
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            elif response_text.startswith('```'):
                response_text = response_text.replace('```', '').strip()

            analysis = json.loads(response_text)

            # Add metadata
            analysis['_metadata'] = {
                'mode': 'educational',
                'model': 'gemini-2.5-flash-lite',
                'analyzed_at': datetime.now().isoformat(),
                'symbol': market_data.get('symbol', 'BTCUSDT')
            }

            print(f"✓ Educational analysis complete")
            return analysis

        except Exception as e:
            print(f"✗ Error during educational analysis: {e}")
            raise

    def _format_advanced_data(self, market_data: Dict) -> str:
        """
        Format advanced market data with real calculated metrics

        Args:
            market_data: Market data with CVD, orderbook depth, OI delta

        Returns:
            Formatted string with calculated metrics
        """
        cvd = market_data.get('cvd_trend', {})
        depth = market_data.get('orderbook_depth', {})
        oi_delta = market_data.get('oi_delta', {})
        ticker = market_data.get('ticker', {})
        funding = market_data.get('funding_rate', {})

        prompt = f"""
📊 CALCULATED ADVANCED METRICS

💹 CVD TREND (Cumulative Volume Delta)
1H CVD: {cvd.get('1h', 0):,.2f} BTC ({cvd.get('trend_1h', 'neutral')})
4H CVD: {cvd.get('4h', 0):,.2f} BTC ({cvd.get('trend_4h', 'neutral')})
24H CVD: {cvd.get('24h', 0):,.2f} BTC ({cvd.get('trend_24h', 'neutral')})

📖 ORDERBOOK DEPTH ANALYSIS
1% Depth (±${ticker.get('last_price', 0) * 0.01:,.2f}):
  Bids: {depth.get('1%', {}).get('bid_volume', 0):,.2f} BTC
  Asks: {depth.get('1%', {}).get('ask_volume', 0):,.2f} BTC
  Imbalance: {depth.get('1%', {}).get('imbalance', 0):,.2f}%

2% Depth (±${ticker.get('last_price', 0) * 0.02:,.2f}):
  Bids: {depth.get('2%', {}).get('bid_volume', 0):,.2f} BTC
  Asks: {depth.get('2%', {}).get('ask_volume', 0):,.2f} BTC
  Imbalance: {depth.get('2%', {}).get('imbalance', 0):,.2f}%

5% Depth (±${ticker.get('last_price', 0) * 0.05:,.2f}):
  Bids: {depth.get('5%', {}).get('bid_volume', 0):,.2f} BTC
  Asks: {depth.get('5%', {}).get('ask_volume', 0):,.2f} BTC
  Imbalance: {depth.get('5%', {}).get('imbalance', 0):,.2f}%

📈 FUNDING RATE HISTORY
Current Rate: {funding.get('funding_rate_percent', 0):.4f}%
Annualized: {funding.get('annualized_rate', 0):.2f}%

📊 OPEN INTEREST DELTA
Current OI: {oi_delta.get('current_oi', 0):,.2f} BTC
1H Delta: {oi_delta.get('delta_1h', 'N/A')}
4H Delta: {oi_delta.get('delta_4h', 'N/A')}
24H Delta: {oi_delta.get('delta_24h', 'N/A')}
Note: {oi_delta.get('note', '')}
"""
        return prompt

    def analyze_advanced(self, market_data: Dict) -> Dict:
        """
        QUANTRA-3: Advanced technical analysis
        Deep dive into orderbook, CVD trends, funding history, OI deltas
        For professional traders and researchers

        Args:
            market_data: Market data dictionary from BinanceClient (with include_advanced=True)

        Returns:
            Dict with advanced technical analysis
        """
        ADVANCED_PROMPT = """You are QUANTRA-3, an advanced technical analyst providing institutional-grade derivatives market analysis.

🎯 YOUR MISSION
Deliver deep technical analysis of crypto derivatives markets with multi-level orderbook depth, CVD trends, funding rate history, and OI delta breakdowns.

📊 ADVANCED ANALYSIS FRAMEWORK

1. **ORDERBOOK DEPTH ANALYSIS**
   - 1% depth: Immediate liquidity (next $870 move)
   - 2% depth: Short-term support/resistance
   - 5% depth: Major liquidity zones
   - Bid/Ask imbalance at each level
   - Spoofing detection

2. **CVD TREND ANALYSIS**
   - Current CVD delta (buying vs selling pressure)
   - 1H CVD trend (short-term flow)
   - 4H CVD trend (medium-term accumulation)
   - 24H CVD trend (daily sentiment)
   - Divergences between price and CVD

3. **FUNDING RATE HISTORY**
   - Current funding rate
   - 8-hour trend (recent shifts)
   - Funding rate momentum
   - Historical extremes context
   - Predicted next funding

4. **OPEN INTEREST DELTA**
   - 1H OI delta (immediate positioning)
   - 4H OI delta (short-term trend)
   - 24H OI delta (daily flow)
   - OI vs price correlation
   - Position building or unwinding

5. **MULTI-TIMEFRAME CONFLUENCE**
   - 1H technical score (0-100)
   - 4H technical score (0-100)
   - 8H technical score (0-100)
   - Overall confluence rating
   - Agreement/divergence analysis

6. **RISK/REWARD VALIDATION**
   - Support/resistance levels (technical)
   - Liquidity-based levels (orderbook)
   - High-probability zones
   - Invalidation levels
   - Position sizing implications

📋 OUTPUT FORMAT (JSON)
{
  "orderbook_depth": {
    "depth_1pct": {"bids": "amount", "asks": "amount", "ratio": 0.0, "imbalance": "explanation"},
    "depth_2pct": {"bids": "amount", "asks": "amount", "ratio": 0.0, "zones": "key levels"},
    "depth_5pct": {"bids": "amount", "asks": "amount", "ratio": 0.0, "major_walls": "locations"}
  },
  "cvd_analysis": {
    "current_delta": "buying/selling pressure",
    "trend_1h": "short-term flow",
    "trend_4h": "medium-term accumulation",
    "trend_24h": "daily sentiment",
    "divergences": "price vs CVD mismatches"
  },
  "funding_history": {
    "current": 0.0000,
    "trend_8h": "rising/falling/stable",
    "momentum": "accelerating/decelerating",
    "extremes_context": "historical comparison",
    "prediction": "next funding estimate"
  },
  "oi_delta": {
    "delta_1h": "+/- amount and %",
    "delta_4h": "+/- amount and %",
    "delta_24h": "+/- amount and %",
    "correlation": "OI vs price relationship",
    "interpretation": "building or unwinding"
  },
  "confluence_score": {
    "timeframe_1h": 0-100,
    "timeframe_4h": 0-100,
    "timeframe_8h": 0-100,
    "overall": 0-100,
    "analysis": "agreement or divergence"
  },
  "risk_reward": {
    "support_levels": [levels with strength],
    "resistance_levels": [levels with strength],
    "high_probability_zones": "where edge exists",
    "invalidation": "where thesis breaks",
    "position_sizing": "risk management guidance"
  },
  "timestamp": "ISO format"
}

Be technical. Be precise. Quantify everything. This is for professional traders."""

        try:
            # Format basic market data
            base_prompt = self._format_market_data(market_data)

            # Add advanced calculated metrics
            advanced_prompt = self._format_advanced_data(market_data)

            # Combine prompts
            full_prompt = base_prompt + "\n" + advanced_prompt

            print("\n📊 Generating advanced technical analysis with QUANTRA-3...")

            response = self.model.generate_content([ADVANCED_PROMPT, full_prompt])
            response_text = response.text.strip()

            # Clean response
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            elif response_text.startswith('```'):
                response_text = response_text.replace('```', '').strip()

            analysis = json.loads(response_text)

            # Add metadata
            analysis['_metadata'] = {
                'mode': 'advanced',
                'model': 'gemini-2.5-flash-lite',
                'analyzed_at': datetime.now().isoformat(),
                'symbol': market_data.get('symbol', 'BTCUSDT')
            }

            print(f"✓ Advanced technical analysis complete")
            return analysis

        except Exception as e:
            print(f"✗ Error during advanced analysis: {e}")
            raise

    def analyze_raw_data(self, market_data: Dict) -> Dict:
        """
        QUANTRA-4: Educational raw data interpretation
        AI explains what each metric means without predictions
        
        Args:
            market_data: Market data dictionary from BinanceClient

        Returns:
            Dict with educational interpretations of raw data
        """
        RAW_DATA_PROMPT = """You are an educational market data analyst. Your job is to explain what raw market data means RIGHT NOW - not to predict the future.

🎯 YOUR MISSION
For each metric provided, explain in 1-2 clear sentences:
1. What the number means RIGHT NOW
2. Whether it's bullish, bearish, or neutral
3. What it suggests about current market structure

Keep explanations simple and educational. No predictions - just data interpretation.

📋 OUTPUT FORMAT (JSON)
{
  "price_interpretation": "1-2 sentences about what current price action suggests",
  "oi_interpretation": "1-2 sentences about what OI tells us about market positioning",
  "funding_interpretation": "1-2 sentences about what funding rate reveals",
  "positioning_interpretation": "1-2 sentences about top trader vs retail positioning",
  "orderbook_interpretation": "1-2 sentences about bid/ask balance",
  "flow_interpretation": "1-2 sentences about CVD and trade flow",
  "key_takeaways": ["3-4 bullet points of most important insights"],
  "what_to_watch": ["3-4 bullet points of key metrics to monitor"]
}

Remember: NO predictions. Just explain what the data shows RIGHT NOW."""

        try:
            # Format market data into prompt
            prompt = self._format_market_data(market_data)
            
            # Add CVD if available
            if market_data.get('cvd_trend'):
                cvd = market_data['cvd_trend']
                prompt += f"\n\n💹 TRADE FLOW (CVD):\n"
                prompt += f"1H CVD: {cvd.get('1h', 0):,.2f} BTC ({cvd.get('trend_1h', 'neutral')})\n"
                prompt += f"4H CVD: {cvd.get('4h', 0):,.2f} BTC ({cvd.get('trend_4h', 'neutral')})\n"
                prompt += f"24H CVD: {cvd.get('24h', 0):,.2f} BTC ({cvd.get('trend_24h', 'neutral')})\n"

            print("\n📚 Generating educational data interpretation with QUANTRA-4...")

            response = self.model.generate_content([RAW_DATA_PROMPT, prompt])
            response_text = response.text.strip()

            # Clean response
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            elif response_text.startswith('```'):
                response_text = response_text.replace('```', '').strip()

            analysis = json.loads(response_text)

            # Add metadata
            analysis['_metadata'] = {
                'mode': 'raw_data',
                'model': 'gemini-2.5-flash-lite',
                'analyzed_at': datetime.now().isoformat(),
                'symbol': market_data.get('symbol', 'BTCUSDT')
            }

            print(f"✓ Raw data interpretation complete")
            return analysis

        except Exception as e:
            print(f"✗ Error during raw data analysis: {e}")
            raise
