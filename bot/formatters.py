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

*COMMANDS*

/q1 BTC - Analyze Bitcoin
/q1 ETH - Analyze Ethereum
/q1 SYMBOL - Analyze any symbol

━━━━━━━━━━━━━━━━━━━━

*FEATURES*
🧠 Gemini AI market analysis
📊 Multi-timeframe signals (8H/4H/1H)
💰 Entry, stop, and target levels
⚖️ Long/short positioning analysis
📈 Open interest & funding rates
🎯 High-conviction trade setups

━━━━━━━━━━━━━━━━━━━━

*HOW IT WORKS*
1. Send /q1 BTC
2. AI analyzes market data
3. Get trading signal with levels
4. Execute or wait for better setup

━━━━━━━━━━━━━━━━━━━━

Ready to receive alpha! 🎯

Type /q1 BTC to get started."""


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
/q1 <SYMBOL> - Get AI analysis

━━━━━━━━━━━━━━━━━━━━

*EXAMPLES*

/q1 BTC
/q1 BTCUSDT
/q1 ETH
/q1 ETHUSDT

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
