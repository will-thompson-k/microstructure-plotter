"""
Interactive microstructure plot example using fake data. Python function call.
"""

from microplot.scripts.plot_csv import run_plotter_csv

fake_quote_data_path = "examples/example_1/fake_data/quote_data.csv"
fake_trade_data_path = "examples/example_1/fake_data/trade_data.csv"
fake_fill_data_path = "examples/example_1/fake_data/fill_data.csv"
fake_orders_data_path = "examples/example_1/fake_data/order_data.csv"
fake_valuation_data_path = "examples/example_1/fake_data/val_data.csv"

args = ["-quote_data_file",fake_quote_data_path,"-trade_data_file",fake_trade_data_path,"-fill_data_sim_file",fake_fill_data_path,"-orders_data_file",fake_orders_data_path,"-valuation_data_file",fake_valuation_data_path]

if __name__ == "__main__":
    run_plotter_csv(args)