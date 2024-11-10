CREATE DATABASE UNstatistics;
USE UNstatistics;

-- create co2emission table

CREATE TABLE co2emission (
    id int auto_increment,
    areaCode int,
    area varchar(100),
    recordYear year,
    series text, 
    val float, 
    source text,
    primary key (id)
);

LOAD DATA INFILE './database/CO2EmissionEstimates.csv'
INTO TABLE co2emission
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(areaCode, area, recordYear, series, val, source);

-- create developmentAid table

CREATE TABLE developmentAid (
    id int auto_increment,
    areaCode int,
    area varchar(100),
    recordYear year,
    series text, 
    val float, 
    source text,
    primary key (id)
);

LOAD DATA INFILE './database/DevelopmentAid.csv'
INTO TABLE developmentAid
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(areaCode, area, recordYear, series, val, source);

-- create exchangeRates table

CREATE TABLE exchangeRates (
    id int auto_increment,
    areaCode int,
    area varchar(100),
    recordYear year,
    series text,
    currency varchar(100), 
    val float, 
    source text,
    primary key (id)
);

LOAD DATA INFILE './database/ExchangeRates.csv'
INTO TABLE exchangeRates
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(areaCode, area, recordYear, series, currency, val, source);

-- create expenditureHealth table

CREATE TABLE expenditureHealth (
    id int auto_increment,
    areaCode int,
    area varchar(100),
    recordYear year,
    series text, 
    val float, 
    source text,
    primary key (id)
);

LOAD DATA INFILE './database/ExpenditureHealth.csv'
INTO TABLE expenditureHealth
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(areaCode, area, recordYear, series, val, source);

-- create importsExports table

CREATE TABLE importsExports (
    id int auto_increment,
    areaCode int,
    area varchar(100),
    recordYear year,
    series text, 
    tradeSystem char(1),
    val int, 
    source text,
    primary key (id)
);

LOAD DATA INFILE './database/ImportsExports.csv'
INTO TABLE importsExports
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(areaCode, area, recordYear, series, tradeSystem, val, source);

-- create internetUsage table

CREATE TABLE internetUsage (
    id int auto_increment,
    areaCode int,
    area varchar(100),
    recordYear year,
    series text, 
    val float, 
    source text,
    primary key (id)
);

LOAD DATA INFILE './database/InternetUsage.csv'
INTO TABLE internetUsage
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(areaCode, area, recordYear, series, val, source);

-- create threatenedSpecies table

CREATE TABLE threatenedSpecies (
    id int auto_increment,
    areaCode int,
    area varchar(100),
    recordYear year,
    series text, 
    val int, 
    source text,
    primary key (id)
);

LOAD DATA INFILE './database/ThreatenedSpecies.csv'
INTO TABLE threatenedSpecies
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(areaCode, area, recordYear, series, val, source);

-- create tourism table

CREATE TABLE tourism (
    id int auto_increment,
    areaCode int,
    area varchar(100),
    recordYear year,
    series text, 
    arrivalType varchar(5),
    val int, 
    source text,
    primary key (id)
);

LOAD DATA INFILE './database/Tourism.csv'
INTO TABLE tourism
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(areaCode, area, recordYear, series, arrivalType, val, source);

-- create regions table

CREATE TABLE regions (
    region varchar(50),
    regionCode smallint,
    primary key (regionCode)
);

LOAD DATA INFILE './database/regions.csv'
INTO TABLE regions
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(region, regionCode);

-- create sub-regions table

CREATE TABLE subRegions (
    subRegion varchar(50),
    regionCode smallint,
    subRegionCode smallint,
    sqmi float,
    sqkm float,
    primary key (subRegionCode),
    foreign key (regionCode) references regions (regionCode)
    on delete set null
    on update cascade
);

LOAD DATA INFILE './database/subRegions.csv'
INTO TABLE subRegions
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(subRegion, regionCode, subRegionCode, sqmi, sqkm);

-- create countries table

CREATE TABLE countries (
    country varchar(50),
    alpha_2 char(2),
    alpha_3 char(3),
    countryCode smallint,
    iso_3166_2 char(13),
    regionCode smallint,
    subRegionCode smallint,
    primary key (countryCode),
    foreign key (regionCode) references regions (regionCode)
    on delete set null
    on update cascade,
    foreign key (subRegionCode) references subRegions (subRegionCode)
    on delete set null
    on update cascade
);

LOAD DATA INFILE './database/countries.csv'
INTO TABLE countries
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(country, alpha_2, alpha_3, countryCode, iso_3166_2, @regionCode, @subRegionCode)
SET regionCode = NULLIF(@regionCode, ''),
    subRegionCode = NULLIF(@subRegionCode, '');