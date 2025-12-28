"""
Gemini AI Analyzer for Quantra-950
Advanced market intelligence using Google Gemini 2.5 Flash
"""
import google.generativeai as genai
from config.settings import settings
import json
from typing import Dict, Optional, List
from datetime import datetime


class GeminiAnalyzer:
    """
    AI-powered market analyzer using Gemini 2.5 Flash
    Implements evolutionary learning and multi-timeframe analysis
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

        # Use Gemini 2.5 Flash for speed and efficiency
        self.model = genai.GenerativeModel(
            model_name='gemini-2.0-flash-exp',
            generation_config={
                'temperature': 0.3,  # Lower temperature for more consistent analysis
                'top_p': 0.95,
                'top_k': 40,
                'max_output_tokens': 2048,
            }
        )

        print(f"✓ Gemini AI analyzer initialized (Model: gemini-2.0-flash-exp)")

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
            print("\n🤖 Generating AI analysis with Gemini 2.0 Flash...")
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
                'model': 'gemini-2.0-flash-exp',
                'analyzed_at': datetime.now().isoformat(),
                'prompt_tokens': len(prompt.split()),
                'symbol': market_data.get('symbol', 'BTCUSDT')
            }

            print(f"✓ AI analysis complete")
            return analysis

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
        print(f"\n💰 ENTRY PRICE: ${analysis['entry_price']:,.2f}")
        print(f"🛑 STOP LOSS: ${analysis['stop_loss']:,.2f}")

        if 'targets' in analysis:
            targets = analysis['targets']
            print(f"🎯 TARGETS:")
            print(f"   TP1: ${targets.get('tp1', 0):,.2f}")
            print(f"   TP2: ${targets.get('tp2', 0):,.2f}")
            print(f"   TP3: ${targets.get('tp3', 0):,.2f}")

        if 'risk_reward_ratio' in analysis:
            print(f"📈 RISK/REWARD: 1:{analysis['risk_reward_ratio']:.2f}")

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
