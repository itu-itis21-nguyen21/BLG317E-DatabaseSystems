import mysql.connector
from flask import render_template
from app.backend.database import connection

def get_trade_details():
    cursor = connection.cursor(dictionary=True)
    #show: id, countryName, recordYear, Series,series unit, val, source
    sql_string = """
        SELECT
            trade.id AS id,
            countries.country AS country_name,
            series.series AS series,
            trade.val AS value,
            series.unit AS unit,
            trade.recordYear AS record_year,
            sources.source AS source

        FROM trade 
        JOIN countries ON trade.countryCode = countries.countryCode
        JOIN series ON trade.seriesID = series.seriesID
        JOIN sources ON trade.sourceID = sources.sourceID

        ORDER BY id ASC
        LIMIT 20;

    """
    cursor.execute(sql_string)
    result = cursor.fetchall()
    cursor.close()
    return result

