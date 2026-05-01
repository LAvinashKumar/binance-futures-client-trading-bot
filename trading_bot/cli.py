"""
CLI entry point for the Binance Futures Testnet trading bot.

Usage examples:
    # Market BUY
    python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01

    # Limit SELL
    python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 70000

    # Market SELL on ETHUSDT
    python cli.py --symbol ETHUSDT --side SELL --type MARKET --quantity 0.1
"""

import argparse
import sys

from binance.error import ClientError

from bot.client import get_client
from bot.orders import place_order
from bot.validators import validate_inputs
from bot.logging_config import get_logger

logger = get_logger(__name__)


# ──────────────────────────────────────────────────────────────────────────────
# Output helpers
# ──────────────────────────────────────────────────────────────────────────────

def print_order_summary(params: dict) -> None:
    """Print a formatted summary of the order parameters before submission."""
    print("\n" + "=" * 40)
    print("         Order Summary")
    print("=" * 40)
    print(f"  Symbol   : {params['symbol']}")
    print(f"  Side     : {params['side']}")
    print(f"  Type     : {params['type']}")
    print(f"  Quantity : {params['quantity']}")
    if "price" in params:
        print(f"  Price    : {params['price']}")
    print("=" * 40)


def print_order_response(response: dict) -> None:
    """Print a formatted summary of the API response."""
    order_id    = response.get("orderId", "N/A")
    status      = response.get("status", "N/A")
    exec_qty    = response.get("executedQty", "N/A")
    avg_price   = response.get("avgPrice", "N/A")

    print("\nResponse:")
    print(f"  Order ID     : {order_id}")
    print(f"  Status       : {status}")
    print(f"  Executed Qty : {exec_qty}")
    print(f"  Avg Price    : {avg_price}")
    print()


def print_success() -> None:
    print("SUCCESS ✅\n")


def print_failure(message: str) -> None:
    print(f"\nFAILED ❌  {message}\n")


# ──────────────────────────────────────────────────────────────────────────────
# Argument parsing
# ──────────────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    """Build and return the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Binance USDT-M Futures Testnet — CLI trading bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--symbol", "-s",
        required=True,
        help="Trading pair symbol, e.g. BTCUSDT",
    )
    parser.add_argument(
        "--side",
        required=True,
        choices=["BUY", "SELL", "buy", "sell"],
        help="Order side: BUY or SELL",
    )
    parser.add_argument(
        "--type", "-t",
        dest="order_type",
        required=True,
        choices=["MARKET", "LIMIT", "market", "limit"],
        help="Order type: MARKET or LIMIT",
    )
    parser.add_argument(
        "--quantity", "-q",
        required=True,
        help="Order quantity (e.g. 0.01)",
    )
    parser.add_argument(
        "--price", "-p",
        default=None,
        help="Limit price — required for LIMIT orders",
    )
    return parser


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:
    """Parse CLI arguments, validate inputs, place order, and display results."""
    parser = build_parser()
    args = parser.parse_args()

    # ── Validate ──────────────────────────────────────────────────────────────
    try:
        params = validate_inputs(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )
    except ValueError as exc:
        logger.error("Validation error: %s", exc)
        print_failure(str(exc))
        sys.exit(1)

    print_order_summary(params)

    # ── Connect ───────────────────────────────────────────────────────────────
    try:
        client = get_client()
    except EnvironmentError as exc:
        logger.error("Client setup error: %s", exc)
        print_failure(str(exc))
        sys.exit(1)

    # ── Place order ───────────────────────────────────────────────────────────
    try:
        response = place_order(client, params)
    except ClientError as exc:
        msg = f"Binance API error [{exc.error_code}]: {exc.error_message}"
        logger.error(msg)
        print_failure(msg)
        sys.exit(1)
    except ConnectionError as exc:
        msg = f"Network error: {exc}"
        logger.error(msg)
        print_failure(msg)
        sys.exit(1)
    except RuntimeError as exc:
        logger.error("Runtime error: %s", exc)
        print_failure(str(exc))
        sys.exit(1)

    # ── Display result ────────────────────────────────────────────────────────
    print_order_response(response)
    print_success()
    logger.info("Order placed successfully. Order ID: %s", response.get("orderId"))


if __name__ == "__main__":
    main()
