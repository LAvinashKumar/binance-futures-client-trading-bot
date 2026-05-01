# Binance Futures Testnet — CLI Trading Bot

A modular Python CLI bot for placing MARKET and LIMIT orders on the
Binance USDT-M Futures Testnet.

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance client setup
│   ├── orders.py          # Order placement functions
│   ├── validators.py      # Input validation
│   └── logging_config.py  # Logging setup
├── logs/                  # Auto-created on first run
│   ├── trading_bot.log
│   ├── requests.log
│   └── errors.log
├── cli.py                 # CLI entry point
├── .env                   # API credentials (never commit this)
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone / download the project

```bash
git clone <repo-url>
cd trading_bot
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API credentials

Edit `.env` and add your Binance Futures **Testnet** keys.
Get them from: https://testnet.binancefuture.com

```env
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
```

> ⚠️ Never commit `.env` to version control. Add it to `.gitignore`.

---

## How to Run

```
python cli.py --symbol <SYMBOL> --side <BUY|SELL> --type <MARKET|LIMIT> \
              --quantity <QTY> [--price <PRICE>]
```

| Argument     | Required          | Description                        |
|--------------|-------------------|------------------------------------|
| `--symbol`   | Yes               | Trading pair, e.g. `BTCUSDT`       |
| `--side`     | Yes               | `BUY` or `SELL`                    |
| `--type`     | Yes               | `MARKET` or `LIMIT`                |
| `--quantity` | Yes               | Order quantity, e.g. `0.01`        |
| `--price`    | LIMIT orders only | Limit price, e.g. `65000`          |

---

## Example Commands

### Market BUY

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

**Output:**

```
========================================
         Order Summary
========================================
  Symbol   : BTCUSDT
  Side     : BUY
  Type     : MARKET
  Quantity : 0.01
========================================

Response:
  Order ID     : 123456
  Status       : FILLED
  Executed Qty : 0.01
  Avg Price    : 65000.00

SUCCESS ✅
```

---

### Limit SELL

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 70000
```

**Output:**

```
========================================
         Order Summary
========================================
  Symbol   : BTCUSDT
  Side     : SELL
  Type     : LIMIT
  Quantity : 0.01
  Price    : 70000.0
========================================

Response:
  Order ID     : 789012
  Status       : NEW
  Executed Qty : 0
  Avg Price    : 0

SUCCESS ✅
```

---

### Market SELL on ETHUSDT

```bash
python cli.py --symbol ETHUSDT --side SELL --type MARKET --quantity 0.1
```

---

## Log Files

Logs are written to the `logs/` directory (auto-created on first run).

| File               | Content                                  |
|--------------------|------------------------------------------|
| `trading_bot.log`  | All events (DEBUG and above)             |
| `requests.log`     | Order requests and responses (INFO+)     |
| `errors.log`       | Errors only (ERROR+)                     |

All log files rotate at 5 MB with up to 3 backups.

---

## Error Handling

| Scenario                  | Behaviour                                      |
|---------------------------|------------------------------------------------|
| Missing API keys          | Clear error message, exits with code 1         |
| Invalid symbol/side/type  | Validation error printed, exits with code 1    |
| Negative / zero quantity  | Validation error printed, exits with code 1    |
| LIMIT order without price | Validation error printed, exits with code 1    |
| Binance API error         | API error code and message printed and logged  |
| Network / connection error| Network error printed and logged               |

---

## Dependencies

| Package                      | Version  | Purpose                        |
|------------------------------|----------|--------------------------------|
| `binance-futures-connector`  | 4.1.0    | Official Binance Futures SDK   |
| `python-dotenv`              | 1.0.1    | Load `.env` credentials        |

---

## Security Notes

- API keys are loaded from `.env` — never hard-coded.
- Add `.env` to `.gitignore` before committing.
- This bot targets the **Testnet** only. To use on mainnet, remove the
  `base_url` override in `bot/client.py` and use mainnet keys.


## Features

- Place MARKET and LIMIT orders on Binance Futures Testnet
- Supports both BUY and SELL sides
- CLI-based interface using argparse
- Structured modular code (client, orders, validators, logging)
- Comprehensive logging (requests, responses, errors)
- Robust input validation and error handling

## Design Decisions

- Separated API logic (client.py) from business logic (orders.py) for modularity
- Used validation layer (validators.py) to ensure clean CLI inputs
- Implemented structured logging with multiple log files for clarity
- CLI chosen for simplicity and focus on backend logic rather than UI
- Environment variables used for secure API key management