from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import os

app = Flask(__name__)

# Define the feature order (must match training order)
feature_order = [
    "industry",
    "revenue", 
    "market_position_score",
    "debt_equity_ratio", 
    "interest_coverage_ratio",
    "working_capital_days",
    "profit_margin",
    "liquidity_ratio",
    "management_quality_score", 
    "promoter_experience_years",
    "compliance_score",
    "loan_repayment_history_score",
    "banking_relationship_score",
    "financial_flexibility_score",
]

# Load the model
model_filename = os.path.join(os.path.dirname(__file__), "models", "xgboost_credit_model.pkl")
try:
    with open(model_filename, "rb") as model_file:
        model = pickle.load(model_file)
        # Add sklearn tags to model if missing
        if not hasattr(model, '_sklearn_version'):
            model._sklearn_version = '1.0'
except FileNotFoundError:
    raise FileNotFoundError(f"Model file {model_filename} not found. Please ensure it exists in the models directory")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_credit_score', methods=['POST'])
def predict_credit_score():
    try:
        # Get data from request
        data = request.json
        
        # Create a complete data dictionary with default values
        default_data = {
            "industry": "Technology",
            "revenue": 1000000,
            "market_position_score": 8.5,
            "debt_equity_ratio": 0.7,
            "interest_coverage_ratio": 3.2,
            "working_capital_days": 45,
            "profit_margin": 0.15,
            "liquidity_ratio": 1.5,
            "management_quality_score": 7.8,
            "promoter_experience_years": 10,
            "compliance_score": 9.0,
            "loan_repayment_history_score": 8.5,
            "banking_relationship_score": 7.0,
            "financial_flexibility_score": 8.0
        }

        # If data was provided, update default values with provided values
        if data:
            default_data.update(data)
        
        # Create DataFrame with proper column order
        input_df = pd.DataFrame([default_data])[feature_order]
        
        # Convert industry to string and other numeric fields to float
        input_df['industry'] = input_df['industry'].astype(str)
        numeric_columns = feature_order[1:]  # All columns except industry
        input_df[numeric_columns] = input_df[numeric_columns].astype(float)
        
        # Make prediction
        credit_score = model.predict(input_df)[0]
        
        # Determine RAG status
        if credit_score < 650:
            rag_status = "Red"
        elif credit_score < 750:
            rag_status = "Amber"
        else:
            rag_status = "Green"
            
        return jsonify({
            'credit_score': int(credit_score),
            'rag_status': rag_status
        })
        
    except Exception as e:
        return jsonify({'error': f'Error processing request: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(debug=True)