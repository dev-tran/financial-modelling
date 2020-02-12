from financial_modelling import __version__
import logging
import pytest
import toml
import sys


sys.path.append("financial_modelling/src/data/")


import FinancialDataRetriever


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


@pytest.mark.skip
def test_get_stock_price():
    fdr = FinancialDataRetriever.YahooFinanceCrawler()
    result = fdr.get_stock_price("MSFT")
    assert result.status_code == 200
