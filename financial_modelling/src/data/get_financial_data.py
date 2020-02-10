import FinancialDataRetriever
import logging
import toml


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_financial_data():
    config_path = "../../data/config.toml"
    config = toml.load(config_path)
    fdr = FinancialDataRetriever.FinancialDataRetriever(
        config["credentials_file"]
    )
    config["stock_symbols"] = ["AAPL"]
    for stock in config["stock_symbols"]:
        logging.info(f"Retrieving stock data for {stock}.")
        result = fdr.get_stock_price(stock, config["output_directory"])
        logging.info(result.text)
    return 1


if __name__ == "__main__":
    get_financial_data()
