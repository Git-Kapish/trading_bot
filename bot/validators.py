"""Input validation functions for trading bot orders."""


def validate_symbol(symbol: str) -> None:
    """
    Validate trading pair symbol.
    
    Args:
        symbol: The symbol to validate (e.g., "BTCUSDT")
    
    Raises:
        ValueError: If symbol is invalid.
    """
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Symbol must be a non-empty string")
    
    if not symbol.isupper():
        raise ValueError("Symbol must be in uppercase (e.g., BTCUSDT)")
    
    if len(symbol) < 5:
        raise ValueError("Symbol appears too short (minimum 5 characters)")


def validate_side(side: str) -> None:
    """
    Validate order side (BUY or SELL).
    
    Args:
        side: The side to validate
    
    Raises:
        ValueError: If side is not BUY or SELL.
    """
    if side not in ("BUY", "SELL"):
        raise ValueError("Side must be 'BUY' or 'SELL'")


def validate_order_type(order_type: str) -> None:
    """
    Validate order type (MARKET or LIMIT).
    
    Args:
        order_type: The order type to validate
    
    Raises:
        ValueError: If order type is not MARKET or LIMIT.
    """
    if order_type not in ("MARKET", "LIMIT"):
        raise ValueError("Order type must be 'MARKET' or 'LIMIT'")


def validate_quantity(quantity: str) -> float:
    """
    Validate and convert order quantity to float.
    
    Args:
        quantity: The quantity string to validate
    
    Returns:
        The quantity as a float.
    
    Raises:
        ValueError: If quantity is not a positive number.
    """
    try:
        qty = float(quantity)
    except (ValueError, TypeError):
        raise ValueError("Quantity must be a valid number")
    
    if qty <= 0:
        raise ValueError("Quantity must be a positive number (> 0)")
    
    return qty


def validate_price(price: str) -> float:
    """
    Validate and convert order price to float.
    
    Args:
        price: The price string to validate
    
    Returns:
        The price as a float.
    
    Raises:
        ValueError: If price is not a positive number.
    """
    try:
        prc = float(price)
    except (ValueError, TypeError):
        raise ValueError("Price must be a valid number")
    
    if prc <= 0:
        raise ValueError("Price must be a positive number (> 0)")
    
    return prc
