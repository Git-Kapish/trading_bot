"""Binance Futures testnet API client with HMAC-SHA256 signing."""

import hashlib
import hmac
import logging
import os
import time
import urllib.parse

import requests
from dotenv import load_dotenv


class BinanceClient:
    """
    Client for Binance Futures testnet API.
    
    Handles HMAC-SHA256 signed requests to the testnet API.
    Requires API_KEY and API_SECRET from environment variables.
    """
    
    BASE_URL = "https://testnet.binancefuture.com"
    
    def __init__(self):
        """
        Initialize the BinanceClient.
        
        Loads API credentials from .env file.
        
        Raises:
            ValueError: If API_KEY or API_SECRET are not set in environment.
        """
        load_dotenv()
        self.logger = logging.getLogger("trading_bot")
        
        self.api_key = os.getenv("API_KEY")
        self.api_secret = os.getenv("API_SECRET")
        
        if not self.api_key:
            raise ValueError("API_KEY not set in .env file")
        if not self.api_secret:
            raise ValueError("API_SECRET not set in .env file")
        
        # Initialize session with proper headers
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded"
        })
    
    def _sign(self, params: dict) -> str:
        """
        Generate HMAC-SHA256 signature for request.
        
        CRITICAL: Encode params in exact same order they will be sent.
        Uses urllib.parse.urlencode which properly encodes special characters.
        
        Args:
            params: The parameters to sign (without signature field)
        
        Returns:
            The HMAC-SHA256 signature as a hex string.
        """
        query_string = urllib.parse.urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: float | None = None
    ) -> dict:
        """
        Place an order on the Binance Futures testnet.
        
        Args:
            symbol: Trading pair symbol (e.g., "BTCUSDT")
            side: Order side ("BUY" or "SELL")
            order_type: Order type ("MARKET" or "LIMIT")
            quantity: Order quantity
            price: Order price (required for LIMIT orders, ignored for MARKET)
        
        Returns:
            API response as dictionary containing order details.
        
        Raises:
            requests.RequestException: If the HTTP request fails.
        """
        endpoint = "/fapi/v1/order"
        url = self.BASE_URL + endpoint
        
        # Build params WITHOUT signature first
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": f"{float(quantity):.3f}",
            "timestamp": int(time.time() * 1000),
            "recvWindow": 5000
        }
        
        # Add price for LIMIT orders
        if order_type == "LIMIT" and price is not None:
            params["timeInForce"] = "GTC"  # Good Till Cancel
            params["price"] = f"{float(price):.2f}"
        
        # Sign AFTER all params are set
        params["signature"] = self._sign(params)
        
        # Log request details
        query_string = urllib.parse.urlencode(params)
        self.logger.info(f"Sending order request to {url}")
        self.logger.info(f"Request body: {query_string}")
        
        try:
            # Send as POST body (data=), NOT as query params (params=)
            response = self.session.post(url, data=params, timeout=10)
            
            # Read response body before checking status
            try:
                data = response.json()
            except ValueError:
                data = None
            
            # Check HTTP status
            if not response.ok:
                if data and "code" in data:
                    error_msg = f"Binance API Error {data.get('code')}: {data.get('msg', 'Unknown error')}"
                else:
                    error_msg = f"HTTP {response.status_code}: {response.text}"
                self.logger.error(error_msg)
                raise requests.RequestException(error_msg)
            
            # Check for API error in response body
            if data and "code" in data and data["code"] != 200:
                error_msg = f"Binance API Error {data.get('code')}: {data.get('msg', 'Unknown error')}"
                self.logger.error(error_msg)
                raise requests.RequestException(error_msg)
            
            if data:
                self.logger.info(f"Order response received: {data}")
            
            return data if data else {}
        
        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to place order: {str(e)}"
            self.logger.error(error_msg)
            raise requests.RequestException(error_msg)
