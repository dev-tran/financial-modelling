from financial_modelling import __version__
import logging
import toml
import sys

sys.path.append("financial_modelling/src/data/")


import FinancialDataRetriever


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


def test_version():
    assert __version__ == "0.1.0"


def test_get_stock_price():
    credentials_file = "financial_modelling/data/credentials.toml"
    fdr = FinancialDataRetriever.FinancialDataRetriever(
        credentials_file,
    )
    fdr.credentials = toml.load(credentials_file)["sandbox-api"]
    fdr.base_url = "https://sandbox.iexapis.com/stable"
    result = fdr.get_stock_price("MSFT", "tests/logs")
    assert result.status_code == 200
    assert result.json()["quote"]["symbol"] == "MSFT"
