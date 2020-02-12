import argparse
from FinancialModellingPrep import *


def main():
    parser = argparse.ArgumentParser(
        description="Utility to retrieve financial data"
    )

    args_config = [
        {
            "arg": ["command"],
            "help": "The command to run",
            "choices": ["tickers", "company", "symbols", "prices"],
        },
        {"arg": ["-e", "--exchange"], "help": "The exchange to get data for"},
        {
            "arg": ["-o", "--output"],
            "help": "The directory to write the output to",
        },
        {"arg": ["-n", "--number"], "help": "The number of records to return"},
        {"arg": ["-q", "--query"], "help": "The search term to query for"},
        {
            "arg": ["-s", "--stock-symbol"],
            "help": "The stock symbol to return data for",
        },
        {"arg": ["-f", "--from-date"], "help": "The date to return data for"},
        {"arg": ["-t", "--to-date"], "help": "The date to return data to"},
    ]

    for arg_entry in args_config:
        if "metavar" not in arg_entry.keys():
            arg_entry["metavar"] = ""
        arg_as_dict = {k: v for k, v in arg_entry.items() if k != "arg"}
        parser.add_argument(*arg_entry["arg"], **arg_as_dict)

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = main()

    data_retriever = FinancialModellingPrep()

    if args.command == "tickers":
        req = data_retriever.get_tickers(
            exchange=args.exchange,
            limit=args.number,
            query=args.query,
            output_directory=args.output,
        )

    elif args.command == "company":
        req = data_retriever.get_company_profile(
            stock_symbol=args.stock_symbol, output_directory=args.output
        )

    elif args.command == "symbols":
        req = data_retriever.get_symbols(output_directory=args.output)

    elif args.command == "prices":
        req = data_retriever.get_stock_historical_price(
            stock_symbol=args.stock_symbol,
            from_date=args.from_date,
            to_date=args.to_date,
            output_directory=args.output,
        )
