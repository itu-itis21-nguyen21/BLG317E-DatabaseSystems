import mysql.connector
from flask import render_template
from app.backend.database import connection

def get_aid_details():
    cursor = connection.cursor(dictionary=True)
    #show: id, countryName, recordYear, Series,series unit, val, source
    sql_string = """
        SELECT
            aid.id AS id,
            countries.country AS country_name,
            series.series AS series,
            aid.val AS value,
            series.unit AS unit,
            aid.recordYear AS record_year,
            sources.source AS source

        FROM aid 
        JOIN countries ON aid.countryCode = countries.countryCode
        JOIN series ON aid.seriesID = series.seriesID
        JOIN sources ON aid.sourceID = sources.sourceID

        ORDER BY id ASC
        LIMIT 20;

    """
    cursor.execute(sql_string)
    result = cursor.fetchall()
    cursor.close()
    return result

