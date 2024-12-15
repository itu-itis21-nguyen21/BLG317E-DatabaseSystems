from flask import Blueprint, render_template, request, redirect, session
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
    session['current_page'] = 1
    
    aid_details = get_aid_details()
    return render_template('aid.html', details=aid_details)

@aid_bp.route('/aid/add', methods=['GET', 'POST'])
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
    cursor = connection.cursor()
    sql = "DELETE FROM aid WHERE id = %s"
    cursor.execute(sql, (record_id,))
    connection.commit()
    cursor.close()

    return redirect('/aid')

@aid_bp.route('/aid/search', methods=['GET'])
@login_required
def search_by_country_and_series():
    country_name = request.args.get('country_name', '').strip()
    series_name = request.args.get('series_name', '').strip()
    
    # Build the query dynamically based on provided filters
    filters = []
    query = """
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
    return render_template('aid.html', details=results)

@aid_bp.route('/aid/next', methods=['POST'])
def next_record():
    cursor = connection.cursor(dictionary=True)
    # Example of incrementing the offset (assuming you store current page in session)
    current_page = session.get('current_page', 1) + 1
    offset = (current_page - 1) * 20
    sql = f"""
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
        LIMIT 20 OFFSET {offset};
    """
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    
    # Update the session page count
    session['current_page'] = current_page
    return render_template('aid.html', details=results)


@aid_bp.route('/aid/previous', methods=['POST'])
def previous_record():
    cursor = connection.cursor(dictionary=True)
    current_page = session.get('current_page', 1)

    # Ensure we don't go below page 1
    if current_page > 1:
        current_page -= 1

    offset = (current_page - 1) * 20
    sql = f"""
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
        LIMIT 20 OFFSET {offset};
    """
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()

    # Update the session page count
    session['current_page'] = current_page
    return render_template('aid.html', details=results)