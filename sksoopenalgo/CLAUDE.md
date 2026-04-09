# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## System Constraints (always enforced)

- **No live orders** — all broker API calls must be in `paper`, `signal_log`, or `dry_run` mode
- **Max drawdown < 10%** of capital per strategy per session
- **Position sizing** capped at 1% risk per trade (ATR-based)
- **Fixed slippage + brokerage** included in all P&L calculations (0.1% round-trip)
- **Kill switch** halts a session when daily P&L < `DAILY_LOSS_LIMIT` (default −₹15,000)
- **Backtest gate** before any promotion to paper: PF ≥ 1.5, Sharpe ≥ 2.0, MaxDD ≤ 20%, trades ≥ 50

## Runtime Environment

```bash
# Always use this venv
/Users/mac/sksoopenalgo/openalgo-official/.venv/bin/python3

# All work happens in
cd /Users/mac/sksoopenalgo/
```

Key packages: `pandas`, `pandas_ta`, `vectorbt`, `yfinance`, `httpx`, `apscheduler`, `python-dotenv`

## Daily Workflow

```bash
# 1. Refresh Dhan token (from Dhan portal → Access Token)
#    Update in .env:
sed -i '' "s|DHAN_ACCESS_TOKEN=.*|DHAN_ACCESS_TOKEN='eyJ...'|" .env

# 2. Health check
python3 dhan_paper_launcher.py --check-health

# 3. Start paper trading (APScheduler continuous mode)
nohup python3 dhan_paper_launcher.py --scheduled >> logs/paper_trades/paper_$(date +%F).log 2>&1 &

# 4. Monitor
tail -f logs/paper_trades/paper_$(date +%F).log

# 5. EOD: check session summary
cat logs/paper_trades/summary_$(date +%F).json
```

## Architecture

### Broker Layer (zero-OpenAlgo)

OpenAlgo is **disabled** — static IP issues. All broker access goes through:

- **`dhan_direct.py`** — `DhanDirect(mode="paper"|"log_only")` + `DhanHistoricalData`. Auto-registers the current public IP via Dhan `/v2/ip` at startup. Paper mode simulates fills locally using real LTP from Dhan API.
- **`broker_base.py`** — Abstract `BrokerBase` interface that `DhanDirect` implements. New brokers implement this interface.

```python
from dhan_direct import DhanDirect, DhanHistoricalData
client = DhanDirect(mode="paper")
client.startup()                          # auto IP registration
client.place_order(symbol, exchange, ...)
df = hist.get_candles(symbol, interval="1h", days=30)
```

### State Layer

- **`trade_state.py`** — `TradeStateManager`: persists orders, positions, signals, P&L to `vaults/trading-brain/state/orders/<date>.json` and auto-writes Obsidian markdown trade logs. Every launcher uses this.

### Backtest Layer

- **`backtest_engine.py`** — `run_backtest(df, signals, capital, ...)` — vectorized engine with ATR-based position sizing, slippage, and kill switch. Returns `(stats_dict, trade_log_df)`.
- **`backtest_vbt.py`** — CLI runner using vectorbt. `python3 backtest_vbt.py --all --days 365` runs all 10 registered strategies. Results auto-saved to `vaults/trading-brain/backtests/`.
- **`institutional_strategies.py`** — Pure signal functions (no broker calls). Each function returns `pd.Series` of `{-1, 0, 1}` signals. Used by both the backtest runner and live launchers.

### Strategy Signal Modules

| Module | Content |
|---|---|
| `institutional_strategies.py` | `nifty_ema_adx`, `banknifty_trend`, `silver_donchian`, `gold_ichimoku`, `crude_keltner`, `nifty_pivot_rsi`, `banknifty_rsi_mr` — pure signal functions |
| `equity_orb.py` | `ORBRunner` — Opening Range Breakout for equities (RELIANCE/HDFC/TCS). ORB window 09:15–09:45 IST. |
| `options_strategies.py` | `Nifty0DTERunner`, `BankNiftyICRunner` — options wrappers (signal_log mode; ATM strike computed from spot) |

### Orchestration

- **`regime_detector.py`** — `RegimeDetector().run()` returns `Regime` enum (TRENDING/MEAN_REVERTING/CHOPPY/UNKNOWN) from VIX + gap + ADX. Run at 09:10 IST before strategy selection.
- **`portfolio_manager.py`** — `PortfolioManager(capital=20_00_000)`. Call `request_position()` before entry; `open()` / `close()` to track margin. Enforces per-strategy limits and overall kill switch.
- **`strategy_suite_launcher_v2.py`** — Regime-aware launcher: maps regime → enabled strategy groups → iterates runners with portfolio gating.

### Cherry-pick paper launcher

**Canonical entrypoint**: `dhan_paper_launcher.py` (TOP-10 stack, no OpenAlgo). Prefer this in docs, cron, and health checks.

`dhan_paper_launcher_YYYY_MM_DD.py` may exist as a thin **shim** for old bookmarks; implementation lives in `dhan_paper_launcher.py`.

- `run_scheduled_mode()` — APScheduler continuous mode (recommended)
- `run_once()` — single-shot eval of current bar
- `SessionState` wraps `TradeStateManager`; logs under `logs/paper_trades/`

### Obsidian Vault

`vaults/trading-brain/` is the knowledge layer:
- `strategies/` — one `.md` per strategy with params, backtest metrics, edge thesis
- `trades/` — auto-generated daily logs by `trade_state.py`
- `backtests/` — backtest summaries from `backtest_vbt.py`
- `state/orders/` — machine-readable JSON per session

## Dhan API Notes

- Exchange segments: `NSE_EQ`, `NSE_FNO`, `MCX_COMM`, `BSE_EQ`, `BSE_FNO`, `IDX_I` (index quotes only)
- Key security IDs: NIFTY=13 (IDX_I), BANKNIFTY=25 (IDX_I), SILVERMIC=466029 (MCX_COMM)
- `get_ltp()` takes Dhan numeric `security_ids`, not ticker symbols
- Token expires daily — refresh from Dhan portal and update `.env` each morning

## Backtest Promotion Gates

| Gate | Threshold |
|---|---|
| Profit Factor | ≥ 1.5 |
| Sharpe Ratio | ≥ 2.0 |
| Win Rate | ≥ 45% |
| Max Drawdown | ≤ 20% |
| Min Trades | ≥ 50 |

Run with 365-day lookback for meaningful sample size. Note: yfinance caps 15m data at ~60 days — use Dhan historical API for sub-hourly strategies.

## Running Tests / Backtests

```bash
# Syntax check any module
python3 -m py_compile <file>.py

# Full backtest suite (365 days, all strategies)
python3 backtest_vbt.py --all --days 365

# Single strategy backtest
python3 backtest_vbt.py --strategy silver_donchian --days 365

# Backtest a specific strategy module function
python3 -c "
from institutional_strategies import silver_donchian, fetch_yfinance
df = fetch_yfinance('SI=F', '1h', 365)
signals = silver_donchian(df)
print(signals.value_counts())
"
```

## Key Patterns

**Adding a new strategy runner** (to a daily launcher):
1. Add config dict entry to `STRATEGIES`
2. Create a runner class with `fetch_data()`, `compute_signal()`, `_qty()`, `run_bar()`, `square_off()`
3. All exits compare close to ATR-based SL/TP computed from `entry_price`
4. P&L is tracked via `_session.update_pnl(sign * (close - entry_price) * qty * lot_multiplier, sid)`
5. Add to scheduler in `run_scheduled_mode()`

**Signal convention** in `institutional_strategies.py`: functions return `pd.Series` of `{1: LONG, -1: SHORT, 0: FLAT}` with `shift(1)` applied (no look-ahead).
