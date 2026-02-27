import os
from sqlmodel import Session, select
from .trade import Trade, Portfolio
from datetime import datetime

class TradingEngine:
    def __init__(self, mode="sandbox"):
        self.mode = mode
        self.fee_rate = 0.0001
        self.slippage_estimate = 0.0005

    def get_portfolio_balance(self, session: Session):
        statement = select(Portfolio).where(Portfolio.is_sandbox == (self.mode == "sandbox"))
        portfolio = session.exec(statement).first()
        if not portfolio:
            portfolio = Portfolio(balance=100000.0, is_sandbox=True)
            session.add(portfolio)
            session.commit()
            session.refresh(portfolio)
        return portfolio

    def calculate_position_size(self, balance, confidence):
        baseline = float(os.getenv("PORTFOLIO_PERCENTAGE_BASELINE", 0.05))
        multiplier = 0.5 + confidence
        return balance * baseline * multiplier

    def execute_trade(self, session: Session, recommendation, current_price, symbol, trading_mode):
        portfolio = self.get_portfolio_balance(session)

        if recommendation["recommendation"] == "BUY" and recommendation["confidence_threshold"] > 0.7:
            position_value = self.calculate_position_size(portfolio.balance, recommendation["confidence_threshold"])
            effective_price = current_price * (1 + self.slippage_estimate)
            quantity = position_value / effective_price
            cost = (quantity * effective_price) * (1 + self.fee_rate)

            if portfolio.balance >= cost:
                trade = Trade(
                    symbol=symbol,
                    action=recommendation["suggested_action"],
                    price=effective_price,
                    quantity=quantity,
                    mode=trading_mode,
                    confidence=recommendation["confidence_threshold"],
                    reasoning=recommendation["reasoning"],
                    is_sandbox=(self.mode == "sandbox")
                )
                portfolio.balance -= cost
                session.add(trade)
                session.add(portfolio)
                session.commit()
                return f"Executed BUY for {symbol} at {effective_price}"

        elif recommendation["recommendation"] == "SELL":
            statement = select(Trade).where(
                Trade.symbol == symbol,
                Trade.status == "OPEN",
                Trade.mode == trading_mode,
                Trade.is_sandbox == (self.mode == "sandbox")
            )
            open_trades = session.exec(statement).all()
            for trade in open_trades:
                effective_exit_price = current_price * (1 - self.slippage_estimate)
                revenue = (trade.quantity * effective_exit_price) * (1 - self.fee_rate)
                trade.status = "CLOSED"
                trade.exit_price = effective_exit_price
                trade.pnl = revenue - (trade.quantity * trade.price)
                portfolio.balance += revenue
                session.add(trade)

            if open_trades:
                session.add(portfolio)
                session.commit()
                return f"Executed SELL for {symbol} at {current_price}"
        return "No action taken"
