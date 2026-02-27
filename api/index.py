from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from .app.models.trade import get_session, create_db_and_tables, Trade, Portfolio
from .app.services.market_data import MarketDataService
from .app.services.technical_analysis import TechnicalAnalysisService
from .app.services.news_gatherer import NewsGathererService
from .app.services.ai_engine import AIEngineService
from .app.services.trading_engine import TradingEngine
from .app.services.telegram_service import TelegramService

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

market_data_service = MarketDataService()
ta_service = TechnicalAnalysisService()
news_service = NewsGathererService()
ai_engine = AIEngineService()
telegram_service = TelegramService()

@app.get("/api/portfolio")
def get_portfolio(session: Session = Depends(get_session)):
    statement = select(Portfolio)
    return session.exec(statement).first()

@app.get("/api/trades")
def get_trades(session: Session = Depends(get_session)):
    statement = select(Trade).order_by(Trade.timestamp.desc())
    return session.exec(statement).all()

async def run_analysis_and_trade(symbol: str, mode: str, session: Session):
    hist_data = market_data_service.get_historical_data(symbol)
    if not hist_data: return
    df = ta_service.calculate_indicators(hist_data)
    signals = ta_service.get_latest_signals(df)
    news = await news_service.get_company_news(symbol)
    recommendation = await ai_engine.get_trading_recommendation(symbol, signals, news, mode)
    trading_engine = TradingEngine(mode="sandbox")
    current_price = signals['price']
    result = trading_engine.execute_trade(session, recommendation, current_price, symbol, mode)
    if "Executed" in result:
        await telegram_service.send_message(f"Trade Executed for {symbol}: {result}")

@app.post("/api/analyze/{symbol}")
async def analyze_symbol(symbol: str, mode: str = "intraday", session: Session = Depends(get_session)):
    await run_analysis_and_trade(symbol, mode, session)
    return {"status": "Analysis triggered"}
