import FinancialDataRetriever as fdr
import requests


class FinancialModellingPrep(fdr.FinancialDataRetriever):
    def __init__(self):
        self.base_url = "https://financialmodelingprep.com/api/v3/"
        self.base_args = ["FinancialModellingPrep"]

    def get_tickers(
        self, exchange=None, limit=None, query=None, output_directory=None
    ):
        if exchange is None:
            exchange = ""
        if query is None:
            query = ""
        if limit is None:
            limit = ""

        endpoint = (
            f"search?exchange={exchange}&query={query}&limit={limit}"
        )
        req = requests.get(f"{self.base_url}{endpoint}")
        return self.handle_api_request(
            req,
            *self.base_args,
            "Tickers",
            exchange,
            query,
            limit,
            output_directory=output_directory,
        )

    def get_company_profile(self, stock_symbol, output_directory=None):
        endpoint = f"company/profile/{stock_symbol}"
        req = requests.get(f"{self.base_url}{endpoint}")
        return self.handle_api_request(
            req,
            *self.base_args,
            "Profile",
            stock_symbol,
            output_directory=output_directory
        )

    def get_symbols(self, output_directory=None):
        endpoint = f"company/stock/list"
        req = requests.get(f"{self.base_url}{endpoint}")
        return self.handle_api_request(
            req,
            *self.base_args,
            "Symbols",
            output_directory=output_directory
        )
