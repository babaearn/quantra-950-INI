"""
Message formatters for Telegram bot
Converts analysis data to formatted Telegram messages
"""
from typing import Dict, List
from datetime import datetime


def format_analysis_message(analysis: Dict, symbol: str = "BTCUSDT") -> str:
    """
    Format AI analysis into a nice Telegram message

    Args:
        analysis: Analysis dictionary from GeminiAnalyzer
        symbol: Trading symbol

    Returns:
        Formatted message string for Telegram
    """
    # Signal emoji
    signal_emoji = {
        "LONG": "🟢",
        "SHORT": "🔴",
        "NEUTRAL": "🟡"
    }

    signal = analysis.get('signal', 'UNKNOWN')
    confidence = analysis.get('confidence', 0)
    emoji = signal_emoji.get(signal, "⚪")

    # Build message
    lines = [
        "🧠 *QUANTRA-950 AI ANALYSIS*",
        "━━━━━━━━━━━━━━━━━━━━",
        f"📊 Symbol: `{symbol}`",
        "",
        f"{emoji} *SIGNAL: {signal}*",
        f"📈 Confidence: *{confidence}/100*",
        ""
    ]

    # Entry and risk management
    if analysis.get('entry_price') is not None:
        lines.append(f"💰 Entry: `${analysis['entry_price']:,.2f}`")
    else:
        lines.append(f"💰 Entry: `N/A (No trade)`")

    if analysis.get('stop_loss') is not None:
        lines.append(f"🛑 Stop: `${analysis['stop_loss']:,.2f}`")
    else:
        lines.append(f"🛑 Stop: `N/A (No trade)`")

    # Targets
    if analysis.get('targets') and analysis['targets'] is not None:
        targets = analysis['targets']
        lines.append("")
        lines.append("🎯 *TARGETS*")
        if targets.get('tp1') is not None:
            lines.append(f"   TP1: `${targets['tp1']:,.2f}`")
        if targets.get('tp2') is not None:
            lines.append(f"   TP2: `${targets['tp2']:,.2f}`")
        if targets.get('tp3') is not None:
            lines.append(f"   TP3: `${targets['tp3']:,.2f}`")
    else:
        lines.append("")
        lines.append("🎯 Targets: `N/A (No trade)`")

    # Risk/Reward
    lines.append("")
    if analysis.get('risk_reward_ratio') is not None:
        lines.append(f"📊 Risk/Reward: `1:{analysis['risk_reward_ratio']:.2f}`")
    else:
        lines.append(f"📊 Risk/Reward: `N/A`")

    # Timeframe alignment
    if 'timeframe_alignment' in analysis:
        tf = analysis['timeframe_alignment']
        lines.append("")
        lines.append("⏰ *TIMEFRAME ALIGNMENT*")
        lines.append(f"   8H: `{tf.get('8h', 'N/A')}`")
        lines.append(f"   4H: `{tf.get('4h', 'N/A')}`")
        lines.append(f"   1H: `{tf.get('1h', 'N/A')}`")

    # Key levels
    if 'key_levels' in analysis:
        levels = analysis['key_levels']

        if levels.get('resistance'):
            lines.append("")
            lines.append("🔺 *RESISTANCE*")
            for r in levels['resistance'][:3]:  # Top 3
                lines.append(f"   `${r:,.2f}`")

        if levels.get('support'):
            lines.append("")
            lines.append("🔻 *SUPPORT*")
            for s in levels['support'][:3]:  # Top 3
                lines.append(f"   `${s:,.2f}`")

    # Market regime
    if 'market_regime' in analysis:
        lines.append("")
        lines.append(f"📊 Regime: `{analysis['market_regime']}`")

    # Narrative
    if 'narrative' in analysis:
        lines.append("")
        lines.append("📝 *ANALYSIS*")
        lines.append(f"_{analysis['narrative']}_")

    # Warnings
    if analysis.get('warnings'):
        lines.append("")
        lines.append("⚠️ *WARNINGS*")
        for warning in analysis['warnings']:
            lines.append(f"• {warning}")

    # Metadata
    if '_metadata' in analysis:
        meta = analysis['_metadata']
        lines.append("")
        lines.append("━━━━━━━━━━━━━━━━━━━━")
        lines.append(f"🤖 Model: `{meta.get('model', 'N/A')}`")

        # Parse timestamp
        analyzed_at = meta.get('analyzed_at', '')
        if analyzed_at:
            try:
                dt = datetime.fromisoformat(analyzed_at)
                time_str = dt.strftime('%Y-%m-%d %H:%M:%S UTC')
                lines.append(f"⏱ Analyzed: `{time_str}`")
            except:
                lines.append(f"⏱ Analyzed: `{analyzed_at}`")

    return "\n".join(lines)


def format_error_message(error: str, symbol: str = "BTCUSDT") -> str:
    """
    Format error message for Telegram

    Args:
        error: Error message
        symbol: Trading symbol

    Returns:
        Formatted error message
    """
    return f"""❌ *ERROR*

Symbol: `{symbol}`

{error}

Please try again or contact support if the issue persists."""


def format_welcome_message() -> str:
    """
    Format welcome message for /start command

    Returns:
        Welcome message string
    """
    return """🚀 *Welcome to QUANTRA-950*

_AI-Powered Crypto Trading Intelligence_

━━━━━━━━━━━━━━━━━━━━

*FOUR ANALYSIS MODES*

/q1 BTC - Quick Signal
🎯 Fast trading signals with entry/stop/targets

/q2 BTC - Educational
🎓 Market psychology & smart money insights

/q3 BTC - Advanced Technical
📊 Deep orderbook, CVD, funding analysis

/q4 BTC - Raw Data
📊 Pure market data with optional AI insights

━━━━━━━━━━━━━━━━━━━━

*FEATURES*
🧠 Gemini AI market analysis
📊 Multi-timeframe signals (8H/4H/1H)
💰 Entry, stop, and target levels
⚖️ Long/short positioning analysis
📈 Open interest & funding rates
🎯 High-conviction trade setups
🎓 Educational market insights
📊 Advanced technical deep dives
📈 Raw data mode (save AI quota)

━━━━━━━━━━━━━━━━━━━━

*HOW IT WORKS*
1. Choose your mode: /q1, /q2, /q3, or /q4
2. AI analyzes real-time market data
3. Get structured analysis
4. Make informed decisions

━━━━━━━━━━━━━━━━━━━━

Ready to receive alpha! 🎯

Try: /q1 BTC | /q2 BTC | /q3 BTC | /q4 BTC"""


def format_help_message() -> str:
    """
    Format help message

    Returns:
        Help message string
    """
    return """📚 *QUANTRA-950 HELP*

━━━━━━━━━━━━━━━━━━━━

*COMMANDS*

/start - Show welcome message
/help - Show this help message
/q1 <SYMBOL> - Quick AI signal
/q2 <SYMBOL> - Educational analysis
/q3 <SYMBOL> - Advanced technical
/q4 <SYMBOL> - Raw data (no AI)
/q4 ai <SYMBOL> - Raw data + AI

━━━━━━━━━━━━━━━━━━━━

*EXAMPLES*

/q1 BTC - Quick trading signal
/q2 BTC - Deep market psychology
/q3 BTC - Technical deep dive
/q4 BTC - Raw data only
/q4 ai BTC - Raw data + AI explanations

━━━━━━━━━━━━━━━━━━━━

*SIGNALS*

🟢 *LONG* - Bullish setup
🔴 *SHORT* - Bearish setup
🟡 *NEUTRAL* - No clear edge

━━━━━━━━━━━━━━━━━━━━

*CONFIDENCE LEVELS*

90-100: Extremely high conviction
70-89: High conviction
50-69: Moderate conviction
30-49: Low conviction
0-29: Very low conviction

━━━━━━━━━━━━━━━━━━━━

*RISK MANAGEMENT*

Always use stop losses!
Position size based on confidence
Never risk more than 1-2% per trade

━━━━━━━━━━━━━━━━━━━━

*SAVE AI QUOTA*

Use /q4 BTC for raw data without using AI quota
Use /q4 ai BTC when you want AI interpretation

━━━━━━━━━━━━━━━━━━━━

Need more help? Contact support."""


def format_educational_analysis(analysis: Dict, symbol: str = "BTCUSDT") -> List[str]:
    """
    Format QUANTRA-2 educational analysis into Telegram messages (2 parts)

    Args:
        analysis: Educational analysis dictionary from GeminiAnalyzer
        symbol: Trading symbol

    Returns:
        List of 2 formatted message strings for Telegram
    """
    price = analysis.get('price', 'N/A')

    # PART 1: What's Happening + Smart Money Insights
    part1_lines = [
        "📊 *QUANTRA-2 EDUCATIONAL ANALYSIS*",
        f"Symbol: `{symbol}`",
        f"Price: `${price}` " if price != 'N/A' else "",
        "",
        "*Part 1 of 2*",
        "━━━━━━━━━━━━━━━━━━━━",
        ""
    ]

    # What's Happening Now
    if 'whats_happening' in analysis:
        wh = analysis['whats_happening']
        part1_lines.append("📈 *WHAT'S HAPPENING NOW*")
        part1_lines.append("")

        if wh.get('price_action'):
            part1_lines.append(f"Price Action:")
            part1_lines.append(f"{wh['price_action']}")
            part1_lines.append("")

        if wh.get('volume_trend'):
            part1_lines.append(f"Volume Trend:")
            part1_lines.append(f"{wh['volume_trend']}")
            part1_lines.append("")

        if wh.get('volatility'):
            part1_lines.append(f"Volatility:")
            part1_lines.append(f"{wh['volatility']}")
            part1_lines.append("")

        if wh.get('smart_money'):
            part1_lines.append(f"Smart Money Activity:")
            part1_lines.append(f"{wh['smart_money']}")

        part1_lines.append("")
        part1_lines.append("━━━━━━━━━━━━━━━━━━━━")
        part1_lines.append("")

    # Smart Money Insights
    if 'smart_money_insights' in analysis:
        sm = analysis['smart_money_insights']
        part1_lines.append("🧠 *SMART MONEY INSIGHTS*")
        part1_lines.append("")

        if sm.get('institution_activity'):
            part1_lines.append(f"What Institutions Are Doing:")
            part1_lines.append(f"{sm['institution_activity']}")
            part1_lines.append("")

        if sm.get('orderbook_psychology'):
            part1_lines.append(f"Order Book Psychology:")
            part1_lines.append(f"{sm['orderbook_psychology']}")
            part1_lines.append("")

        if sm.get('whale_activity'):
            part1_lines.append(f"Whale Activity:")
            part1_lines.append(f"{sm['whale_activity']}")

        part1_lines.append("")
        part1_lines.append("━━━━━━━━━━━━━━━━━━━━")

    # PART 2: Market Psychology + Educational Insights + Evolution
    part2_lines = [
        "📊 *QUANTRA-2 EDUCATIONAL ANALYSIS*",
        f"Symbol: `{symbol}`",
        "",
        "*Part 2 of 2*",
        "━━━━━━━━━━━━━━━━━━━━",
        ""
    ]

    # Market Psychology
    if 'market_psychology' in analysis:
        mp = analysis['market_psychology']
        part2_lines.append("🎭 *MARKET PSYCHOLOGY*")
        part2_lines.append("")

        if mp.get('crowd_behavior'):
            part2_lines.append(f"Crowd Behavior:")
            part2_lines.append(f"{mp['crowd_behavior']}")
            part2_lines.append("")

        if mp.get('sentiment'):
            part2_lines.append(f"Sentiment:")
            part2_lines.append(f"{mp['sentiment']}")
            part2_lines.append("")

        if mp.get('potential_traps'):
            part2_lines.append(f"Potential Traps:")
            for trap in mp['potential_traps']:
                part2_lines.append(f"• {trap}")

        part2_lines.append("")
        part2_lines.append("━━━━━━━━━━━━━━━━━━━━")
        part2_lines.append("")

    # Key Data Points
    if 'key_data' in analysis:
        kd = analysis['key_data']
        part2_lines.append("📊 *KEY DATA POINTS*")
        part2_lines.append("")

        if kd.get('technical'):
            part2_lines.append(f"Technical Metrics:")
            part2_lines.append(f"{kd['technical']}")
            part2_lines.append("")

        if kd.get('derivatives'):
            part2_lines.append(f"Derivatives Data:")
            part2_lines.append(f"{kd['derivatives']}")
            part2_lines.append("")

        if kd.get('volume_profile'):
            part2_lines.append(f"Volume Profile:")
            part2_lines.append(f"{kd['volume_profile']}")

        part2_lines.append("")
        part2_lines.append("━━━━━━━━━━━━━━━━━━━━")
        part2_lines.append("")

    # Educational Insights
    if 'educational_insights' in analysis:
        ei = analysis['educational_insights']
        part2_lines.append("💡 *EDUCATIONAL INSIGHTS*")
        part2_lines.append("")

        if ei.get('what_this_means'):
            part2_lines.append(f"What This Means:")
            part2_lines.append(f"{ei['what_this_means']}")
            part2_lines.append("")

        if ei.get('things_to_watch'):
            part2_lines.append(f"Things to Watch:")
            for thing in ei['things_to_watch']:
                part2_lines.append(f"• {thing}")
            part2_lines.append("")

        if ei.get('market_context'):
            part2_lines.append(f"Market Context:")
            part2_lines.append(f"{ei['market_context']}")

        part2_lines.append("")
        part2_lines.append("━━━━━━━━━━━━━━━━━━━━")
        part2_lines.append("")

    # Evolution Notes
    if 'evolution_notes' in analysis:
        en = analysis['evolution_notes']
        part2_lines.append("🔄 *EVOLUTION NOTES*")
        part2_lines.append("")

        if en.get('learning'):
            part2_lines.append(f"What I'm Learning:")
            part2_lines.append(f"{en['learning']}")
            part2_lines.append("")

        if en.get('pattern_success'):
            part2_lines.append(f"Pattern Success:")
            part2_lines.append(f"{en['pattern_success']}")
            part2_lines.append("")

        if en.get('improvements'):
            part2_lines.append(f"Improving Analysis:")
            part2_lines.append(f"{en['improvements']}")

        part2_lines.append("")
        part2_lines.append("━━━━━━━━━━━━━━━━━━━━")

    # Add metadata to part 2
    if '_metadata' in analysis:
        meta = analysis['_metadata']
        part2_lines.append("")
        part2_lines.append(f"🤖 Model: {meta.get('model', 'N/A')}")

    return ["\n".join(part1_lines), "\n".join(part2_lines)]


def format_advanced_analysis(analysis: Dict, symbol: str = "BTCUSDT") -> List[str]:
    """
    Format QUANTRA-3 advanced technical analysis into Telegram messages (2 parts)

    Args:
        analysis: Advanced analysis dictionary from GeminiAnalyzer
        symbol: Trading symbol

    Returns:
        List of 2 formatted message strings for Telegram
    """
    # PART 1: Orderbook + Funding + Confluence
    part1_lines = [
        "📊 *QUANTRA-3 TECHNICAL ANALYSIS*",
        f"Symbol: `{symbol}`",
        "",
        "*Part 1 of 2*",
        "━━━━━━━━━━━━━━━━━━━━",
        ""
    ]

    # Orderbook Depth
    if 'orderbook_depth' in analysis:
        od = analysis['orderbook_depth']
        part1_lines.append("📖 *ORDERBOOK DEPTH ANALYSIS*")
        part1_lines.append("")

        if od.get('depth_1pct'):
            d1 = od['depth_1pct']
            part1_lines.append(f"1% Depth (Immediate Liquidity):")
            part1_lines.append(f"• Bids: {d1.get('bids', 'N/A')}")
            part1_lines.append(f"• Asks: {d1.get('asks', 'N/A')}")
            part1_lines.append(f"• Ratio: {d1.get('ratio', 'N/A')}")
            part1_lines.append(f"• {d1.get('imbalance', '')}")
            part1_lines.append("")

        if od.get('depth_2pct'):
            d2 = od['depth_2pct']
            part1_lines.append(f"2% Depth (Short-term):")
            part1_lines.append(f"• Bids: {d2.get('bids', 'N/A')}")
            part1_lines.append(f"• Asks: {d2.get('asks', 'N/A')}")
            part1_lines.append(f"• Key Zones: {d2.get('zones', 'N/A')}")
            part1_lines.append("")

        if od.get('depth_5pct'):
            d5 = od['depth_5pct']
            part1_lines.append(f"5% Depth (Major Liquidity):")
            part1_lines.append(f"• Bids: {d5.get('bids', 'N/A')}")
            part1_lines.append(f"• Asks: {d5.get('asks', 'N/A')}")
            part1_lines.append(f"• Walls: {d5.get('major_walls', 'N/A')}")

        part1_lines.append("")
        part1_lines.append("━━━━━━━━━━━━━━━━━━━━")
        part1_lines.append("")

    # Funding History
    if 'funding_history' in analysis:
        fh = analysis['funding_history']
        part1_lines.append("💰 *FUNDING RATE HISTORY*")
        part1_lines.append("")
        part1_lines.append(f"Current: {fh.get('current', 'N/A')}%")
        part1_lines.append(f"8H Trend: {fh.get('trend_8h', 'N/A')}")
        part1_lines.append(f"Momentum: {fh.get('momentum', 'N/A')}")
        part1_lines.append(f"Context: {fh.get('extremes_context', 'N/A')}")
        if fh.get('prediction'):
            part1_lines.append(f"Prediction: {fh['prediction']}")
        part1_lines.append("")
        part1_lines.append("━━━━━━━━━━━━━━━━━━━━")
        part1_lines.append("")

    # Confluence Score
    if 'confluence_score' in analysis:
        cs = analysis['confluence_score']
        part1_lines.append("🎯 *MULTI-TIMEFRAME CONFLUENCE*")
        part1_lines.append("")
        part1_lines.append(f"1H Score: {cs.get('timeframe_1h', 'N/A')}/100")
        part1_lines.append(f"4H Score: {cs.get('timeframe_4h', 'N/A')}/100")
        part1_lines.append(f"8H Score: {cs.get('timeframe_8h', 'N/A')}/100")
        part1_lines.append(f"Overall: {cs.get('overall', 'N/A')}/100")
        if cs.get('analysis'):
            part1_lines.append(f"{cs['analysis']}")
        part1_lines.append("")
        part1_lines.append("━━━━━━━━━━━━━━━━━━━━")

    # PART 2: CVD Analysis + OI Delta + Risk/Reward
    part2_lines = [
        "📊 *QUANTRA-3 TECHNICAL ANALYSIS*",
        f"Symbol: `{symbol}`",
        "",
        "*Part 2 of 2*",
        "━━━━━━━━━━━━━━━━━━━━",
        ""
    ]

    # CVD Analysis
    if 'cvd_analysis' in analysis:
        cvd = analysis['cvd_analysis']
        part2_lines.append("📈 *CVD TREND ANALYSIS*")
        part2_lines.append("")
        part2_lines.append(f"Current Delta: {cvd.get('current_delta', 'N/A')}")
        part2_lines.append(f"1H Trend: {cvd.get('trend_1h', 'N/A')}")
        part2_lines.append(f"4H Trend: {cvd.get('trend_4h', 'N/A')}")
        part2_lines.append(f"24H Trend: {cvd.get('trend_24h', 'N/A')}")
        if cvd.get('divergences'):
            part2_lines.append(f"Divergences: {cvd['divergences']}")
        part2_lines.append("")
        part2_lines.append("━━━━━━━━━━━━━━━━━━━━")
        part2_lines.append("")

    # Risk/Reward
    if 'risk_reward' in analysis:
        rr = analysis['risk_reward']
        part2_lines.append("⚖️ *RISK/REWARD VALIDATION*")
        part2_lines.append("")

        if rr.get('support_levels'):
            part2_lines.append(f"Support Levels:")
            for level in rr['support_levels']:
                part2_lines.append(f"• {level}")
            part2_lines.append("")

        if rr.get('resistance_levels'):
            part2_lines.append(f"Resistance Levels:")
            for level in rr['resistance_levels']:
                part2_lines.append(f"• {level}")
            part2_lines.append("")

        if rr.get('high_probability_zones'):
            part2_lines.append(f"High Probability: {rr['high_probability_zones']}")
            part2_lines.append("")

        if rr.get('invalidation'):
            part2_lines.append(f"Invalidation: {rr['invalidation']}")
            part2_lines.append("")

        if rr.get('position_sizing'):
            part2_lines.append(f"Position Sizing: {rr['position_sizing']}")

        part2_lines.append("")
        part2_lines.append("━━━━━━━━━━━━━━━━━━━━")

    # Add metadata to part 2
    if '_metadata' in analysis:
        meta = analysis['_metadata']
        part2_lines.append("")
        part2_lines.append(f"🤖 Model: {meta.get('model', 'N/A')}")

    return ["\n".join(part1_lines), "\n".join(part2_lines)]

def format_raw_data_only(market_data: Dict, symbol: str = "BTCUSDT") -> List[str]:
    """
    Format raw market data without AI explanations (QUANTRA-4 mode 1)

    Args:
        market_data: Market data dictionary from BinanceClient
        symbol: Trading symbol

    Returns:
        List of 2 formatted message strings for Telegram
    """
    ticker = market_data.get('ticker', {})
    oi = market_data.get('open_interest', {})
    funding = market_data.get('funding_rate', {})
    ratio = market_data.get('long_short_ratio', {})
    orderbook = market_data.get('orderbook', {})
    cvd = market_data.get('cvd_trend', {}) if market_data.get('cvd_trend') else {}

    # PART 1: Price, OI, Funding, Positioning
    part1_lines = [
        "📊 *QUANTRA-4 RAW DATA*",
        f"Symbol: {symbol}",
        "",
        "*Part 1 of 2*",
        "━━━━━━━━━━━━━━━━━━━━",
        "",
        "💰 *PRICE DATA*",
        f"Current: ${ticker.get('last_price', 0):,.2f}",
        f"24h High: ${ticker.get('high_price', 0):,.2f}",
        f"24h Low: ${ticker.get('low_price', 0):,.2f}",
        f"24h Change: {ticker.get('price_change_percent', 0):+.2f}%",
        f"24h Volume: {ticker.get('volume', 0):,.2f} BTC",
        f"24h Turnover: ${ticker.get('quote_volume', 0) / 1e9:.2f}B",
        "",
        "What this means:",
        "Price near 24h low = selling pressure",
        "High volume = active market participation",
        "",
        "━━━━━━━━━━━━━━━━━━━━",
        "",
        "📊 *OPEN INTEREST*",
        f"Current OI: {oi.get('open_interest', 0):,.2f} BTC",
        f"OI Value: ${oi.get('open_interest_value', 0) / 1e9:.2f}B",
        "",
        "What this means:",
        "Rising OI + rising price = strong trend",
        "Rising OI + flat price = big move coming",
        "",
        "━━━━━━━━━━━━━━━━━━━━",
        "",
        "💸 *FUNDING RATE*",
        f"Current: {funding.get('funding_rate_percent', 0):.4f}%",
        f"Annualized: {funding.get('annualized_rate', 0):.2f}%",
        "",
        "What this means:",
        "Positive = longs pay shorts (bullish bias)",
        ">0.05% = overheated longs",
        "<-0.05% = overheated shorts",
        "",
        "━━━━━━━━━━━━━━━━━━━━",
        "",
        "⚖️ *POSITIONING*",
        "Top Traders:",
        f"• Long: {ratio.get('long_ratio', 0) * 100:.1f}%",
        f"• Short: {ratio.get('short_ratio', 0) * 100:.1f}%",
        f"• Ratio: {ratio.get('long_short_ratio', 0):.2f}:1",
        "",
        "What this means:",
        "Extreme retail positioning = contrarian signal",
        "Follow smart money when divergence occurs",
        "",
        "━━━━━━━━━━━━━━━━━━━━"
    ]

    # PART 2: Orderbook, Trade Flow, Guide
    part2_lines = [
        "📊 *QUANTRA-4 RAW DATA*",
        f"Symbol: {symbol}",
        "",
        "*Part 2 of 2*",
        "━━━━━━━━━━━━━━━━━━━━",
        "",
        "📖 *ORDERBOOK*",
        f"Best Bid: ${orderbook.get('best_bid', 0):,.2f}",
        f"Best Ask: ${orderbook.get('best_ask', 0):,.2f}",
        f"Spread: ${orderbook.get('spread', 0):.2f}",
        f"Bid/Ask Ratio: {orderbook.get('bid_ask_ratio', 0):.2f}",
        "",
        "What this means:",
        "Ratio >1.0 = more buyers (bullish)",
        "Ratio <1.0 = more sellers (bearish)",
        "",
        "━━━━━━━━━━━━━━━━━━━━",
        ""
    ]

    # Add CVD if available
    if cvd:
        part2_lines.extend([
            "📈 *TRADE FLOW (CVD)*",
            f"1H: {cvd.get('1h', 0):+,.2f} BTC ({cvd.get('trend_1h', 'neutral')})",
            f"4H: {cvd.get('4h', 0):+,.2f} BTC ({cvd.get('trend_4h', 'neutral')})",
            f"24H: {cvd.get('24h', 0):+,.2f} BTC ({cvd.get('trend_24h', 'neutral')})",
            "",
            "What this means:",
            "Negative CVD = distribution (selling)",
            "Positive CVD = accumulation (buying)",
            "",
            "━━━━━━━━━━━━━━━━━━━━",
            ""
        ])

    part2_lines.extend([
        "🔍 *QUICK GUIDE*",
        "",
        "*Bullish Signs:*",
        "• Price rising + volume high",
        "• OI rising with price",
        "• Positive CVD trend",
        "• Bid-heavy orderbook",
        "",
        "*Bearish Signs:*",
        "• Price falling + volume high",
        "• OI flat while price moves",
        "• Negative CVD trend",
        "• Ask-heavy orderbook",
        "",
        "*Reversal Signs:*",
        "• Extreme funding (>0.05%)",
        "• Extreme L/S ratio (>3:1)",
        "• CVD divergence from price",
        "",
        "━━━━━━━━━━━━━━━━━━━━",
        f"⏱ Snapshot: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}"
    ])

    return ["\n".join(part1_lines), "\n".join(part2_lines)]


def format_raw_data_with_ai(market_data: Dict, ai_analysis: Dict, symbol: str = "BTCUSDT") -> List[str]:
    """
    Format raw market data WITH AI explanations (QUANTRA-4 mode 2)

    Args:
        market_data: Market data dictionary from BinanceClient
        ai_analysis: AI analysis dictionary from GeminiAnalyzer
        symbol: Trading symbol

    Returns:
        List of 2 formatted message strings for Telegram
    """
    ticker = market_data.get('ticker', {})
    oi = market_data.get('open_interest', {})
    funding = market_data.get('funding_rate', {})
    ratio = market_data.get('long_short_ratio', {})
    orderbook = market_data.get('orderbook', {})
    cvd = market_data.get('cvd_trend', {}) if market_data.get('cvd_trend') else {}

    # PART 1: Price, OI, Funding, Positioning with AI
    part1_lines = [
        "📊 *QUANTRA-4 RAW DATA + AI*",
        f"Symbol: {symbol}",
        "",
        "*Part 1 of 2*",
        "━━━━━━━━━━━━━━━━━━━━",
        "",
        "💰 *PRICE DATA*",
        f"Current: ${ticker.get('last_price', 0):,.2f}",
        f"24h High: ${ticker.get('high_price', 0):,.2f}",
        f"24h Low: ${ticker.get('low_price', 0):,.2f}",
        f"24h Change: {ticker.get('price_change_percent', 0):+.2f}%",
        "",
        "🤖 AI Insight:",
        f"{ai_analysis.get('price_interpretation', 'N/A')}",
        "",
        "━━━━━━━━━━━━━━━━━━━━",
        "",
        "📊 *OPEN INTEREST*",
        f"Current: {oi.get('open_interest', 0):,.2f} BTC",
        f"Value: ${oi.get('open_interest_value', 0) / 1e9:.2f}B",
        "",
        "🤖 AI Insight:",
        f"{ai_analysis.get('oi_interpretation', 'N/A')}",
        "",
        "━━━━━━━━━━━━━━━━━━━━",
        "",
        "💸 *FUNDING RATE*",
        f"Current: {funding.get('funding_rate_percent', 0):.4f}%",
        "",
        "🤖 AI Insight:",
        f"{ai_analysis.get('funding_interpretation', 'N/A')}",
        "",
        "━━━━━━━━━━━━━━━━━━━━",
        "",
        "⚖️ *POSITIONING*",
        f"Top Traders: {ratio.get('long_short_ratio', 0):.2f}:1",
        "",
        "🤖 AI Insight:",
        f"{ai_analysis.get('positioning_interpretation', 'N/A')}",
        "",
        "━━━━━━━━━━━━━━━━━━━━"
    ]

    # PART 2: Orderbook, CVD, Takeaways with AI
    part2_lines = [
        "📊 *QUANTRA-4 RAW DATA + AI*",
        f"Symbol: {symbol}",
        "",
        "*Part 2 of 2*",
        "━━━━━━━━━━━━━━━━━━━━",
        "",
        "📖 *ORDERBOOK*",
        f"Bid/Ask Ratio: {orderbook.get('bid_ask_ratio', 0):.2f}",
        "",
        "🤖 AI Insight:",
        f"{ai_analysis.get('orderbook_interpretation', 'N/A')}",
        "",
        "━━━━━━━━━━━━━━━━━━━━",
        ""
    ]

    # Add CVD if available
    if cvd:
        part2_lines.extend([
            "📈 *CVD FLOW*",
            f"1H: {cvd.get('1h', 0):+,.2f} BTC",
            f"4H: {cvd.get('4h', 0):+,.2f} BTC",
            f"24H: {cvd.get('24h', 0):+,.2f} BTC",
            "",
            "🤖 AI Insight:",
            f"{ai_analysis.get('flow_interpretation', 'N/A')}",
            "",
            "━━━━━━━━━━━━━━━━━━━━",
            ""
        ])

    # Add key takeaways
    part2_lines.extend([
        "💡 *KEY TAKEAWAYS*"
    ])

    for takeaway in ai_analysis.get('key_takeaways', []):
        part2_lines.append(f"• {takeaway}")

    part2_lines.extend([
        "",
        "━━━━━━━━━━━━━━━━━━━━",
        "",
        "👀 *WHAT TO WATCH*"
    ])

    for watch_item in ai_analysis.get('what_to_watch', []):
        part2_lines.append(f"• {watch_item}")

    part2_lines.extend([
        "",
        "━━━━━━━━━━━━━━━━━━━━",
        f"🤖 Model: {ai_analysis.get('_metadata', {}).get('model', 'gemini-2.5-flash-lite')}",
        f"⏱ Analyzed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}"
    ])

    return ["\n".join(part1_lines), "\n".join(part2_lines)]
