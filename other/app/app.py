from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])

def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return redirect(url_for('index'))
    
    return render_template('login.html')



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/co2-emissions')
def co2_emissions():
    return render_template('co2_emissions.html')

@app.route('/development-aid')
def tourism():
    return render_template('development_aid.html')

@app.route('/exchange-rates')
def tourism():
    return render_template('exchange_rates.html')

@app.route('/expenditure-health')
def tourism():
    return render_template('expenditure_health.html')

@app.route('/imports-exports')
def tourism():
    return render_template('imports_exports.html')

@app.route('/internet-usage')
def tourism():
    return render_template('internet_usage.html')

@app.route('/threatened-species')
def tourism():
    return render_template('threatened_species.html')

@app.route('/tourism')
def tourism():
    return render_template('tourism.html')



if __name__ == '__main__':
    app.run(debug=True)
