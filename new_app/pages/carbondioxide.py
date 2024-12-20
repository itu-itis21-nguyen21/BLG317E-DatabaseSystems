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
    return render_template('carbondioxide.html', details=carbondioxide_details, is_admin=(current_user.id == "admin"))

@carbondioxide_bp.route('/carbondioxide/add', methods=['GET', 'POST'])
@login_required
def add_record():
    if current_user.id != "admin":
        return redirect('/carbondioxide')
    
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

        # Insert into the carbondioxide table
        sql = """
            INSERT INTO carbondioxide (countryCode, seriesID, val, recordYear, sourceID)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (country_code, series_id, value, record_year, source_id))
        connection.commit()
        cursor.close()

        return redirect('/carbondioxide')
    
    # Fetch country names only (not tuples)
    cursor.execute("SELECT country FROM countries ORDER BY country")
    countries = [row[0] for row in cursor.fetchall()]  # Extract the first element of each tuple

    cursor.execute("SELECT DISTINCT series FROM series INNER JOIN carbondioxide ON series.seriesID = carbondioxide.seriesID")
    series = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT source FROM sources INNER JOIN carbondioxide ON sources.sourceID = carbondioxide.sourceID")
    sources = [row[0] for row in cursor.fetchall()]

    cursor.close()

    return render_template('add.html', countries=countries, series=series, sources=sources)

@carbondioxide_bp.route('/carbondioxide/edit/<int:record_id>', methods=['GET', 'POST'])
@login_required
def edit_record(record_id):
    if current_user.id != "admin":
        return redirect('/carbondioxide')
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
    if current_user.id != "admin":
        return redirect('/carbondioxide')
    cursor = connection.cursor()
    sql = "DELETE FROM carbondioxide WHERE id = %s"
    cursor.execute(sql, (record_id,))
    connection.commit()
    cursor.close()
    
    return redirect('/carbondioxide')

@carbondioxide_bp.route('/carbondioxide/search', methods=['GET'])
@login_required
def search_by_country_and_series():
    country_name = request.args.get('country_name', '').strip()
    series_name = request.args.get('series_name', '').strip()
    
    # Build the query dynamically based on provided filters
    filters = []
    query = """
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
    return render_template('carbondioxide.html', details=results)