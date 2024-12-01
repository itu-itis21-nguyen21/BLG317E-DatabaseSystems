import mysql.connector
from flask import render_template
from app.backend.database import connection

def get_carbondioxide_details():
    cursor = connection.cursor(dictionary=True)
    #show: id, countryName, recordYear, Series,series unit, val, source
    sql_string = """
        SELECT
            carbondioxide.id AS id,
            countries.country AS country_name,
            series.series AS series,
            carbondioxide.val AS value,
            series.unit AS unit,
            carbondioxide.recordYear AS record_year,
            sources.source AS source

        FROM carbondioxide 
        JOIN countries ON carbondioxide.countryCode = countries.countryCode
        JOIN series ON carbondioxide.seriesID = series.seriesID
        JOIN sources ON carbondioxide.sourceID = sources.sourceID

        ORDER BY id ASC
        LIMIT 20;

    """
    cursor.execute(sql_string)
    result = cursor.fetchall()
    cursor.close()
    return result

