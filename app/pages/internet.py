import mysql.connector
from flask import render_template
from app.backend.database import connection

def get_internet_details():
    cursor = connection.cursor(dictionary=True)
    #show: id, countryName, recordYear, Series,series unit, val, source
    sql_string = """
        SELECT
            internet.id AS id,
            countries.country AS country_name,
            series.series AS series,
            internet.val AS value,
            series.unit AS unit,
            internet.recordYear AS record_year,
            sources.source AS source

        FROM internet 
        JOIN countries ON internet.countryCode = countries.countryCode
        JOIN series ON internet.seriesID = series.seriesID
        JOIN sources ON internet.sourceID = sources.sourceID

        ORDER BY id ASC
        LIMIT 20;

    """
    cursor.execute(sql_string)
    result = cursor.fetchall()
    cursor.close()
    return result

