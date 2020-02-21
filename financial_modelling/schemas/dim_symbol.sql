CREATE TABLE IF NOT EXISTS financialmodelling.dim_symbol
(
    symbol_id INT GENERATED ALWAYS AS IDENTITY,
    symbol_code VARCHAR(10),
    company_name VARCHAR(200),
    latest_symbol_price DOUBLE PRECISION,
    exchange_name VARCHAR(200),
    CONSTRAINT pk_dim_symbol
    PRIMARY KEY (symbol_code)
);
