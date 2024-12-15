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
    return render_template('tourism.html', details=tourism_details, is_admin=(current_user.id == "admin"))

@tourism_bp.route('/tourism/add', methods=['GET', 'POST'])
@login_required
def add_record():
    if current_user.id != "admin":
        return redirect('/tourism')
    
    cursor = connection.cursor()

    if request.method == 'POST':
        # Retrieve form data
        country_name = request.form['country_name']
        series = request.form['series']
        value = request.form['value']
        record_year = request.form['record_year']
        source = request.form['source']

        # Get the corresponding country code from the database
        cursor.execute("SELECT countryCode FROM countries WHERE country = %s", (country_name,))
        result = cursor.fetchone()
        if not result:
            cursor.close()
            return "Error: Selected country does not exist in the database.", 400
        country_code = result[0]
        
        cursor.execute("SELECT seriesID FROM series WHERE series = %s", (series,))
        result = cursor.fetchone()
        if not result:
            cursor.close()
            return "Error: Selected series does not exist in the database.", 400
        series_id = result[0]

        cursor.execute("SELECT sourceID FROM sources WHERE source = %s", (source,))
        result = cursor.fetchone()
        if not result:
            cursor.close()
            return "Error: Selected source does not exist in the database.", 400
        source_id = result[0]

        # Insert into the tourism table
        sql = """
            INSERT INTO tourism (countryCode, seriesID, val, recordYear, sourceID)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (country_code, series_id, value, record_year, source_id))
        connection.commit()
        cursor.close()

        return redirect('/tourism')
    
    # Fetch country names only (not tuples)
    cursor.execute("SELECT country FROM countries ORDER BY country")
    countries = [row[0] for row in cursor.fetchall()]  # Extract the first element of each tuple

    cursor.execute("SELECT DISTINCT series FROM series INNER JOIN tourism ON series.seriesID = tourism.seriesID")
    series = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT source FROM sources INNER JOIN tourism ON sources.sourceID = tourism.sourceID")
    sources = [row[0] for row in cursor.fetchall()]

    cursor.close()

    return render_template('add.html', countries=countries, series=series, sources=sources)

@tourism_bp.route('/tourism/edit/<int:record_id>', methods=['GET', 'POST'])
@login_required
def edit_record(record_id):
    if current_user.id != "admin":
        return redirect('/tourism')
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
    if current_user.id != "admin":
        return redirect('/tourism')
    cursor = connection.cursor()
    sql = "DELETE FROM tourism WHERE id = %s"
    cursor.execute(sql, (record_id,))
    connection.commit()
    cursor.close()
    
    return redirect('/tourism')

@tourism_bp.route('/tourism/search', methods=['GET'])
@login_required
def search_by_country_and_series():
    country_name = request.args.get('country_name', '').strip()
    series_name = request.args.get('series_name', '').strip()
    
    # Build the query dynamically based on provided filters
    filters = []
    query = """
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
    return render_template('tourism.html', details=results)