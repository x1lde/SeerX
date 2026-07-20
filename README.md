# SeerX

A cloud-integrated app that predicts stock/crypto price movement and paper-trades on those predictions using Alpaca's API

## Status
Phase 1: Setup

## What's ahead?
1. **Setup** - repository, accounts, API keys
2. **Data pipeline** - fetch & store market data
3. **Baseline model** - train a simple prediction model
4. **Trading engine** - predictions trigger paper trades
5. **Dashboard & polish** - frontend, README, monitoring

## Setup
1. Clone this repository
2. 'python -m venv venv && source venv/bin/activate'
3. `pip install -r requirements.txt`
4. `cp .env.example .env` and fill in your API keys
5. `python src/test_connections.py`