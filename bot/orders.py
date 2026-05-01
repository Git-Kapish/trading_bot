"""Order placement functions for Binance Futures testnet."""

from bot.client import BinanceClient


def place_market_order(symbol: str, side: str, quantity: float) -> dict:
    """
    Place a market order on Binance Futures testnet.
    
    Args:
        symbol: Trading pair symbol (e.g., "BTCUSDT")
        side: Order side ("BUY" or "SELL")
        quantity: Order quantity
    
    Returns:
        API response as dictionary.
    """
    client = BinanceClient()
    response = client.place_order(
        symbol=symbol,
        side=side,
        order_type="MARKET",
        quantity=quantity
    )
    
    _print_order_summary(response)
    return response


def place_limit_order(symbol: str, side: str, quantity: float, price: float) -> dict:
    """
    Place a limit order on Binance Futures testnet.
    
    Args:
        symbol: Trading pair symbol (e.g., "BTCUSDT")
        side: Order side ("BUY" or "SELL")
        quantity: Order quantity
        price: Limit price
    
    Returns:
        API response as dictionary.
    """
    client = BinanceClient()
    response = client.place_order(
        symbol=symbol,
        side=side,
        order_type="LIMIT",
        quantity=quantity,
        price=price
    )
    
    _print_order_summary(response)
    return response


def _print_order_summary(response: dict) -> None:
    """
    Print a formatted order summary from API response.
    
    Args:
        response: The API response dictionary containing order details.
    """
    # Extract key fields
    order_id = response.get("orderId", "N/A")
    status = response.get("status", "N/A")
    executed_qty = response.get("executedQty", "0")
    avg_price = response.get("avgPrice", "0")
    symbol = response.get("symbol", "N/A")
    side = response.get("side", "N/A")
    order_type = response.get("type", "N/A")
    orig_qty = response.get("origQty", "0")
    time = response.get("time", "N/A")
    
    # Print formatted summary
    print("\n" + "=" * 60)
    print("ORDER PLACED SUCCESSFULLY")
    print("=" * 60)
    print(f"Order ID:       {order_id}")
    print(f"Symbol:         {symbol}")
    print(f"Side:           {side}")
    print(f"Type:           {order_type}")
    print(f"Status:         {status}")
    print(f"Original Qty:   {orig_qty}")
    print(f"Executed Qty:   {executed_qty}")
    print(f"Average Price:  {avg_price}")
    print(f"Time:           {time}")
    print("=" * 60 + "\n")
