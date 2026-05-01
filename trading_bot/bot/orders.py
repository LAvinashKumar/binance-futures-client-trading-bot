"""
Order placement functions for Binance USDT-M Futures Testnet.
Supports MARKET and LIMIT orders for BUY and SELL sides.
"""

from binance.um_futures import UMFutures
from binance.error import ClientError

from bot.logging_config import get_logger

logger = get_logger(__name__)


def place_order(client: UMFutures, params: dict) -> dict:
    """
    Place a futures order using the provided validated parameters.

    Args:
        client: Authenticated UMFutures client instance.
        params: Validated order parameters produced by validators.validate_inputs().
                Expected keys: symbol, side, type, quantity.
                Optional keys: price, timeInForce (for LIMIT orders).

    Returns:
        Raw response dict from the Binance API.

    Raises:
        ClientError: On Binance API-level errors (e.g. insufficient balance,
                     invalid symbol, bad precision).
        ConnectionError: On network / connectivity issues.
        RuntimeError: On unexpected errors during order placement.
    """
    order_type = params["type"]
    symbol = params["symbol"]

    # Build the request payload
    payload: dict = {
        "symbol": symbol,
        "side": params["side"],
        "type": order_type,
        "quantity": params["quantity"],
    }

    if order_type == "LIMIT":
        payload["price"] = params["price"]
        payload["timeInForce"] = params.get("timeInForce", "GTC")

    logger.info("Placing %s %s order | payload: %s", order_type, symbol, payload)

    try:
        response = client.new_order(**payload)
        logger.info("Order response for %s: %s", symbol, response)
        return response

    except ClientError as exc:
        logger.error(
            "Binance API error placing order for %s: status=%s, code=%s, msg=%s",
            symbol,
            exc.status_code,
            exc.error_code,
            exc.error_message,
        )
        raise

    except Exception as exc:
        logger.error("Unexpected error placing order for %s: %s", symbol, exc)
        raise RuntimeError(f"Unexpected error: {exc}") from exc


def place_market_order(client: UMFutures, symbol: str, side: str, quantity: float) -> dict:
    """
    Convenience wrapper to place a MARKET order.

    Args:
        client:   Authenticated UMFutures client.
        symbol:   Trading pair (e.g. 'BTCUSDT').
        side:     'BUY' or 'SELL'.
        quantity: Order quantity.

    Returns:
        Raw API response dict.
    """
    params = {
        "symbol": symbol,
        "side": side,
        "type": "MARKET",
        "quantity": quantity,
    }
    return place_order(client, params)


def place_limit_order(
    client: UMFutures,
    symbol: str,
    side: str,
    quantity: float,
    price: float,
    time_in_force: str = "GTC",
) -> dict:
    """
    Convenience wrapper to place a LIMIT order.

    Args:
        client:        Authenticated UMFutures client.
        symbol:        Trading pair (e.g. 'BTCUSDT').
        side:          'BUY' or 'SELL'.
        quantity:      Order quantity.
        price:         Limit price.
        time_in_force: Time-in-force policy (default: GTC).

    Returns:
        Raw API response dict.
    """
    params = {
        "symbol": symbol,
        "side": side,
        "type": "LIMIT",
        "quantity": quantity,
        "price": price,
        "timeInForce": time_in_force,
    }
    return place_order(client, params)
