from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from database import connection

aid_bp = Blueprint('aid', __name__)

def get_aid_details():
    cursor = connection.cursor(dictionary=True)
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

@aid_bp.route('/aid')
@login_required
def page1():
    aid_details = get_aid_details()
    return render_template('aid.html', details=aid_details, is_admin=(current_user.id == "admin"))

@aid_bp.route('/aid/add', methods=['GET', 'POST'])
@login_required
def add_record():
    if current_user.id != "admin":
        return redirect('/aid')

    if request.method == 'POST':
        country_code = request.form['country_code']
        series_id = request.form['series_id']
        value = request.form['value']
        record_year = request.form['record_year']
        source_id = request.form['source_id']
        
        cursor = connection.cursor()
        sql = """
            INSERT INTO aid (countryCode, seriesID, val, recordYear, sourceID)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (country_code, series_id, value, record_year, source_id))
        connection.commit()
        cursor.close()
        
        return redirect('/aid')
    
    return render_template('add.html')

@aid_bp.route('/aid/edit/<int:record_id>', methods=['GET', 'POST'])
@login_required
def edit_record(record_id):
    if current_user.id != "admin":
        return redirect('/aid')

    if request.method == 'POST':
        value = request.form['value']
        record_year = request.form['record_year']
        
        cursor = connection.cursor()
        sql = """
            UPDATE aid
            SET val = %s, recordYear = %s
            WHERE id = %s
        """
        cursor.execute(sql, (value, record_year, record_id))
        connection.commit()
        cursor.close()
        
        return redirect('/aid')
    
    cursor = connection.cursor(dictionary=True)
    sql = "SELECT * FROM aid WHERE id = %s"
    cursor.execute(sql, (record_id,))
    record = cursor.fetchone()
    cursor.close()
    
    return render_template('edit.html', record=record)

@aid_bp.route('/aid/delete/<int:record_id>', methods=['POST'])
@login_required
def delete_record(record_id):
    if current_user.id != "admin":
        return redirect('/aid')

    cursor = connection.cursor()
    sql = "DELETE FROM aid WHERE id = %s"
    cursor.execute(sql, (record_id,))
    connection.commit()
    cursor.close()

    return redirect('/aid')
