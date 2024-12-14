from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from database import connection

exchangeRates_bp = Blueprint('exchangeRates', __name__)

def get_exchangeRates_details():
    cursor = connection.cursor(dictionary=True)
    #show: id, countryName, recordYear, Series,series unit, val, source
    sql_string = """
        SELECT
            exchangeRates.id AS id,
            countries.country AS country_name,
            series.series AS series,
            exchangeRates.currency AS currency,
            exchangeRates.val AS value,
            series.unit AS unit,
            exchangeRates.recordYear AS record_year,
            sources.source AS source

        FROM exchangeRates 
        JOIN countries ON exchangeRates.countryCode = countries.countryCode
        JOIN series ON exchangeRates.seriesID = series.seriesID
        JOIN sources ON exchangeRates.sourceID = sources.sourceID

        ORDER BY id ASC
        LIMIT 20;

    """
    cursor.execute(sql_string)
    result = cursor.fetchall()
    cursor.close()
    return result

@exchangeRates_bp.route('/exchangeRates')
@login_required
def page1():
    exchangeRates_details = get_exchangeRates_details()
    return render_template('exchangeRates.html', details=exchangeRates_details)

@exchangeRates_bp.route('/exchangeRates/add', methods=['GET', 'POST'])
@login_required
def add_record():
    if request.method == 'POST':
        country_code = request.form['country_code']
        series_id = request.form['series_id']
        value = request.form['value']
        record_year = request.form['record_year']
        source_id = request.form['source_id']
        
        cursor = connection.cursor()
        sql = """
            INSERT INTO exchangeRates (countryCode, seriesID, val, recordYear, sourceID)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (country_code, series_id, value, record_year, source_id))
        connection.commit()
        cursor.close()
        
        return redirect('/exchangeRates')
    
    return render_template('add.html')

@exchangeRates_bp.route('/exchangeRates/edit/<int:record_id>', methods=['GET', 'POST'])
@login_required
def edit_record(record_id):
    if request.method == 'POST':
        value = request.form['value']
        record_year = request.form['record_year']
        
        cursor = connection.cursor()
        sql = """
            UPDATE exchangeRates
            SET val = %s, recordYear = %s
            WHERE id = %s
        """
        cursor.execute(sql, (value, record_year, record_id))
        connection.commit()
        cursor.close()
        
        return redirect('/exchangeRates')
    
    cursor = connection.cursor(dictionary=True)
    sql = "SELECT * FROM exchangeRates WHERE id = %s"
    cursor.execute(sql, (record_id,))
    record = cursor.fetchone()
    cursor.close()
    
    return render_template('edit.html', record=record)

@exchangeRates_bp.route('/exchangeRates/delete/<int:record_id>', methods=['POST'])
@login_required
def delete_record(record_id):
    cursor = connection.cursor()
    sql = "DELETE FROM exchangeRates WHERE id = %s"
    cursor.execute(sql, (record_id,))
    connection.commit()
    cursor.close()
    
    return redirect('/exchangeRates')