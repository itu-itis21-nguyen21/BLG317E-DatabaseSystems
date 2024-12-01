CREATE DATABASE IF NOT EXISTS un_stats23;
USE un_stats23;

-- create regions table

CREATE TABLE regions (
    region varchar(20) not null,
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

CREATE TABLE subregions (
    subregion varchar(50) not null,
    subregionCode smallint,
    regionCode smallint,
    sqmi float,
    sqkm float,
    primary key (subregionCode),
    foreign key (regionCode) references regions (regionCode)
    on delete set null
    on update cascade
);

LOAD DATA INFILE './database/subregions.csv'
INTO TABLE subregions
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(subRegion, subregionCode, regionCode, sqmi, sqkm);

-- create countries table

CREATE TABLE countries (
    country varchar(50) not null,
    countryCode smallint,
    alpha_2 char(2),
    alpha_3 char(3),
    iso_3166_2 char(13),
    regionCode smallint,
    subRegionCode smallint,
    primary key (countryCode),
    foreign key (regionCode) references regions (regionCode)
    on delete set null
    on update cascade,
    foreign key (subregionCode) references subregions (subregionCode)
    on delete set null
    on update cascade
);

LOAD DATA INFILE './database/countries.csv'
INTO TABLE countries
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(country, countryCode, alpha_2, alpha_3, iso_3166_2, regionCode, subregionCode);

-- create series table

CREATE TABLE series (
    seriesID smallint,
    series text not null,
    unit text,
    primary key (seriesID)
);

LOAD DATA INFILE './database/series.csv'
INTO TABLE series
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(seriesID, series, unit);

-- create sources table

CREATE TABLE sources (
    sourceID smallint,
    source text not null,
    primary key (sourceID)
);

LOAD DATA INFILE './database/sources.csv'
INTO TABLE sources
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(sourceID, source);

-- create carbondioxide table

CREATE TABLE carbondioxide (
    id smallint auto_increment,
    countryCode smallint not null,
    recordYear year,
    seriesID smallint not null, 
    val float, 
    sourceID smallint,
    accessTime varchar(20),
    primary key (id),
    foreign key (countryCode) references countries (countryCode)
    on delete restrict
    on update cascade,
    foreign key (seriesID) references series (seriesID)
    on delete restrict
    on update cascade,
    foreign key (sourceID) references sources (sourceID)
    on delete set null
    on update cascade
);

LOAD DATA INFILE './database/CO2Emission.csv'
INTO TABLE carbondioxide
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(countryCode,recordYear,seriesID,val,sourceID,accessTime);

-- create aid table

CREATE TABLE aid (
    id smallint auto_increment,
    countryCode smallint not null,
    recordYear year,
    seriesID smallint not null, 
    val float, 
    sourceID smallint,
    accessTime varchar(20),
    primary key (id),
    foreign key (countryCode) references countries (countryCode)
    on delete restrict
    on update cascade,
    foreign key (seriesID) references series (seriesID)
    on delete restrict
    on update cascade,
    foreign key (sourceID) references sources (sourceID)
    on delete set null
    on update cascade
);

LOAD DATA INFILE './database/DevelopmentAid.csv'
INTO TABLE aid
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(countryCode,recordYear,seriesID,val,sourceID,accessTime);

-- create exchangeRates table

CREATE TABLE exchangeRates (
    id smallint auto_increment,
    countryCode smallint not null,
    recordYear year,
    seriesID smallint not null, 
    currency varchar(50),
    val float, 
    sourceID smallint,
    accessTime varchar(20),
    primary key (id),
    foreign key (countryCode) references countries (countryCode)
    on delete restrict
    on update cascade,
    foreign key (seriesID) references series (seriesID)
    on delete restrict
    on update cascade,
    foreign key (sourceID) references sources (sourceID)
    on delete set null
    on update cascade
);

LOAD DATA INFILE './database/ExchangeRates.csv'
INTO TABLE exchangeRates
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(countryCode,recordYear,seriesID,@currency,val,sourceID,accessTime)
SET currency = NULLIF(@currency, '');

-- create health table

CREATE TABLE health (
    id smallint auto_increment,
    countryCode smallint not null,
    recordYear year,
    seriesID smallint not null, 
    val float, 
    sourceID smallint,
    accessTime varchar(20),
    primary key (id),
    foreign key (countryCode) references countries (countryCode)
    on delete restrict
    on update cascade,
    foreign key (seriesID) references series (seriesID)
    on delete restrict
    on update cascade,
    foreign key (sourceID) references sources (sourceID)
    on delete set null
    on update cascade
);

LOAD DATA INFILE './database/ExpenditureHealth.csv'
INTO TABLE health
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(countryCode,recordYear,seriesID,val,sourceID,accessTime);

-- create trade table

CREATE TABLE trade (
    id smallint auto_increment,
    countryCode smallint not null,
    recordYear year,
    seriesID smallint not null, 
    val int, 
    sourceID smallint,
    accessTime varchar(20),
    primary key (id),
    foreign key (countryCode) references countries (countryCode)
    on delete restrict
    on update cascade,
    foreign key (seriesID) references series (seriesID)
    on delete restrict
    on update cascade,
    foreign key (sourceID) references sources (sourceID)
    on delete set null
    on update cascade
);

LOAD DATA INFILE './database/ImportsExports.csv'
INTO TABLE trade
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(countryCode,recordYear,seriesID,val,sourceID,accessTime);

-- create internet table

CREATE TABLE internet (
    id smallint auto_increment,
    countryCode smallint not null,
    recordYear year,
    seriesID smallint not null, 
    val float, 
    sourceID smallint,
    accessTime varchar(20),
    primary key (id),
    foreign key (countryCode) references countries (countryCode)
    on delete restrict
    on update cascade,
    foreign key (seriesID) references series (seriesID)
    on delete restrict
    on update cascade,
    foreign key (sourceID) references sources (sourceID)
    on delete set null
    on update cascade
);

LOAD DATA INFILE './database/InternetUsage.csv'
INTO TABLE internet
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(countryCode,recordYear,seriesID,val,sourceID,accessTime);

-- create threatenedSpecies table

CREATE TABLE threatenedSpecies (
    id smallint auto_increment,
    countryCode smallint not null,
    recordYear year,
    seriesID smallint not null, 
    val smallint, 
    sourceID smallint,
    accessTime varchar(20),
    primary key (id),
    foreign key (countryCode) references countries (countryCode)
    on delete restrict
    on update cascade,
    foreign key (seriesID) references series (seriesID)
    on delete restrict
    on update cascade,
    foreign key (sourceID) references sources (sourceID)
    on delete set null
    on update cascade
);

LOAD DATA INFILE './database/ThreatenedSpecies.csv'
INTO TABLE threatenedSpecies
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(countryCode,recordYear,seriesID,val,sourceID,accessTime);

-- create tourism table

CREATE TABLE tourism (
    id smallint auto_increment,
    countryCode smallint not null,
    recordYear year,
    seriesID smallint not null, 
    val int, 
    sourceID smallint,
    accessTime varchar(20),
    primary key (id),
    foreign key (countryCode) references countries (countryCode)
    on delete restrict
    on update cascade,
    foreign key (seriesID) references series (seriesID)
    on delete restrict
    on update cascade,
    foreign key (sourceID) references sources (sourceID)
    on delete set null
    on update cascade
);

LOAD DATA INFILE './database/Tourism.csv'
INTO TABLE tourism
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(countryCode,recordYear,seriesID,val,sourceID,accessTime);