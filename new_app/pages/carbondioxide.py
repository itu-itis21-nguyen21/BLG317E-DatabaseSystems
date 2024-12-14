from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from database import connection

carbondioxide_bp = Blueprint('carbondioxide', __name__)

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

@carbondioxide_bp.route('/carbondioxide')
@login_required
def page1():
    carbondioxide_details = get_carbondioxide_details()
    return render_template('carbondioxide.html', details=carbondioxide_details)

@carbondioxide_bp.route('/carbondioxide/add', methods=['GET', 'POST'])
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
            INSERT INTO carbondioxide (countryCode, seriesID, val, recordYear, sourceID)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (country_code, series_id, value, record_year, source_id))
        connection.commit()
        cursor.close()
        
        return redirect('/carbondioxide')
    
    return render_template('add.html')

@carbondioxide_bp.route('/carbondioxide/edit/<int:record_id>', methods=['GET', 'POST'])
@login_required
def edit_record(record_id):
    if request.method == 'POST':
        # Retrieve updated data
        value = request.form['value']
        record_year = request.form['record_year']
        
        # Update the database
        cursor = connection.cursor()
        sql = """
            UPDATE carbondioxide
            SET val = %s, recordYear = %s
            WHERE id = %s
        """
        cursor.execute(sql, (value, record_year, record_id))
        connection.commit()
        cursor.close()
        
        return redirect('/carbondioxide')
    
    # Fetch existing data for the record
    cursor = connection.cursor(dictionary=True)
    sql = "SELECT * FROM carbondioxide WHERE id = %s"
    cursor.execute(sql, (record_id,))
    record = cursor.fetchone()
    cursor.close()
    
    return render_template('edit.html', record=record)

@carbondioxide_bp.route('/carbondioxide/delete/<int:record_id>', methods=['POST'])
@login_required
def delete_record(record_id):
    cursor = connection.cursor()
    sql = "DELETE FROM carbondioxide WHERE id = %s"
    cursor.execute(sql, (record_id,))
    connection.commit()
    cursor.close()
    
    return redirect('/carbondioxide')