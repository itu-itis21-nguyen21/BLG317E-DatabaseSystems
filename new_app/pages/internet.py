from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
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
@login_required
def page1():
    internet_details = get_internet_details()
    return render_template('internet.html', details=internet_details, is_admin=(current_user.id == "admin"))

@internet_bp.route('/internet/add', methods=['GET', 'POST'])
@login_required
def add_record():
    if current_user.id != "admin":
        return redirect('/internet')
    
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

        # Insert into the internet table
        sql = """
            INSERT INTO internet (countryCode, seriesID, val, recordYear, sourceID)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (country_code, series_id, value, record_year, source_id))
        connection.commit()
        cursor.close()

        return redirect('/internet')
    
    # Fetch country names only (not tuples)
    cursor.execute("SELECT country FROM countries ORDER BY country")
    countries = [row[0] for row in cursor.fetchall()]  # Extract the first element of each tuple

    cursor.execute("SELECT DISTINCT series FROM series INNER JOIN internet ON series.seriesID = internet.seriesID")
    series = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT source FROM sources INNER JOIN internet ON sources.sourceID = internet.sourceID")
    sources = [row[0] for row in cursor.fetchall()]

    cursor.close()

    return render_template('add.html', countries=countries, series=series, sources=sources)

@internet_bp.route('/internet/edit/<int:record_id>', methods=['GET', 'POST'])
@login_required
def edit_record(record_id):
    if current_user.id != "admin":
        return redirect('/internet')
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
@login_required
def delete_record(record_id):
    if current_user.id != "admin":
        return redirect('/internet')
    cursor = connection.cursor()
    sql = "DELETE FROM internet WHERE id = %s"
    cursor.execute(sql, (record_id,))
    connection.commit()
    cursor.close()
    
    return redirect('/internet')

@internet_bp.route('/internet/search', methods=['GET'])
@login_required
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
