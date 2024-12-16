from flask import Flask, jsonify, render_template
from financial_data import FinancialDataProcessor
import plotly.graph_objects as go
import plotly.utils
import numpy as np
import json

app = Flask(__name__)
data_processor = FinancialDataProcessor()

# Initialize flag
_initialization_complete = False

@app.before_request
def initialize():
    global _initialization_complete
    if not _initialization_complete:
        data_processor.load_data()
        _initialization_complete = True

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/api/financial/profit-loss')
def get_profit_loss():
    data = data_processor.process_profit_loss()
    return jsonify(data)

@app.route('/api/financial/cash-flow')
def get_cash_flow():
    data = data_processor.process_cash_flow()
    return jsonify(data)

@app.route('/api/financial/working-capital')
def get_working_capital():
    data = data_processor.process_working_capital()
    return jsonify(data)

@app.route('/api/financial/monthly-trends')
def get_monthly_trends():
    data = data_processor.get_monthly_trends()
    return jsonify(data)

@app.route('/api/financial/ratios')
def get_ratios():
    # Define the data for ratios
    categories = ["Quick Ratio", "Current Ratio", "Cash Flow Ratio", "Debt-to-Equity Ratio"]
    msme_ratios = [0.9, 1.8, 0.7, 1.5]
    benchmark_ratios = [1.2, 2.0, 1.0, 1.0]

    # Return data in JSON format
    return jsonify({
        "categories": categories,
        "msme_ratios": msme_ratios,
        "benchmark_ratios": benchmark_ratios
    })




time_periods = ['Q1', 'Q2', 'Q3', 'Q4']
company_ccc = [70, 75, 80, 72]
benchmark_ccc = [60, 65, 70, 68]


@app.route('/api/financial/cash-conversion-cycle')
def get_cash_conversion_cycle():
    # Data for the heatmap (2 rows: company CCC and benchmark CCC)
    data = np.array([company_ccc, benchmark_ccc])

    # Create the heatmap
    fig = go.Figure(data=go.Heatmap(
        z=data,  # 2D data array for CCC values
        x=time_periods,  # Time periods (x-axis)
        y=["Company's CCC", "Benchmark CCC"],  # Categories (y-axis)
        colorscale='Blues',  # Color scheme for the heatmap
        colorbar=dict(title="CCC Value"),  # Colorbar title
        showscale=True
    ))

    # Add title and labels
    fig.update_layout(
        title="Cash Conversion Cycle Comparison: Company vs. Benchmark",
        xaxis_title="Time Periods",
        yaxis_title="CCC Type",
    )

    # Convert figure to JSON
    heatmap_json = fig.to_json()

    return jsonify(heatmap_json)

if __name__ == '__main__':
    app.run(debug=True)

