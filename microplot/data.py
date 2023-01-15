"""
This module contains the PlotterDataClass for the plotting object.
"""

from dataclasses import dataclass
import pandas as pd
from typing import Tuple, List
from microplot.schema import (
    QUOTE_DATA_COLUMNS,
    TRADE_DATA_COLUMNS,
    FILL_DATA_COLUMNS,
    ORDERS_DATA_COLUMNS,
    VAL_DATA_COLUMNS,
)


@dataclass
class PlotterDataClass:
    """
    A dataclass to pass data to the microstructure plotter.

    NOTE: See required fields in each property setter function or the data schema.

    _quote_data (pd.DataFrame): time series of best bid and offer prices and microprice ("weight ave")
    _trade_data (pd.DataFrame): time series of trade prices.
    _fill_data_sim (pd.DataFrame): time series of system fill data (but for simulations).
    _fill_data_prod (pd.DataFrame): time series of system fill data (but for prod).
    _orders (pd.DataFrame): time series of exchange order activity. Currently only news, cancels, rejects.
    _val_data (pd.DataFrame): time series of system valuation data-> theoretical price, "bid edge", "ask edge" (if market-making).
    """

    _quote_data: pd.DataFrame = None
    _trade_data: pd.DataFrame = None
    _fill_data_sim: pd.DataFrame = None
    _fill_data_prod: pd.DataFrame = None
    _orders: pd.DataFrame = None
    _val_data: pd.DataFrame = None

    def get_symbols(self) -> List[str]:
        """
        Method for grabbing all symbols in dataclass.

        Returns:
            List[str]: list of symbols found across all data series.
        """
        symbol_set = set()
        time_series = [
            self._quote_data,
            self.trade_data,
            self._fill_data_prod,
            self._fill_data_sim,
            self._orders,
            self._val_data,
        ]
        for series in time_series:
            series_symbols = series["symbol"].ravel() if series is not None else None
            if series_symbols is not None:
                for symbol in series_symbols:
                    symbol_set.add(symbol)

        return list(symbol_set)

    @staticmethod
    def _validate_timestamps(timeseries: pd.Series) -> bool:
        """
        Timestamps should be EPOCH nanosecond precision, integer timestamps.

        This equates to 19 digit ints.

        Args:
            ts (pd.Series): pandas Series object containing timestamps.

        Returns:
            bool: true/false indicating whether timestamps are valid.
        """
        return all(timeseries.apply(lambda x: len(list(str(x))) == 19)) == True

    @staticmethod
    def _convert_timestamps(timeseries: pd.Series) -> pd.Series:
        """
        Convert timestamps from nanosecond ints -> second-level floats.

        Args:
            ts (pd.Series): pandas Series object containing timestamps.

        Returns:
            pd.Series: converted timeseries.
        """
        return timeseries.apply(lambda x: x * 1e-9)

    @classmethod
    def _check_columns(cls, columns: List[str], data: pd.DataFrame, name: str):
        """
        Checks a pandas dataframe timeseries that it contains the required fields
        prior to setting the value. Also sanity-checks the timestamps are valid.

        Args:
            columns (List[str]): Names of required columns for data schema.
            data (pd.DataFrame): Pandas dataframe containing time series.
            name (str): Name of time series to be set.

        Raises:
            Exception: Required column not found.
        """

        assert type(data) is pd.DataFrame

        for column in columns:
            if column not in data.columns:
                raise Exception(f"column:{column} not in {name}")

        assert "timestamp" in data.columns

        assert cls._validate_timestamps(data["timestamp"])

        data["timestamp"] = cls._convert_timestamps(data["timestamp"])

    @property
    def quote_data(self) -> pd.DataFrame:
        """
        Quote data property getter.

        Returns:
            pd.DataFrame: Quote data.
        """
        return self._quote_data

    @quote_data.setter
    def quote_data(self, data: pd.DataFrame):
        """
        Quote data property setter.

        Args:
            data (pd.DataFrame): Quote data.
        """
        # timestamp, symbol, bid_price, ask_price, micro_price

        self._check_columns(QUOTE_DATA_COLUMNS, data, "quote_data")
        self._quote_data = data

    @property
    def trade_data(self) -> pd.DataFrame:
        """
        Trade data property getter.

        Returns:
            pd.DataFrame: Trade data.
        """
        return self._trade_data

    @trade_data.setter
    def trade_data(self, data: pd.DataFrame):
        """
        Trade data property setter.

        Args:
            data (pd.DataFrame): Trade data.
        """
        # timestamp, symbol, price

        self._check_columns(TRADE_DATA_COLUMNS, data, "trade_data")
        self._trade_data = data

    @property
    def fill_data_sim(
        self,
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Fill data sim property getter.

        Returns:
            Tuple[pd.DataFrame,pd.DataFrame,pd.DataFrame,pd.DataFrame]:
               [buy_aggressive_fills, buy_passive_fills, sell_aggressive_fills, sell_passive_fills]
        """

        if self._fill_data_sim is None:
            return None, None, None, None

        buy_aggressive_fills = self._fill_data_sim[
            self._fill_data_sim.is_buy & self._fill_data_sim.is_aggressive
        ]
        buy_passive_fills = self._fill_data_sim[
            self._fill_data_sim.is_buy & ~self._fill_data_sim.is_aggressive
        ]
        sell_aggressive_fills = self._fill_data_sim[
            ~self._fill_data_sim.is_buy & self._fill_data_sim.is_aggressive
        ]
        sell_passive_fills = self._fill_data_sim[
            ~self._fill_data_sim.is_buy & ~self._fill_data_sim.is_aggressive
        ]

        return (
            buy_aggressive_fills,
            buy_passive_fills,
            sell_aggressive_fills,
            sell_passive_fills,
        )

    @fill_data_sim.setter
    def fill_data_sim(self, data: pd.DataFrame):
        """
        Fill data property setter.

        Args:
            data (pd.DataFrame): Fill data.
        """
        # timestamp, symbol, price, is_buy, is_aggressive

        self._check_columns(FILL_DATA_COLUMNS, data, "fill_data_sim")
        self._fill_data_sim = data

    @property
    def fill_data_prod(
        self,
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Fill data prod property getter.

        Returns:
            Tuple[pd.DataFrame,pd.DataFrame,pd.DataFrame,pd.DataFrame]:
               [buy_aggressive_fills, buy_passive_fills, sell_aggressive_fills, sell_passive_fills]
        """
        if self._fill_data_prod is None:
            return None, None, None, None

        buy_aggressive_fills = self._fill_data_prod[
            self._fill_data_prod.is_buy & self._fill_data_prod.is_aggressive
        ]
        buy_passive_fills = self._fill_data_prod[
            self._fill_data_prod.is_buy & ~self._fill_data_prod.is_aggressive
        ]
        sell_aggressive_fills = self._fill_data_prod[
            ~self._fill_data_prod.is_buy & self._fill_data_prod.is_aggressive
        ]
        sell_passive_fills = self._fill_data_prod[
            ~self._fill_data_prod.is_buy & ~self._fill_data_prod.is_aggressive
        ]

        return (
            buy_aggressive_fills,
            buy_passive_fills,
            sell_aggressive_fills,
            sell_passive_fills,
        )


    @fill_data_prod.setter
    def fill_data_prod(self, data: pd.DataFrame):
        """
        Fill data property setter.

        Args:
            data (pd.DataFrame): Fill data.
        """
        # timestamp, symbol, price, is_buy, is_aggressive

        self._check_columns(FILL_DATA_COLUMNS, data, "fill_data_prod")
        self._fill_data_prod = data

    @property
    def orders(
        self,
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Order data property getter.

        Returns:
            Tuple[pd.DataFrame,pd.DataFrame,pd.DataFrame,pd.DataFrame,pd.DataFrame]:
                [new_orders,new_order_acks,cancel_orders,cancel_order_acks, rejects]
        """
        # new, new_ack, cxl, cxl_ack, rej
        # TODO: add modifies and all the other types

        if self._orders is None:
            return None, None, None, None, None

        new_orders = self._orders[self._orders.is_new & ~self._orders.is_ack]
        new_order_acks = self._orders[self._orders.is_new & self._orders.is_ack]
        cancel_orders = self._orders[self._orders.is_cancel & ~self._orders.is_ack]
        cancel_orders_acks = self._orders[self._orders.is_cancel & self._orders.is_ack]
        rejects = self._orders[self._orders.is_reject]

        return new_orders, new_order_acks, cancel_orders, cancel_orders_acks, rejects

    @orders.setter
    def orders(self, data: pd.DataFrame):
        """
        Order data property setter.

        Args:
            data (pd.DataFrame): Order data.
        """
        # timestamp, symbol, price, is_new, is_cancel, is_reject, is_ack

        self._check_columns(ORDERS_DATA_COLUMNS, data, "orders")
        self._orders = data

    @property
    def val_data(self) -> pd.DataFrame:
        """
        Valuation data property getter.

        Returns:
            pd.DataFrame: valuation data.
        """
        return self._val_data


    @val_data.setter
    def val_data(self, data: pd.DataFrame):
        """
        Valuation data property setter.

        Args:
            data (pd.DataFrame): Val data.
        """
        # timestamp, symbol, theo_price

        self._check_columns(VAL_DATA_COLUMNS, data, "val_data")
        self._val_data = data