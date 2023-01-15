"""
This module contains the column names ("data schema") for the required inputs.
"""

QUOTE_DATA_COLUMNS = ["timestamp", "symbol", "bid_price", "ask_price", "micro_price"]
TRADE_DATA_COLUMNS = ["timestamp", "symbol", "price"]
FILL_DATA_COLUMNS = ["timestamp", "symbol", "price", "is_buy", "is_aggressive"]
ORDERS_DATA_COLUMNS = [
    "timestamp",
    "symbol",
    "price",
    "is_new",
    "is_cancel",
    "is_reject",
    "is_ack",
]
VAL_DATA_COLUMNS = ["timestamp", "symbol", "theo_price"]
