CREATE TABLE IF NOT EXISTS financialmodelling.dim_profiles
(
    profile_id INT GENERATED ALWAYS AS IDENTITY,
    symbol_code VARCHAR(10),
    company_name VARCHAR(200),
    exchange_name VARCHAR(200),
    industry_name VARCHAR(200),
    website_link VARCHAR(200),
    company_description VARCHAR(1000),
    ceo_name VARCHAR(200),
    sector_name VARCHAR(200),
    company_image VARCHAR(200),
    CONSTRAINT pk_dim_profile
    PRIMARY KEY (symbol_code)
);
