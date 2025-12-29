"""
Message formatters for Telegram bot
Converts analysis data to formatted Telegram messages
"""
from typing import Dict
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

*THREE ANALYSIS MODES*

/q1 BTC - Quick Signal
🎯 Fast trading signals with entry/stop/targets

/q2 BTC - Educational
🎓 Market psychology & smart money insights

/q3 BTC - Advanced Technical
📊 Deep orderbook, CVD, funding analysis

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

━━━━━━━━━━━━━━━━━━━━

*HOW IT WORKS*
1. Choose your mode: /q1, /q2, or /q3
2. AI analyzes real-time market data
3. Get structured analysis
4. Make informed decisions

━━━━━━━━━━━━━━━━━━━━

Ready to receive alpha! 🎯

Try: /q1 BTC | /q2 BTC | /q3 BTC"""


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

━━━━━━━━━━━━━━━━━━━━

*EXAMPLES*

/q1 BTC - Quick trading signal
/q2 BTC - Deep market psychology
/q3 BTC - Technical deep dive

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

Need more help? Contact support."""


def format_educational_analysis(analysis: Dict, symbol: str = "BTCUSDT") -> str:
    """
    Format QUANTRA-2 educational analysis into Telegram message

    Args:
        analysis: Educational analysis dictionary from GeminiAnalyzer
        symbol: Trading symbol

    Returns:
        Formatted message string for Telegram
    """
    price = analysis.get('price', 'N/A')

    lines = [
        "📊 *QUANTRA-2 DEEP ANALYSIS*",
        f"Symbol: `{symbol}`",
        f"Price: `${price}` " if price != 'N/A' else "",
        "",
        "━━━━━━━━━━━━━━━━━━━━",
        ""
    ]

    # What's Happening Now
    if 'whats_happening' in analysis:
        wh = analysis['whats_happening']
        lines.append("📈 *WHAT'S HAPPENING NOW*")
        lines.append("")

        if wh.get('price_action'):
            lines.append(f"Price Action:")
            lines.append(f"_{wh['price_action']}_")
            lines.append("")

        if wh.get('volume_trend'):
            lines.append(f"Volume Trend:")
            lines.append(f"_{wh['volume_trend']}_")
            lines.append("")

        if wh.get('volatility'):
            lines.append(f"Volatility:")
            lines.append(f"_{wh['volatility']}_")
            lines.append("")

        if wh.get('smart_money'):
            lines.append(f"Smart Money Activity:")
            lines.append(f"_{wh['smart_money']}_")

        lines.append("")
        lines.append("━━━━━━━━━━━━━━━━━━━━")
        lines.append("")

    # Smart Money Insights
    if 'smart_money_insights' in analysis:
        sm = analysis['smart_money_insights']
        lines.append("🧠 *SMART MONEY INSIGHTS*")
        lines.append("")

        if sm.get('institution_activity'):
            lines.append(f"What Institutions Are Doing:")
            lines.append(f"_{sm['institution_activity']}_")
            lines.append("")

        if sm.get('orderbook_psychology'):
            lines.append(f"Order Book Psychology:")
            lines.append(f"_{sm['orderbook_psychology']}_")
            lines.append("")

        if sm.get('whale_activity'):
            lines.append(f"Whale Activity:")
            lines.append(f"_{sm['whale_activity']}_")

        lines.append("")
        lines.append("━━━━━━━━━━━━━━━━━━━━")
        lines.append("")

    # Market Psychology
    if 'market_psychology' in analysis:
        mp = analysis['market_psychology']
        lines.append("🎭 *MARKET PSYCHOLOGY*")
        lines.append("")

        if mp.get('crowd_behavior'):
            lines.append(f"Crowd Behavior:")
            lines.append(f"_{mp['crowd_behavior']}_")
            lines.append("")

        if mp.get('sentiment'):
            lines.append(f"Sentiment:")
            lines.append(f"_{mp['sentiment']}_")
            lines.append("")

        if mp.get('potential_traps'):
            lines.append(f"Potential Traps:")
            for trap in mp['potential_traps']:
                lines.append(f"• {trap}")

        lines.append("")
        lines.append("━━━━━━━━━━━━━━━━━━━━")
        lines.append("")

    # Key Data Points
    if 'key_data' in analysis:
        kd = analysis['key_data']
        lines.append("📊 *KEY DATA POINTS*")
        lines.append("")

        if kd.get('technical'):
            lines.append(f"Technical Metrics:")
            lines.append(f"_{kd['technical']}_")
            lines.append("")

        if kd.get('derivatives'):
            lines.append(f"Derivatives Data:")
            lines.append(f"_{kd['derivatives']}_")
            lines.append("")

        if kd.get('volume_profile'):
            lines.append(f"Volume Profile:")
            lines.append(f"_{kd['volume_profile']}_")

        lines.append("")
        lines.append("━━━━━━━━━━━━━━━━━━━━")
        lines.append("")

    # Educational Insights
    if 'educational_insights' in analysis:
        ei = analysis['educational_insights']
        lines.append("💡 *EDUCATIONAL INSIGHTS*")
        lines.append("")

        if ei.get('what_this_means'):
            lines.append(f"What This Means:")
            lines.append(f"_{ei['what_this_means']}_")
            lines.append("")

        if ei.get('things_to_watch'):
            lines.append(f"Things to Watch:")
            for thing in ei['things_to_watch']:
                lines.append(f"• {thing}")
            lines.append("")

        if ei.get('market_context'):
            lines.append(f"Market Context:")
            lines.append(f"_{ei['market_context']}_")

        lines.append("")
        lines.append("━━━━━━━━━━━━━━━━━━━━")
        lines.append("")

    # Evolution Notes
    if 'evolution_notes' in analysis:
        en = analysis['evolution_notes']
        lines.append("🔄 *EVOLUTION NOTES*")
        lines.append("")

        if en.get('learning'):
            lines.append(f"What I'm Learning:")
            lines.append(f"_{en['learning']}_")
            lines.append("")

        if en.get('pattern_success'):
            lines.append(f"Pattern Success:")
            lines.append(f"_{en['pattern_success']}_")
            lines.append("")

        if en.get('improvements'):
            lines.append(f"Improving Analysis:")
            lines.append(f"_{en['improvements']}_")

        lines.append("")
        lines.append("━━━━━━━━━━━━━━━━━━━━")

    return "\n".join(lines)


def format_advanced_analysis(analysis: Dict, symbol: str = "BTCUSDT") -> str:
    """
    Format QUANTRA-3 advanced technical analysis into Telegram message

    Args:
        analysis: Advanced analysis dictionary from GeminiAnalyzer
        symbol: Trading symbol

    Returns:
        Formatted message string for Telegram
    """
    lines = [
        "📊 *QUANTRA-3 TECHNICAL ANALYSIS*",
        f"Symbol: `{symbol}`",
        "",
        "━━━━━━━━━━━━━━━━━━━━",
        ""
    ]

    # Orderbook Depth
    if 'orderbook_depth' in analysis:
        od = analysis['orderbook_depth']
        lines.append("📖 *ORDERBOOK DEPTH ANALYSIS*")
        lines.append("")

        if od.get('depth_1pct'):
            d1 = od['depth_1pct']
            lines.append(f"1% Depth (Immediate Liquidity):")
            lines.append(f"• Bids: `{d1.get('bids', 'N/A')}`")
            lines.append(f"• Asks: `{d1.get('asks', 'N/A')}`")
            lines.append(f"• Ratio: `{d1.get('ratio', 'N/A')}`")
            lines.append(f"• {d1.get('imbalance', '')}")
            lines.append("")

        if od.get('depth_2pct'):
            d2 = od['depth_2pct']
            lines.append(f"2% Depth (Short-term):")
            lines.append(f"• Bids: `{d2.get('bids', 'N/A')}`")
            lines.append(f"• Asks: `{d2.get('asks', 'N/A')}`")
            lines.append(f"• Key Zones: {d2.get('zones', 'N/A')}")
            lines.append("")

        if od.get('depth_5pct'):
            d5 = od['depth_5pct']
            lines.append(f"5% Depth (Major Liquidity):")
            lines.append(f"• Bids: `{d5.get('bids', 'N/A')}`")
            lines.append(f"• Asks: `{d5.get('asks', 'N/A')}`")
            lines.append(f"• Walls: {d5.get('major_walls', 'N/A')}")

        lines.append("")
        lines.append("━━━━━━━━━━━━━━━━━━━━")
        lines.append("")

    # CVD Analysis
    if 'cvd_analysis' in analysis:
        cvd = analysis['cvd_analysis']
        lines.append("📈 *CVD TREND ANALYSIS*")
        lines.append("")
        lines.append(f"Current Delta: _{cvd.get('current_delta', 'N/A')}_")
        lines.append(f"1H Trend: _{cvd.get('trend_1h', 'N/A')}_")
        lines.append(f"4H Trend: _{cvd.get('trend_4h', 'N/A')}_")
        lines.append(f"24H Trend: _{cvd.get('trend_24h', 'N/A')}_")
        if cvd.get('divergences'):
            lines.append(f"Divergences: _{cvd['divergences']}_")
        lines.append("")
        lines.append("━━━━━━━━━━━━━━━━━━━━")
        lines.append("")

    # Funding History
    if 'funding_history' in analysis:
        fh = analysis['funding_history']
        lines.append("💰 *FUNDING RATE HISTORY*")
        lines.append("")
        lines.append(f"Current: `{fh.get('current', 'N/A')}%`")
        lines.append(f"8H Trend: _{fh.get('trend_8h', 'N/A')}_")
        lines.append(f"Momentum: _{fh.get('momentum', 'N/A')}_")
        lines.append(f"Context: _{fh.get('extremes_context', 'N/A')}_")
        if fh.get('prediction'):
            lines.append(f"Prediction: _{fh['prediction']}_")
        lines.append("")
        lines.append("━━━━━━━━━━━━━━━━━━━━")
        lines.append("")

    # OI Delta
    if 'oi_delta' in analysis:
        oi = analysis['oi_delta']
        lines.append("📊 *OPEN INTEREST DELTA*")
        lines.append("")
        lines.append(f"1H: `{oi.get('delta_1h', 'N/A')}`")
        lines.append(f"4H: `{oi.get('delta_4h', 'N/A')}`")
        lines.append(f"24H: `{oi.get('delta_24h', 'N/A')}`")
        lines.append(f"Correlation: _{oi.get('correlation', 'N/A')}_")
        lines.append(f"_{oi.get('interpretation', '')}_")
        lines.append("")
        lines.append("━━━━━━━━━━━━━━━━━━━━")
        lines.append("")

    # Confluence Score
    if 'confluence_score' in analysis:
        cs = analysis['confluence_score']
        lines.append("🎯 *MULTI-TIMEFRAME CONFLUENCE*")
        lines.append("")
        lines.append(f"1H Score: `{cs.get('timeframe_1h', 'N/A')}/100`")
        lines.append(f"4H Score: `{cs.get('timeframe_4h', 'N/A')}/100`")
        lines.append(f"8H Score: `{cs.get('timeframe_8h', 'N/A')}/100`")
        lines.append(f"Overall: `{cs.get('overall', 'N/A')}/100`")
        if cs.get('analysis'):
            lines.append(f"_{cs['analysis']}_")
        lines.append("")
        lines.append("━━━━━━━━━━━━━━━━━━━━")
        lines.append("")

    # Risk/Reward
    if 'risk_reward' in analysis:
        rr = analysis['risk_reward']
        lines.append("⚖️ *RISK/REWARD VALIDATION*")
        lines.append("")

        if rr.get('support_levels'):
            lines.append(f"Support Levels:")
            for level in rr['support_levels']:
                lines.append(f"• `{level}`")
            lines.append("")

        if rr.get('resistance_levels'):
            lines.append(f"Resistance Levels:")
            for level in rr['resistance_levels']:
                lines.append(f"• `{level}`")
            lines.append("")

        if rr.get('high_probability_zones'):
            lines.append(f"High Probability: _{rr['high_probability_zones']}_")
            lines.append("")

        if rr.get('invalidation'):
            lines.append(f"Invalidation: _{rr['invalidation']}_")
            lines.append("")

        if rr.get('position_sizing'):
            lines.append(f"Position Sizing: _{rr['position_sizing']}_")

        lines.append("")
        lines.append("━━━━━━━━━━━━━━━━━━━━")

    # Metadata
    if '_metadata' in analysis:
        meta = analysis['_metadata']
        lines.append("")
        lines.append(f"🤖 Model: `{meta.get('model', 'N/A')}`")

    return "\n".join(lines)
