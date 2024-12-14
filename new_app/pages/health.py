from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from database import connection

health_bp = Blueprint('health', __name__)

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

@health_bp.route('/health')
@login_required
def page1():
    health_details = get_health_details()
    return render_template('health.html', details=health_details)

@health_bp.route('/health/add', methods=['GET', 'POST'])
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
            INSERT INTO health (countryCode, seriesID, val, recordYear, sourceID)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (country_code, series_id, value, record_year, source_id))
        connection.commit()
        cursor.close()
        
        return redirect('/health')
    
    return render_template('add.html')

@health_bp.route('/health/edit/<int:record_id>', methods=['GET', 'POST'])
@login_required
def edit_record(record_id):
    if request.method == 'POST':
        value = request.form['value']
        record_year = request.form['record_year']
        
        cursor = connection.cursor()
        sql = """
            UPDATE health
            SET val = %s, recordYear = %s
            WHERE id = %s
        """
        cursor.execute(sql, (value, record_year, record_id))
        connection.commit()
        cursor.close()
        
        return redirect('/health')
    
    cursor = connection.cursor(dictionary=True)
    sql = "SELECT * FROM health WHERE id = %s"
    cursor.execute(sql, (record_id,))
    record = cursor.fetchone()
    cursor.close()
    
    return render_template('edit.html', record=record)

@health_bp.route('/health/delete/<int:record_id>', methods=['POST'])
@login_required
def delete_record(record_id):
    cursor = connection.cursor()
    sql = "DELETE FROM health WHERE id = %s"
    cursor.execute(sql, (record_id,))
    connection.commit()
    cursor.close()
    
    return redirect('/health')

@health_bp.route('/health/search', methods=['GET'])
@login_required
def search_by_country_and_series():
    country_name = request.args.get('country_name', '').strip()
    series_name = request.args.get('series_name', '').strip()
    
    # Build the query dynamically based on provided filters
    filters = []
    query = """
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
    return render_template('health.html', details=results)