from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from database import connection

threatenedSpecies_bp = Blueprint('threatenedSpecies', __name__)

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

@threatenedSpecies_bp.route('/threatenedSpecies')
@login_required
def page1():
    threatenedSpecies_details = get_threatenedSpecies_details()
    return render_template('threatenedSpecies.html', details=threatenedSpecies_details)

@threatenedSpecies_bp.route('/threatenedSpecies/add', methods=['GET', 'POST'])
@login_required
def add_record():
    if request.method == 'POST':
        # Retrieve form data
        country_code = request.form['country_code']
        series_id = request.form['series_id']
        value = request.form['value']
        record_year = request.form['record_year']
        source_id = request.form['source_id']
        
        # Insert into the database
        cursor = connection.cursor()
        sql = """
            INSERT INTO threatenedSpecies (countryCode, seriesID, val, recordYear, sourceID)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (country_code, series_id, value, record_year, source_id))
        connection.commit()
        cursor.close()
        
        return redirect('/threatenedSpecies')
    
    return render_template('add.html')

@threatenedSpecies_bp.route('/threatenedSpecies/edit/<int:record_id>', methods=['GET', 'POST'])
@login_required
def edit_record(record_id):
    if request.method == 'POST':
        # Retrieve updated data
        value = request.form['value']
        record_year = request.form['record_year']
        
        # Update the database
        cursor = connection.cursor()
        sql = """
            UPDATE threatenedSpecies
            SET val = %s, recordYear = %s
            WHERE id = %s
        """
        cursor.execute(sql, (value, record_year, record_id))
        connection.commit()
        cursor.close()
        
        return redirect('/threatenedSpecies')
    
    # Fetch existing data for the record
    cursor = connection.cursor(dictionary=True)
    sql = "SELECT * FROM threatenedSpecies WHERE id = %s"
    cursor.execute(sql, (record_id,))
    record = cursor.fetchone()
    cursor.close()
    
    return render_template('edit.html', record=record)

@threatenedSpecies_bp.route('/threatenedSpecies/delete/<int:record_id>', methods=['POST'])
@login_required
def delete_record(record_id):
    cursor = connection.cursor()
    sql = "DELETE FROM threatenedSpecies WHERE id = %s"
    cursor.execute(sql, (record_id,))
    connection.commit()
    cursor.close()
    
    return redirect('/threatenedSpecies')