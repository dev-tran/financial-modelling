import FinancialDataRetriever as fdr


class YahooFinanceCrawler(fdr.FinancialDataRetriever):
    """
    The Yahoo
    """

    def __init__(self):
        pass

    def get_historical_price(
        self, stock_symbol, time_period_start, time_period_end
    ):
        pass
