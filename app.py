"""Flask application entry point for Crypto Investigation Toolkit"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    """Homepage with tool overview and categories"""
    return render_template('index.html')


# Placeholder routes for future tools (will be replaced by Blueprints)
@app.route('/tron/suspicious-analyzer')
def tron_suspicious_analyzer():
    """TRON suspicious feature analysis tool (placeholder)"""
    return render_template('tron/suspicious_analyzer.html')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)