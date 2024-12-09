from flask import Flask, render_template # type: ignore
from pages.trade import trade_bp  # Import the trade Blueprint
from pages.aid import aid_bp
from pages.exchangeRates import exchangeRates_bp
from pages.tourism import tourism_bp
from pages.carbondioxide import carbondioxide_bp
from pages.threatenedSpecies import threatenedSpecies_bp

app = Flask(__name__)

# Register the Blueprints
app.register_blueprint(trade_bp)
app.register_blueprint(aid_bp)
app.register_blueprint(exchangeRates_bp)
app.register_blueprint(tourism_bp)
app.register_blueprint(carbondioxide_bp)
app.register_blueprint(threatenedSpecies_bp)

@app.route('/')
def main_page():
    return render_template('main.html')


if __name__ == '__main__':
    app.run(debug=True)
