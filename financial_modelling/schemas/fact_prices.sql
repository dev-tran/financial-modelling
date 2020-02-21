CREATE TABLE IF NOT EXISTS financialmodelling.fact_prices
(
    price_id INT GENERATED ALWAYS AS IDENTITY,
    symbol_code VARCHAR(10),
    price_date DATE,
    open_price DOUBLE PRECISION,
    high_price DOUBLE PRECISION,
    low_price DOUBLE PRECISION,
    close_price DOUBLE PRECISION,
    adjusted_close_price DOUBLE PRECISION,
    volume DOUBLE PRECISION,
    unadjusted_volume DOUBLE PRECISION,
    price_change DOUBLE PRECISION,
    price_change_percentage DOUBLE PRECISION,
    vwap DOUBLE PRECISION,
    price_date_label VARCHAR(50),
    change_over_time DOUBLE PRECISION,
    CONSTRAINT pk_fact_prices
    PRIMARY KEY (symbol_code, price_date)
);