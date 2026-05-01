"""
Binance Futures Testnet client setup.
Reads API credentials from environment variables and returns
a configured UMFutures client.
"""

import os
from binance.um_futures import UMFutures
from binance.error import ClientError
from dotenv import load_dotenv

from bot.logging_config import get_logger

load_dotenv()

logger = get_logger(__name__)


def get_client() -> UMFutures:
    """
    Create and return a Binance USDT-M Futures Testnet client.

    Reads BINANCE_API_KEY and BINANCE_API_SECRET from environment variables.

    Returns:
        UMFutures client pointed at the testnet base URL.

    Raises:
        EnvironmentError: If API key or secret are missing.
        ClientError: If the client cannot authenticate with Binance.
    """
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        logger.error("BINANCE_API_KEY or BINANCE_API_SECRET not set in environment.")
        raise EnvironmentError(
            "Missing API credentials. Set BINANCE_API_KEY and BINANCE_API_SECRET "
            "in your .env file."
        )

    client = UMFutures(
        key=api_key,
        secret=api_secret,
        base_url="https://testnet.binancefuture.com",
    )

    logger.debug("Binance Futures Testnet client initialised.")
    return client
