import datetime as dt
import json
import pathlib
import requests
import toml


class FinancialDataRetriever:
    """
    The FinancialDataRetriever object is used to call data from the IEX Cloud
    API to retrieve financial data.
    """

    def __init__(self, credentials_file):

        """
        Parameters
        ----------
        credentials_file : str
            Path to file where credentials can be found.
            Credentials should be in a .toml format, with the credentials under
            the key [api].
            For tests, put the credentials under the key [sandbox-api].
        """

        self.base_url = "https://cloud.iexapis.com/stable"
        self.credentials = toml.load(credentials_file)["api"]

    def get_stock_price(self, stock_symbol, output_directory=None):

        """
        Function to get stock price of a certain stock.

        Parameters
        ----------
        stock_symbol : str
            The stock symbol of the stock to retrieve data for
        output_directory : str
            The directory to write the retrieved data in JSON format to

        Returns
        -------
        req
            The request object used to call the API
        """

        endpoint = f"stock/{stock_symbol}/batch"
        options = {
            "token": self.credentials["iex_cloud_secret"],
            "types": "quote,chart",
            "range": "1y",
        }
        query_string = "&".join(
            [f"{parameter}={value}" for parameter, value in options.items()]
        )

        url = f"{self.base_url}/{endpoint}?{query_string}"
        req = requests.get(url)

        if req.status_code != 200:
            return req

        filename = self.generate_output_filepath(stock_symbol)
        if output_directory is None:
            output_filepath = pathlib.Path(filename)
        else:
            output_filepath = pathlib.Path(output_directory).joinpath(filename)

        with open(output_filepath, "w") as f:
            json.dump(req.json(), f)

        return req

    def generate_output_filepath(self, *args):
        file_date = dt.datetime.now().strftime("%Y%m%d%H%M%S")
        args_name = "_".join(args)
        return f"{args_name}_{file_date}.json"
