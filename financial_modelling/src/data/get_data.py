import FinancialDataRetriever
import logging
import pathlib
from tqdm import tqdm


ROOT_DATA_PATH = "../../data/"


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger()

logger.warning("Starting data retriever class")
data_retriever = FinancialDataRetriever.FinancialModellingPrep()


data_dir = pathlib.Path(ROOT_DATA_PATH)
datasets = ["symbols", "profiles", "stock_prices"]
logger.warning("Generating directories")
dir_map = {d: data_dir.joinpath(d) for d in datasets}

for dir_name, dir_path in dir_map.items():
    dir_path.mkdir(exist_ok=True)

logger.warning("Retrieving symbols")
raw_symbols_data = data_retriever.get_symbols(
    output_directory=dir_map["symbols"]
).json()
all_symbols = [s["symbol"] for s in raw_symbols_data["symbolsList"]]

for dataset in datasets[1:]:
    logger.warning(f"Generating data for {dataset}")
    current_files = [fp.stem for fp in dir_map[dataset].iterdir()]
    existing_symbols = [fn.split("_")[2] for fn in current_files]
    new_symbols = [s for s in all_symbols if s not in existing_symbols]
    logging.warning(f"Number of symbols to retrieve: {len(new_symbols)}")
    for symbol in tqdm(new_symbols):
        if dataset == "profiles":
            data_retriever.get_company_profile(
                symbol, output_directory=dir_map[dataset]
            )
        elif dataset == "stock_prices":
            data_retriever.get_stock_historical_price(
                symbol,
                from_date="2000-01-01",
                to_date="2020-01-02",
                output_directory=dir_map[dataset],
            )
