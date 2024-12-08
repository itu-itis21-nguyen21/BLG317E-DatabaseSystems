from flask import Flask, render_template
from trade import trade_bp  # Import the trade Blueprint
from aid import aid_bp
from exchangeRates import exchangeRates_bp

app = Flask(__name__)

# Register the Blueprints
app.register_blueprint(trade_bp)
app.register_blueprint(aid_bp)
app.register_blueprint(exchangeRates_bp)

@app.route('/')
def main_page():
    return render_template('main.html')


if __name__ == '__main__':
    app.run(debug=True)
