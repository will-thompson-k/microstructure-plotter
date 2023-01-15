"""
Command-line script to load a csv and generate a microstructure plot.
"""

from microplot.data import PlotterDataClass
from microplot.plotter import MicroPlotter
from microplot.schema import (
    QUOTE_DATA_COLUMNS,
    TRADE_DATA_COLUMNS,
    FILL_DATA_COLUMNS,
    ORDERS_DATA_COLUMNS,
    VAL_DATA_COLUMNS,
)
import logging
import argparse
import os.path
import pandas as pd
import sys
from typing import Any, List

def _check_file_path(file_path: str) -> bool:
    """
    Check the file_path before trying to open.

    Args:
        file_path (str): file path.

    Returns:
        bool: Boolean whether file path is valid.
    """
    
    if not file_path.endswith(".csv"):
        return False

    return os.path.isfile(file_path)

def _check(file_path: str):
    """
    Red-face test the file.

    Args:
        file_path (str): file path.

    Raises:
        Exception: file path either does not exist or is not a csv.
    """

    if not _check_file_path(file_path):
        raise Exception(f"{file_path} either does not exist or is not a csv file.")


def run_plotter_csv(command_args:List[Any]):
    """
    Main function for creating plotter via csv.

    Args:
        command_args (List[Any]): command-line args.
    """
    # logger
    logger = logging.getLogger("microplotter")
    logger.setLevel(logging.INFO)
    # console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    # formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    # add formatter to ch
    console_handler.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(console_handler)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-quote_data_file",
        "--quote_data_file",
        help="[Required] csv containing market quotes",
        type=str,
        required=True
    )
    parser.add_argument(
        "-trade_data_file",
        "--trade_data_file",
        help="csv containing market trades",
        type=str,
        required=False
    )
    parser.add_argument(
        "-fill_data_sim_file",
        "--fill_data_sim_file",
        help="csv containing fill data from sims",
        type=str,
        required=False
    )
    parser.add_argument(
        "-fill_data_prod_file",
        "--fill_data_prod_file",
        help="csv containing fill data from production",
        type=str,
        required=False
    )
    parser.add_argument(
        "-orders_data_file",
        "--orders_data_file",
        help="csv containing order data",
        type=str,
        required=False
    )
    parser.add_argument(
        "-valuation_data_file",
        "--valuation_data_file",
        help="csv containing valuation data",
        type=str,
        required=False
    )
    # read in command-line args
    args = parser.parse_args(command_args)

    # data class
    data = PlotterDataClass()

    # read in quote data
    if args.quote_data_file is not None:
        _check(args.quote_data_file)
        logger.info("Reading in quote data....")
        with open(args.quote_data_file) as file:
            data.quote_data = pd.read_csv(file, usecols=QUOTE_DATA_COLUMNS)
        logger.info("Done")

    # read in trade data
    if args.trade_data_file is not None:
        _check(args.trade_data_file)
        logger.info("Reading in trade data....")
        with open(args.trade_data_file) as file:
            data.trade_data = pd.read_csv(file, usecols=TRADE_DATA_COLUMNS)
        logger.info("Done")

    # read in fill data -- sim
    if args.fill_data_sim_file is not None:
        _check(args.fill_data_sim_file)
        logger.info("Reading in fill data sim....")
        with open(args.fill_data_sim_file) as file:
            data.fill_data_sim = pd.read_csv(file, usecols=FILL_DATA_COLUMNS)
        logger.info("Done")

    # read in fill data -- prod
    if args.fill_data_prod_file is not None:
        _check(args.fill_data_prod_file)
        logger.info("Reading in fill data prod....")
        with open(args.fill_data_prod_file) as file:
            data.fill_data_prod = pd.read_csv(file, usecols=FILL_DATA_COLUMNS)
        logger.info("Done")

    # read in orders
    if args.orders_data_file is not None:
        _check(args.orders_data_file)
        logger.info("Reading in orders data....")
        with open(args.orders_data_file) as file:
            data.orders = pd.read_csv(file, usecols=ORDERS_DATA_COLUMNS)
        logger.info("Done")

    # read in valuation data
    if args.valuation_data_file is not None:
        _check(args.valuation_data_file)
        logger.info("Reading in valuation data....")
        with open(args.valuation_data_file) as file:
            data.val_data = pd.read_csv(file, usecols=VAL_DATA_COLUMNS)
        logger.info("Done")

    # plotter
    logger.info("Creating plotter....")
    plotter = MicroPlotter(data)
    logger.info("Done")
    # call plot() method
    logger.info("Rendering plots....")
    plotter.plot()
    logger.info("Done")


if __name__ == "__main__":
    # set up this way to be able to import function
    run_plotter_csv(sys.argv[1:])