import datetime as dt
import FinancialDataRetriever as fdr
import requests


class FinancialModellingPrep(fdr.FinancialDataRetriever):
    """
    Use the Financial Modelling Prep API to retrieve financial data.
    """

    def __init__(self):
        """
        Notes
        ---------
        base_url : str
            The base URL of the API endpoint
        base_args : list
            List of str to use to name the file output
        """

        self.base_url = "https://financialmodelingprep.com/api/v3/"
        self.base_args = ["FinancialModellingPrep"]

    def get_tickers(
        self, exchange=None, limit=None, query=None, output_directory=None
    ):
        """
        Function to get data of available tickers for an exchange

        Parameters
        ----------
        exchange : str
            The exchange to retrieve tickers for
        limit : int
            The number of records to retrieve
        query : str
            The search term to filter tickers by
        output_directory : str
            The directory to write the retrieved data in JSON format to

        Returns
        -------
        req
            The request object used to call the API
        """

        if exchange is None:
            exchange = ""
        if query is None:
            query = ""
        if limit is None:
            limit = ""

        endpoint = f"search?exchange={exchange}&query={query}&limit={limit}"
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
        """
        Function to get the profile of a company identified by the stock symbol

        Parameters
        ----------
        stock_symbol : str
            The stock symbol of the company to retrieve tickers for
        output_directory : str
            The directory to write the retrieved data in JSON format to

        Returns
        -------
        req
            The request object used to call the API
        """
        endpoint = f"company/profile/{stock_symbol}"
        req = requests.get(f"{self.base_url}{endpoint}")
        return self.handle_api_request(
            req,
            *self.base_args,
            "Profile",
            stock_symbol,
            output_directory=output_directory,
        )

    def get_symbols(self, output_directory=None):
        """
        Function to get all available stock symbols

        Parameters
        ----------
        output_directory : str
            The directory to write the retrieved data in JSON format to

        Returns
        -------
        req
            The request object used to call the API
        """
        endpoint = f"company/stock/list"
        req = requests.get(f"{self.base_url}{endpoint}")
        return self.handle_api_request(
            req, *self.base_args, "Symbols", output_directory=output_directory
        )

    def get_stock_historical_price(
        self, stock_symbol, from_date=None, to_date=None, output_directory=None
    ):
        """
        Function to get the historical price of a stock symbol

        Parameters
        ----------
        stock_symbol : str
            The stock symbol of the company to retrieve tickers for
        from_date : str
            Retrieves data from the specified date
            Format in YYYY-MM-DD
        to_date : str
            Retrieves data until the specified date
            Format in YYYY-MM-DD
        output_directory : str
            The directory to write the retrieved data in JSON format to

        Returns
        -------
        req
            The request object used to call the API
        """
        if from_date is None and to_date is None:
            from_date = dt.datetime.now() + dt.timedelta(days=-365)
            from_date = from_date.strftime("%Y-%m-%d")
            to_date = dt.datetime.now().strftime("%Y-%m-%d")
        elif from_date is not None and to_date is None:
            to_date = dt.datetime.strptime(
                from_date, "%Y-%m-%d"
            ) + dt.timedelta(days=365)
            to_date = to_date.strftime("%Y-%m-%d")
        elif from_date is None and to_date is not None:
            from_date = dt.datetime.strptime(
                to_date, "%Y-%m-%d"
            ) + dt.timedelta(days=-365)
            from_date = from_date.strftime("%Y-%m-%d")

        query_string = f"from={from_date}&to={to_date}"
        endpoint = f"historical-price-full/{stock_symbol}?{query_string}"
        req = requests.get(f"{self.base_url}{endpoint}")
        return self.handle_api_request(
            req,
            *self.base_args,
            "StockPrice",
            stock_symbol,
            output_directory=output_directory,
        )
