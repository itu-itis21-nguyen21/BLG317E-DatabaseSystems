from flask import Blueprint, render_template, request, redirect
from database import connection

trade_bp = Blueprint('trade', __name__)

def get_trade_details():
    cursor = connection.cursor(dictionary=True)
    #show: id, countryName, recordYear, Series,series unit, val, source
    sql_string = """
        SELECT
            trade.id AS id,
            countries.country AS country_name,
            series.series AS series,
            trade.val AS value,
            series.unit AS unit,
            trade.recordYear AS record_year,
            sources.source AS source

        FROM trade 
        JOIN countries ON trade.countryCode = countries.countryCode
        JOIN series ON trade.seriesID = series.seriesID
        JOIN sources ON trade.sourceID = sources.sourceID

        ORDER BY id ASC
        LIMIT 20;

    """
    cursor.execute(sql_string)
    result = cursor.fetchall()
    cursor.close()
    return result

@trade_bp.route('/trade')
def page1():
    trade_details = get_trade_details()
    return render_template('trade.html', details=trade_details)

@trade_bp.route('/trade/add', methods=['GET', 'POST'])
def add_record():
    if request.method == 'POST':
        country_code = request.form['country_code']
        series_id = request.form['series_id']
        value = request.form['value']
        record_year = request.form['record_year']
        source_id = request.form['source_id']
        
        cursor = connection.cursor()
        sql = """
            INSERT INTO trade (countryCode, seriesID, val, recordYear, sourceID)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (country_code, series_id, value, record_year, source_id))
        connection.commit()
        cursor.close()
        
        return redirect('/trade')
    
    return render_template('add.html')

@trade_bp.route('/trade/edit/<int:record_id>', methods=['GET', 'POST'])
def edit_record(record_id):
    if request.method == 'POST':
        value = request.form['value']
        record_year = request.form['record_year']
        
        cursor = connection.cursor()
        sql = """
            UPDATE trade
            SET val = %s, recordYear = %s
            WHERE id = %s
        """
        cursor.execute(sql, (value, record_year, record_id))
        connection.commit()
        cursor.close()
        
        return redirect('/trade')
    
    cursor = connection.cursor(dictionary=True)
    sql = "SELECT * FROM trade WHERE id = %s"
    cursor.execute(sql, (record_id,))
    record = cursor.fetchone()
    cursor.close()
    
    return render_template('edit.html', record=record)

@trade_bp.route('/trade/delete/<int:record_id>', methods=['POST'])
def delete_record(record_id):
    cursor = connection.cursor()
    sql = "DELETE FROM trade WHERE id = %s"
    cursor.execute(sql, (record_id,))
    connection.commit()
    cursor.close()
    
    return redirect('/trade')