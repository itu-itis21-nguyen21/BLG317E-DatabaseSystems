import mysql.connector
from flask import render_template
from database import connection

def get_tourism_details(country_code):
    cursor = connection.cursor(dictionary=True)
    #show: id, countryName, recordYear, Series,series unit, val, source
    sql_string = """
        SELECT
            tourism.id AS id,
            countries.country AS country_name,
            series.series AS series,
            tourism.val AS value,
            series.unit AS unit,
            tourism.recordYear AS record_year,
            sources.source AS source

        FROM tourism 
        JOIN countries ON tourism.countryCode = countries.countryCode
        JOIN series ON tourism.seriesID = series.seriesID
        JOIN sources ON tourism.sourceID = sources.sourceID

        ORDER BY id ASC
        LIMIT 20;

    """
    cursor.execute(sql_string, (country_code,))
    result = cursor.fetchone()
    cursor.close()
    return result

