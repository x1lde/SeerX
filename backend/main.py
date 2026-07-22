import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client

load_dotenv()

app = FastAPI(title="SeerX")

app.add_middleware(
    CORSMiddleware, 
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(","),
    allow_methods=["GET"],
    allow_headers=["*"],
)

supabase = create_client(
    supabase_url=os.getenv("SUPABASE_URL"),
    supabase_key=os.getenv("SUPABASE_KEY")
)

def get_trading_cient():
    from alpaca.trading.client import TradingClient
    return TradingClient(
        os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_SECRET_KEY")
    )

@app.get("/health")
def health():
    return {'status': 'ok'}

@app.get("/predictions")
def get_predictions(limit: int=100):
    result = (
        supabase.table("predictions")
        .select("*")
        .order("date", desc=True)
        .limit(limit)
        .execute()
    )
    return result.data

@app.get("/trades")
def get_trades(limit: int=100):
    result = (
        supabase.table("trades")
        .select("*")
        .order("date", desc=True)
        .limit(limit)
        .execute()
    )
    return result.data

@app.get("/portfolio")
def get_portfolio():
    try:
        client = get_trading_cient()
        account = client.get_account()
        positions = client.get_all_positions()
    except Exception as e:
        print(f"DEBUG CRASH TRACE: {e}")
        raise HTTPException(status_code=502, detail=f"Alpaca error: {e}")

    return{
        "equity": float(account.equity),
        "cash": float(account.cash),
        "buying_power": float(account.buying_power),
        "positions": [
            {
                "symbol": p.symbol,
                "qty": float(p.qty),
                "market_value": float(p.market_value),
                "unrealized_pl": float(p.unrealized_pl),
            }
            for p in positions
        ]
    }