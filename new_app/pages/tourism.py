from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from database import connection

tourism_bp = Blueprint('tourism', __name__)

def get_tourism_details():
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
    cursor.execute(sql_string)
    result = cursor.fetchall()
    cursor.close()
    return result

@tourism_bp.route('/tourism')
@login_required
def page1():
    tourism_details = get_tourism_details()
    return render_template('tourism.html', details=tourism_details)

@tourism_bp.route('/tourism/add', methods=['GET', 'POST'])
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
            INSERT INTO tourism (countryCode, seriesID, val, recordYear, sourceID)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (country_code, series_id, value, record_year, source_id))
        connection.commit()
        cursor.close()
        
        return redirect('/tourism')
    
    return render_template('add.html')

@tourism_bp.route('/tourism/edit/<int:record_id>', methods=['GET', 'POST'])
@login_required
def edit_record(record_id):
    if request.method == 'POST':
        # Retrieve updated data
        value = request.form['value']
        record_year = request.form['record_year']
        
        # Update the database
        cursor = connection.cursor()
        sql = """
            UPDATE tourism
            SET val = %s, recordYear = %s
            WHERE id = %s
        """
        cursor.execute(sql, (value, record_year, record_id))
        connection.commit()
        cursor.close()
        
        return redirect('/tourism')
    
    # Fetch existing data for the record
    cursor = connection.cursor(dictionary=True)
    sql = "SELECT * FROM tourism WHERE id = %s"
    cursor.execute(sql, (record_id,))
    record = cursor.fetchone()
    cursor.close()
    
    return render_template('edit.html', record=record)

@tourism_bp.route('/tourism/delete/<int:record_id>', methods=['POST'])
@login_required
def delete_record(record_id):
    cursor = connection.cursor()
    sql = "DELETE FROM tourism WHERE id = %s"
    cursor.execute(sql, (record_id,))
    connection.commit()
    cursor.close()
    
    return redirect('/tourism')