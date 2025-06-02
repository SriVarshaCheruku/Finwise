from flask import Blueprint, request, jsonify
from backend.predict import predict_stock  # Import the predict_stock function from predict.py

# Create a Blueprint for prediction routes
predict_bp = Blueprint('predict_bp', __name__)

@predict_bp.route('/predict', methods=['POST'])
def predict():
    # Extract the ticker symbol and number of days from the request
    data = request.get_json()
    ticker = data.get('ticker')
    days_ahead = int(data.get('days', 5))  # Default to 5 days if not provided
    
    if not ticker:
        return jsonify({"success": False, "error": "Ticker symbol is required."})
    
    # Call the predict_stock function and get the result as a dictionary
    prediction_result = predict_stock(ticker, days_ahead)

    # Return the result as JSON
    return prediction_result  # Return the dictionary directly

