import mysql.connector
from flask import render_template
from app.backend.database import connection

def get_exchangeRates_details():
    cursor = connection.cursor(dictionary=True)
    #show: id, countryName, recordYear, Series,series unit, val, source
    sql_string = """
        SELECT
            exchangeRates.id AS id,
            countries.country AS country_name,
            series.series AS series,
            exchangeRates.currency AS currency,
            exchangeRates.val AS value,
            series.unit AS unit,
            exchangeRates.recordYear AS record_year,
            sources.source AS source

        FROM exchangeRates 
        JOIN countries ON exchangeRates.countryCode = countries.countryCode
        JOIN series ON exchangeRates.seriesID = series.seriesID
        JOIN sources ON exchangeRates.sourceID = sources.sourceID

        ORDER BY id ASC
        LIMIT 20;

    """
    cursor.execute(sql_string)
    result = cursor.fetchall()
    cursor.close()
    return result

