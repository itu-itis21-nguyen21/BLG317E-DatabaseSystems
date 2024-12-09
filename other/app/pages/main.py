from flask import Flask, render_template
from app.pages.tourism import tourism_bp  # Import the tourism Blueprint
from app.pages.trade import trade_bp  # Import the trade Blueprint

app = Flask(__name__)

# Register the Blueprints
app.register_blueprint(tourism_bp)
app.register_blueprint(trade_bp)

@app.route('/')
def main_page():
    return render_template('main.html')

@app.route('/page2')
def page2():
    return render_template('page2.html')

@app.route('/page3')
def page3():
    return render_template('page3.html')

if __name__ == '__main__':
    app.run(debug=True)
