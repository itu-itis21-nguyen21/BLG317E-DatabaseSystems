import mysql.connector
from flask import render_template
from app.backend.database import connection

def get_health_details():
    cursor = connection.cursor(dictionary=True)
    #show: id, countryName, recordYear, Series,series unit, val, source
    sql_string = """
        SELECT
            health.id AS id,
            countries.country AS country_name,
            series.series AS series,
            health.val AS value,
            series.unit AS unit,
            health.recordYear AS record_year,
            sources.source AS source

        FROM health 
        JOIN countries ON health.countryCode = countries.countryCode
        JOIN series ON health.seriesID = series.seriesID
        JOIN sources ON health.sourceID = sources.sourceID

        ORDER BY id ASC
        LIMIT 20;

    """
    cursor.execute(sql_string)
    result = cursor.fetchall()
    cursor.close()
    return result

