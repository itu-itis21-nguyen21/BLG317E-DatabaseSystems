import mysql.connector
from flask import render_template
from app.backend.database import connection

def get_threatenedSpecies_details():
    cursor = connection.cursor(dictionary=True)
    #show: id, countryName, recordYear, Series,series unit, val, source
    sql_string = """
        SELECT
            threatenedSpecies.id AS id,
            countries.country AS country_name,
            series.series AS series,
            threatenedSpecies.val AS value,
            series.unit AS unit,
            threatenedSpecies.recordYear AS record_year,
            sources.source AS source

        FROM threatenedSpecies 
        JOIN countries ON threatenedSpecies.countryCode = countries.countryCode
        JOIN series ON threatenedSpecies.seriesID = series.seriesID
        JOIN sources ON threatenedSpecies.sourceID = sources.sourceID

        ORDER BY id ASC
        LIMIT 20;

    """
    cursor.execute(sql_string)
    result = cursor.fetchall()
    cursor.close()
    return result

