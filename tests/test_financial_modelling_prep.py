from financial_modelling import __version__
import json
import logging
import pytest
import sys


sys.path.append("financial_modelling/src/data/")


import FinancialDataRetriever


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


@pytest.fixture
def output_directory():
    return "tests/logs"


class TestFinancialModellingPrep:

    @pytest.mark.parametrize(
        "query_string", [("NASDAQ", 1, ""), ("NYSE", 1, ""),],
    )
    def test_get_tickers(self, query_string, output_directory):
        fmp = FinancialDataRetriever.FinancialModellingPrep()
        req = fmp.get_tickers(
            exchange=query_string[0],
            limit=query_string[1],
            query=query_string[2],
            output_directory=output_directory,
        )
        assert req.status_code == 200
        assert len(req.json()) == query_string[1]

    @pytest.mark.parametrize(
        "stock_symbol", ["AAPL", "AMZN", "MSFT", "NFLX", "GOOGL"]
    )
    def test_get_company_profile(self, stock_symbol, output_directory):
        fmp = FinancialDataRetriever.FinancialModellingPrep()
        req = fmp.get_company_profile(
            stock_symbol, output_directory=output_directory
        )
        assert req.status_code == 200
        assert req.json()["symbol"] == stock_symbol
