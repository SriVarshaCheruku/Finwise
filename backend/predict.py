import numpy as np
import pandas as pd
import yfinance as yf
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from datetime import datetime, timedelta
from statsmodels.tsa.arima.model import ARIMA
import json
from flask import jsonify
from sklearn.metrics import mean_squared_error

def predict_stock(ticker, days_ahead=5):
    if days_ahead > 10:
        return {"success": False, "error": "Days must be 10 or less."}

    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=3*365)).strftime('%Y-%m-%d')
    
    try:
        data = yf.download(ticker, start=start_date, end=end_date)[['Close']]
        data.dropna(inplace=True)
    except Exception as e:
        return {"success": False, "error": f"Stock data error: {str(e)}"}

    # Train ARIMA Model
    arima_model = ARIMA(data['Close'], order=(5, 1, 0))
    arima_fitted = arima_model.fit()
    data['ARIMA_Pred'] = arima_fitted.fittedvalues

    # Normalize Data
    scaler = MinMaxScaler()
    data[['Scaled_Close', 'Scaled_ARIMA']] = scaler.fit_transform(data[['Close', 'ARIMA_Pred']])

    def create_sequences(data, time_step=60):
        X, Y = [], []
        for i in range(len(data) - time_step - 1):
            X.append(data[i:(i + time_step)])
            Y.append(data[i + time_step])
        return np.array(X), np.array(Y)

    # Prepare LSTM data
    time_step = 120
    features = data[['Scaled_Close', 'Scaled_ARIMA']].values
    X, Y = create_sequences(features, time_step)
    X = X.reshape(X.shape[0], X.shape[1], 2)

    train_size = int(len(X) * 0.8)
    X_train, Y_train = X[:train_size], Y[:train_size]
    X_test, Y_test = X[train_size:], Y[train_size:]

    # Build & Train LSTM Model
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(time_step, 2)),
        Dropout(0.2),
        LSTM(50, return_sequences=False),
        Dropout(0.2),
        Dense(30, activation='relu'),
        Dense(2)
    ])
    
    model.compile(optimizer=tf.keras.optimizers.RMSprop(learning_rate=0.005), loss="mean_squared_error")
    model.fit(X_train, Y_train, epochs=30, batch_size=32, verbose=1)

    # Get model predictions on test data
    Y_test_pred = model.predict(X_test)

    # Convert back to original scale
    Y_test_actual = scaler.inverse_transform(np.column_stack((Y_test[:, 0], np.zeros(Y_test.shape[0]))))[:, 0]
    Y_test_pred_actual = scaler.inverse_transform(np.column_stack((Y_test_pred[:, 0], np.zeros(Y_test.shape[0]))))[:, 0]

    # Compute standard deviation from residuals
    std_dev = np.std(Y_test_actual - Y_test_pred_actual)

    # Generate Future Predictions
    predictions = {}
    last_sequence = features[-time_step:].reshape(1, time_step, 2)
    future_dates = [(datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, days_ahead + 1)]

    for date in future_dates:
        lstm_pred_scaled = model.predict(last_sequence)
        lstm_pred = scaler.inverse_transform(np.array([[lstm_pred_scaled[0, 0], 0]]))[0, 0]
    
        low = round(float(lstm_pred) - float(std_dev), 2)
        high = round(float(lstm_pred) + float(std_dev), 2)
    
        predictions[date] = {
            "low": low,
            "predicted": round(float(lstm_pred), 2),
            "high": high
        }
    
        # Prepare next input
        lstm_pred_reshaped = scaler.transform(np.array([[lstm_pred, 0]]))
        last_sequence = np.append(last_sequence[:, 1:, :], lstm_pred_reshaped.reshape(1, 1, 2), axis=1)
    
        # Debugging
        print("DEBUG: lstm_pred ->", lstm_pred, "Type ->", type(lstm_pred))
        print("DEBUG: std_dev ->", std_dev, "Type ->", type(std_dev))
    
    # Convert predictions to native Python float
    predictions_str = {str(date): {"low": val["low"], "predicted": val["predicted"], "high": val["high"]} for date, val in predictions.items()}

    # Print predictions for debugging
    print(f"Predictions in JSON format: {predictions_str}")

    # Return the result directly as a JSON object using jsonify
    return jsonify({
        "success": True,
        "name": ticker.upper(),
        "predictedPrices": predictions_str  # Return the dictionary directly here
    })
