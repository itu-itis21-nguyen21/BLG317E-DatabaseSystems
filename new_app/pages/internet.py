from flask import Blueprint, render_template, request, redirect
from database import connection

internet_bp = Blueprint('internet', __name__)

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

@internet_bp.route('/internet')
def page1():
    internet_details = get_internet_details()
    return render_template('internet.html', details=internet_details)

@internet_bp.route('/internet/add', methods=['GET', 'POST'])
def add_record():
    if request.method == 'POST':
        country_code = request.form['country_code']
        series_id = request.form['series_id']
        value = request.form['value']
        record_year = request.form['record_year']
        source_id = request.form['source_id']
        
        cursor = connection.cursor()
        sql = """
            INSERT INTO internet (countryCode, seriesID, val, recordYear, sourceID)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (country_code, series_id, value, record_year, source_id))
        connection.commit()
        cursor.close()
        
        return redirect('/internet')
    
    return render_template('add.html')

@internet_bp.route('/internet/edit/<int:record_id>', methods=['GET', 'POST'])
def edit_record(record_id):
    if request.method == 'POST':
        value = request.form['value']
        record_year = request.form['record_year']
        
        cursor = connection.cursor()
        sql = """
            UPDATE internet
            SET val = %s, recordYear = %s
            WHERE id = %s
        """
        cursor.execute(sql, (value, record_year, record_id))
        connection.commit()
        cursor.close()
        
        return redirect('/internet')
    
    cursor = connection.cursor(dictionary=True)
    sql = "SELECT * FROM internet WHERE id = %s"
    cursor.execute(sql, (record_id,))
    record = cursor.fetchone()
    cursor.close()
    
    return render_template('edit.html', record=record)

@internet_bp.route('/internet/delete/<int:record_id>', methods=['POST'])
def delete_record(record_id):
    cursor = connection.cursor()
    sql = "DELETE FROM internet WHERE id = %s"
    cursor.execute(sql, (record_id,))
    connection.commit()
    cursor.close()
    
    return redirect('/internet')

@internet_bp.route('/internet/search', methods=['GET'])
def search_by_country_and_series():
    country_name = request.args.get('country_name', '').strip()
    series_name = request.args.get('series_name', '').strip()
    
    # Build the query dynamically based on provided filters
    filters = []
    query = """
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
    """
    
    if country_name:
        filters.append("countries.country LIKE %s")
    if series_name:
        filters.append("series.series = %s")
    
    if filters:
        query += " WHERE " + " AND ".join(filters)
    
    query += " ORDER BY id ASC"
    
    # Execute the query with dynamic filters
    params = []
    if country_name:
        params.append(f"%{country_name}%")
    if series_name:
        params.append(series_name)
    
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, tuple(params))
    results = cursor.fetchall()
    cursor.close()
    
    # Render the filtered results
    return render_template('internet.html', details=results)
