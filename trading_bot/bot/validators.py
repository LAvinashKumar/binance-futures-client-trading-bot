"""
Input validation for CLI trading parameters.
All validators raise ValueError with a descriptive message on failure.
"""

from bot.logging_config import get_logger

logger = get_logger(__name__)

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


def validate_symbol(symbol: str) -> str:
    """
    Validate and normalise a trading symbol.

    Args:
        symbol: Trading pair string, e.g. 'btcusdt' or 'BTCUSDT'.

    Returns:
        Upper-cased symbol string.

    Raises:
        ValueError: If symbol is empty or contains invalid characters.
    """
    symbol = symbol.strip().upper()
    if not symbol:
        raise ValueError("Symbol cannot be empty.")
    if not symbol.isalnum():
        raise ValueError(
            f"Invalid symbol '{symbol}'. Use alphanumeric characters only (e.g. BTCUSDT)."
        )
    logger.debug("Symbol validated: %s", symbol)
    return symbol


def validate_side(side: str) -> str:
    """
    Validate order side.

    Args:
        side: 'BUY' or 'SELL' (case-insensitive).

    Returns:
        Upper-cased side string.

    Raises:
        ValueError: If side is not BUY or SELL.
    """
    side = side.strip().upper()
    if side not in VALID_SIDES:
        raise ValueError(
            f"Invalid side '{side}'. Must be one of: {', '.join(sorted(VALID_SIDES))}."
        )
    logger.debug("Side validated: %s", side)
    return side


def validate_order_type(order_type: str) -> str:
    """
    Validate order type.

    Args:
        order_type: 'MARKET' or 'LIMIT' (case-insensitive).

    Returns:
        Upper-cased order type string.

    Raises:
        ValueError: If order type is not MARKET or LIMIT.
    """
    order_type = order_type.strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        raise ValueError(
            f"Invalid order type '{order_type}'. "
            f"Must be one of: {', '.join(sorted(VALID_ORDER_TYPES))}."
        )
    logger.debug("Order type validated: %s", order_type)
    return order_type


def validate_quantity(quantity: str) -> float:
    """
    Validate order quantity.

    Args:
        quantity: Quantity as a string or numeric value.

    Returns:
        Quantity as a positive float.

    Raises:
        ValueError: If quantity is not a positive number.
    """
    try:
        qty = float(quantity)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid quantity '{quantity}'. Must be a numeric value.")

    if qty <= 0:
        raise ValueError(f"Quantity must be greater than zero, got {qty}.")

    logger.debug("Quantity validated: %s", qty)
    return qty


def validate_price(price: str) -> float:
    """
    Validate limit order price.

    Args:
        price: Price as a string or numeric value.

    Returns:
        Price as a positive float.

    Raises:
        ValueError: If price is not a positive number.
    """
    try:
        p = float(price)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid price '{price}'. Must be a numeric value.")

    if p <= 0:
        raise ValueError(f"Price must be greater than zero, got {p}.")

    logger.debug("Price validated: %s", p)
    return p


def validate_inputs(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: str | None = None,
) -> dict:
    """
    Run all validations and return a clean parameter dict.

    Args:
        symbol:     Trading pair (e.g. 'BTCUSDT').
        side:       'BUY' or 'SELL'.
        order_type: 'MARKET' or 'LIMIT'.
        quantity:   Order quantity.
        price:      Limit price (required when order_type is LIMIT).

    Returns:
        Dict with validated keys: symbol, side, type, quantity, and
        optionally price.

    Raises:
        ValueError: On any validation failure.
    """
    params: dict = {
        "symbol": validate_symbol(symbol),
        "side": validate_side(side),
        "type": validate_order_type(order_type),
        "quantity": validate_quantity(quantity),
    }

    if params["type"] == "LIMIT":
        if price is None:
            raise ValueError("Price is required for LIMIT orders.")
        params["price"] = validate_price(price)
        params["timeInForce"] = "GTC"

    logger.info("All inputs validated: %s", params)
    return params
