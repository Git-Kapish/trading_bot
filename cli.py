"""Command-line interface for Binance Futures testnet trading bot."""

import argparse
import sys

from bot.logging_config import setup_logger
from bot.validators import (
    validate_order_type,
    validate_price,
    validate_quantity,
    validate_side,
    validate_symbol,
)
from bot.orders import place_limit_order, place_market_order


# Global logger instance
logger = setup_logger()


def main():
    """
    Main CLI entry point.
    
    Parses command-line arguments, validates inputs, and places orders.
    """
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
  python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 2500
        """
    )
    
    parser.add_argument(
        "--symbol",
        required=True,
        help="Trading pair symbol (e.g., BTCUSDT)"
    )
    parser.add_argument(
        "--side",
        required=True,
        help="Order side: BUY or SELL"
    )
    parser.add_argument(
        "--type",
        required=True,
        dest="order_type",
        help="Order type: MARKET or LIMIT"
    )
    parser.add_argument(
        "--quantity",
        required=True,
        help="Order quantity (positive number)"
    )
    parser.add_argument(
        "--price",
        required=False,
        help="Order price (required for LIMIT orders)"
    )
    
    args = parser.parse_args()
    
    try:
        # Log the request
        logger.info(f"Placing order: {args.symbol} {args.side} {args.order_type} {args.quantity}")
        
        # Validate inputs
        validate_symbol(args.symbol)
        validate_side(args.side)
        validate_order_type(args.order_type)
        quantity = validate_quantity(args.quantity)
        
        # Determine if price is needed
        if args.order_type == "LIMIT":
            if not args.price:
                raise ValueError("--price is required for LIMIT orders")
            price = validate_price(args.price)
        elif args.order_type == "MARKET":
            if args.price:
                logger.warning("--price is ignored for MARKET orders")
            price = None
        
        # Place order
        if args.order_type == "MARKET":
            result = place_market_order(args.symbol, args.side, quantity)
        else:  # LIMIT
            result = place_limit_order(args.symbol, args.side, quantity, price)
        
        # Log success
        order_id = result.get("orderId", "unknown")
        logger.info(f"Order placed successfully. Order ID: {order_id}")
        
    except ValueError as e:
        # Validation or API error
        error_msg = f"Validation Error: {str(e)}"
        print(f"\n❌ {error_msg}\n", file=sys.stderr)
        logger.error(error_msg)
        sys.exit(1)
    
    except Exception as e:
        # Unexpected error
        error_msg = f"Unexpected Error: {str(e)}"
        print(f"\n❌ {error_msg}\n", file=sys.stderr)
        logger.error(error_msg, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
