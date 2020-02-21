import io
import json
import pathlib
import psycopg2
import toml
from tqdm import tqdm


class StoreDataPostgres:
    def __init__(self, config_file):
        """
        Read config file
        """
        self.config = toml.load(config_file)

    def connect_to_database(self, role):
        user = self.config[role]
        server = self.config["server"]
        connection_string = f"""
            host={server["host"]}
            port={server["port"]}
            dbname={server["dbname"]}
            user={user["username"]}
            password={user["password"]}
        """
        conn = psycopg2.connect(connection_string)
        return conn

    def create_database(self, sql_scripts_dir):
        conn = self.connect_to_database("admin")
        cursor = conn.cursor()

        sql_scripts = [
            fp
            for fp in pathlib.Path(sql_scripts_dir).iterdir()
            if fp.is_file() and fp.suffix.lower() == ".sql"
        ]

        for fp in sql_scripts:
            with open(fp, "r") as f:
                sql_query = f.read()
            cursor.execute(sql_query)
            conn.commit()

        conn.close()

        return 1

    def setup_database(self, data_dirs, tables):
        for table, data_dir in zip(tables, data_dirs):
            truncate_sql = f"""
            TRUNCATE TABLE {self.config["server"]["schema"]}.{table}
            """
            conn = self.connect_to_database("admin")
            cursor = conn.cursor()
            cursor.execute(truncate_sql)
            conn.commit()
            conn.close()

            self.insert_data(table, data_dir)
        return 1

    def insert_data(self, table, data_dir):
        target = f"""{self.config["server"]["schema"]}.{table}"""
        data_files = [
            fp
            for fp in pathlib.Path(data_dir).iterdir()
            if fp.suffix == ".json"
        ]
        parsed_data = io.StringIO()
        for fp in tqdm(data_files):
            with open(fp, "r") as f:
                data = json.load(f)
                if len(data.keys()) > 0:
                    parsed_data_temp, columns = self.parse_data(data, table)
                    parsed_data.write(parsed_data_temp.read())
                    parsed_data.write("\n")
        parsed_data.seek(0)
        with open("test.txt", "w") as f:
            f.write(parsed_data.read())
            parsed_data.seek(0)
        conn = self.connect_to_database("admin")
        cursor = conn.cursor()
        cursor.copy_from(parsed_data, target, sep="|", columns=columns, null="")
        conn.commit()
        conn.close()
        return 1

    def parse_data(self, data, table):
        csv_io = io.StringIO()
        keep_data = [[]]
        if table == "dim_symbol":
            columns = [
                "symbol_code",
                "company_name",
                "latest_symbol_price",
                "exchange_name",
            ]
            keep_data = [
                (
                    line["symbol"],
                    line.get("name"),
                    line["price"],
                    line["exchange"],
                )
                for line in data["symbolsList"]
            ]

        elif table == "dim_profiles":
            columns = [
                "symbol_code",
                "company_name",
                "exchange_name",
                "industry_name",
                "website_link",
                "company_description",
                "ceo_name",
                "sector_name",
                "company_image",
            ]
            keep_data = [
                [
                    data["symbol"],
                    data["profile"]["companyName"],
                    data["profile"]["exchange"],
                    data["profile"]["industry"],
                    data["profile"]["website"],
                    data["profile"]["description"],
                    data["profile"]["ceo"],
                    data["profile"]["sector"],
                    data["profile"]["image"],
                ]
            ]

        elif table == "fact_prices":
            columns = [
                "symbol_code",
                "price_date",
                "open_price",
                "high_price",
                "low_price",
                "close_price",
                "adjusted_close_price",
                "volume",
                "unadjusted_volume",
                "price_change",
                "price_change_percentage",
                "vwap",
                "price_date_label",
                "change_over_time",
            ]
            keep_data = [
                (
                    data.get("symbol"),
                    line.get("date"),
                    line.get("open"),
                    line.get("high"),
                    line.get("low"),
                    line.get("close"),
                    line.get("adjClose"),
                    line.get("volume"),
                    line.get("unadjustedVolume"),
                    line.get("change"),
                    line.get("changePercent"),
                    line.get("vwap"),
                    line.get("label"),
                    line.get("changeOverTime"),
                )
                for line in data["historical"]
            ]

        keep_data_str = [
            "|".join(
                str(s).replace("\n", "") if s is not None else "" for s in line
            )
            for line in keep_data
        ]
        csv_io.write("\n".join(keep_data_str))
        csv_io.seek(0)
        return (csv_io, columns)
