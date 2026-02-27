# AI Trading Bot

An AI-powered trading bot for stocks and options, designed to be deployed on Vercel.

## Features
- **AI Analysis**: Uses Qwen 3 Max via OpenRouter to analyze market trends, technical indicators, and news sentiment.
- **Market Data**: Integrates with Robinhood (via `robin_stocks`) for real-time-ish data.
- **Trading Modes**: Supports both Intraday/Swing and Long-term investment modes.
- **Sandbox Mode**: Executes 'Dry Run' trades in a local SQLite database to test performance without risk.
- **Risk Management**: Configurable portfolio percentage baseline for position sizing.
- **Dashboard**: React-based UI for monitoring portfolio balance and trade history.
- **Notifications**: Telegram integration for instant trade alerts.

## Setup

### Prerequisites
- [Vercel CLI](https://vercel.com/docs/cli)
- Python 3.12+
- Node.js 18+
- OpenRouter API Key
- Telegram Bot Token
- Robinhood Account (for data fetching)

### Environment Variables
Copy `.env.example` to `.env` and fill in your credentials:
- `OPENROUTER_API_KEY`: Your OpenRouter API key.
- `AI_MODEL_STRING`: (Optional) Defaults to `qwen/qwen3-max`.
- `ROBINHOOD_USERNAME`: Your Robinhood email.
- `ROBINHOOD_PASSWORD`: Your Robinhood password.
- `TELEGRAM_BOT_TOKEN`: Token from @BotFather.
- `TELEGRAM_CHAT_ID`: Your chat ID for notifications.

### Local Development

1. **Backend**:
   ```bash
   pip install -r requirements.txt
   export PYTHONPATH=$PYTHONPATH:.
   python3 api/index.py
   ```

2. **Frontend**:
   ```bash
   npm install
   npm start
   ```

## Deployment
This project is configured for one-click deployment to Vercel. Simply push to your repository and configure the environment variables in the Vercel dashboard.

## Disclaimer
This is a proof-of-concept trading bot. Trading stocks and options involves significant risk. Use this bot at your own discretion. The developers are not responsible for any financial losses.
