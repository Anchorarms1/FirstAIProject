from sqlmodel import SQLModel, Field, create_engine, Session, select
from datetime import datetime
from typing import Optional

class Trade(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str
    action: str
    price: float
    quantity: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    mode: str
    confidence: float
    reasoning: str
    status: str = "OPEN"
    exit_price: Optional[float] = None
    pnl: Optional[float] = None
    is_sandbox: bool = True

class Portfolio(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    balance: float
    is_sandbox: bool = True
    last_updated: datetime = Field(default_factory=datetime.utcnow)

sqlite_url = "sqlite:///database.db"
engine = create_engine(sqlite_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
