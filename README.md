# Binance Futures Testnet Trading Bot

## Overview

A Python-based command-line trading bot for Binance Futures Testnet that enables users to place market and limit orders on USDT-M Perpetual Futures. The bot handles HMAC-SHA256 request signing, input validation, and comprehensive logging of all API interactions.

## Setup

1. **Clone the repo**
   ```bash
   git clone <repo-url>
   cd trading_bot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv && venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file in root directory**
   ```
   API_KEY=your_testnet_api_key
   API_SECRET=your_testnet_api_secret
   ```
   
   **Get API keys from:** https://testnet.binancefuture.com
   - Go to Account → API Management
   - Create new API key (testnet environment)
   - Note: Keys must be from testnet, not your main Binance account

## How to Run

### Market Order
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.002
python cli.py --symbol BTCUSDT --side SELL --type MARKET --quantity 0.002
```

### Limit Order
```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.002 --price 60000
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.002 --price 70000
```

## Project Structure

```
trading_bot/
├── cli.py                    Main entry point for CLI with argument parsing
├── requirements.txt          Python dependencies (requests, python-dotenv)
├── .env                      API credentials (API_KEY, API_SECRET)
├── .gitignore               Git ignore patterns
├── README.md                This file
│
├── bot/                      Core trading bot module
│   ├── __init__.py          Module initialization
│   ├── client.py            BinanceClient - API client with HMAC-SHA256 signing
│   ├── orders.py            Order placement functions (market/limit)
│   ├── validators.py        Input validation for symbols, quantities, prices
│   └── logging_config.py    Logging configuration and setup
│
└── logs/                     Log files
    └── trading_bot.log      All API requests, responses, and errors
```

## Assumptions

- **Testnet Only:** Uses Binance Futures Testnet (USDT-M), not real trading accounts
- **Minimum Order Notional:** Order value (quantity × price) must exceed $100
- **Precision:** 
  - BTCUSDT quantity: 3 decimal places (e.g., 0.001)
  - BTCUSDT price: 2 decimal places (e.g., 50000.00)
- **API Keys:** Must be generated from testnet.binancefuture.com, not the main Binance platform
- **Log Location:** Log file automatically created at `logs/trading_bot.log`
- **Time Synchronization:** System clock must be synchronized; Binance rejects requests with timestamp skew > 5000ms

## Logging

All API requests, responses, and errors are logged to `logs/trading_bot.log`:

- **INFO:** Order placement, successful API responses, order confirmations
- **ERROR:** Failed requests, validation errors, API errors with error codes
- **Request Details:** Symbol, side, type, quantity, price, timestamp, and signed request body

Example log entries:
```
2026-05-01 12:01:33 - trading_bot - INFO - Placing order: BTCUSDT BUY MARKET 0.002
2026-05-01 12:01:33 - trading_bot - INFO - Sending order request to https://testnet.binancefuture.com/fapi/v1/order
2026-05-01 12:01:34 - trading_bot - INFO - Order placed successfully. Order ID: 13095548422
```
