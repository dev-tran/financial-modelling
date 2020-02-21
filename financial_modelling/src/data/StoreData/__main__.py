from StoreDataPostgres import *


if __name__ == "__main__":
    pg = StoreDataPostgres("../../data/StoreDataPostgres.toml")
    pg.create_database("../../schemas/")
    # pg.insert_data("dim_profiles", "../../data/profiles")
    pg.setup_database(
        data_dirs=[
            "../../data/profiles",
            "../../data/symbols",
            "../../data/stock_prices",
        ],
        tables=["dim_profiles", "dim_symbol", "fact_prices",],
    )
