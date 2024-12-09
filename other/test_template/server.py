from flask import Flask, render_template, request, redirect
from database import connection
import mysql.connector

app = Flask(__name__)

def get_tourism_details():
    cursor = connection.cursor(dictionary=True)
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
    result = cursor.fetchall()  # Fetch all rows, not just one
    cursor.close()
    return result

@app.route('/')
def main_page():
    return render_template('main.html')

@app.route('/tourism')
def page1():
    tourism_details = get_tourism_details()
    return render_template('tourism.html', details=tourism_details)

@app.route('/tourism/add', methods=['GET', 'POST'])
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
    
    return render_template('add.html')  # Create a form in `add.html`

@app.route('/tourism/edit/<int:record_id>', methods=['GET', 'POST'])
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
    
    return render_template('edit.html', record=record)  # Create an `edit.html` form

@app.route('/tourism/delete/<int:record_id>', methods=['POST'])
def delete_record(record_id):
    # Delete the record from the database
    cursor = connection.cursor()
    sql = "DELETE FROM tourism WHERE id = %s"
    cursor.execute(sql, (record_id,))
    connection.commit()
    cursor.close()
    
    return redirect('/tourism')

@app.route('/page2')
def page2():
    return render_template('page2.html')

@app.route('/page3')
def page3():
    return render_template('page3.html')

if __name__ == '__main__':
    app.run(debug=True)
