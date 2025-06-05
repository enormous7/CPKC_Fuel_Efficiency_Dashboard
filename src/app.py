from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import os
import random # For simulating recommendations
import json

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Load the trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'fuel_model.pkl')
model = None
try:
    model = joblib.load(MODEL_PATH)
    print("Fuel prediction model loaded successfully.")
except FileNotFoundError:
    print(f"Error: Model file '{MODEL_PATH}' not found. Please run model_trainer.py first.")
except Exception as e:
    print(f"Error loading model: {e}")

# Load simulated historical data for dashboard overview
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'cpkc_train_fuel_data.csv')
historical_df = None
try:
    historical_df = pd.read_csv(DATA_PATH)
    historical_df['Timestamp'] = pd.to_datetime(historical_df['Timestamp'])
    historical_df['Month'] = historical_df['Timestamp'].dt.to_period('M')
    print("Historical data loaded successfully.")
except FileNotFoundError:
    print(f"Error: Historical data file '{DATA_PATH}' not found. Please run data_generator.py first.")
except Exception as e:
    print(f"Error loading historical data: {e}")

@app.route('/')
def index():
    """Renders the main dashboard page."""

    total_fuel_consumed = 0
    avg_fuel_per_km = 0
    monthly_avg_fuel = []

    if historical_df is not None and not historical_df.empty:
        total_fuel_consumed = historical_df['Fuel_Consumed_liters'].sum()
        avg_fuel_per_km = historical_df['Fuel_Consumed_liters'].sum() / historical_df['Distance_km'].sum()

        # Calculate monthly average fuel consumption
        monthly_data = historical_df.groupby('Month')['Fuel_Consumed_liters'].sum().reset_index()
        monthly_data['Month'] = monthly_data['Month'].astype(str) # Convert Period to string for JSON
        monthly_avg_fuel = monthly_data.to_dict(orient='records')

    return render_template('index.html',
                           total_fuel_consumed=f"{total_fuel_consumed:,.0f}",
                           avg_fuel_per_km=f"{avg_fuel_per_km:.2f}",
                           monthly_avg_fuel_json=json.dumps(monthly_avg_fuel))

@app.route('/predict_fuel', methods=['POST'])
def predict_fuel():
    """Predicts fuel consumption based on input parameters."""
    if model is None:
        return jsonify({"error": "Model not loaded. Please train the model first."}), 500

    try:
        data = request.json
        distance_km = float(data.get('distance_km'))
        avg_speed_kmh = float(data.get('avg_speed_kmh'))
        train_weight_tons = float(data.get('train_weight_tons'))
        weather_condition = int(data.get('weather_condition')) # 0, 1, 2

        input_data = pd.DataFrame([[distance_km, avg_speed_kmh, train_weight_tons, weather_condition]],
                                  columns=['Distance_km', 'Avg_Speed_kmh', 'Train_Weight_tons', 'Weather_Condition'])

        predicted_fuel = model.predict(input_data)[0]

        # Simulate optimized fuel consumption for comparison (e.g., 5-15% reduction)
        optimized_fuel = predicted_fuel * random.uniform(0.85, 0.95)
        potential_savings = predicted_fuel - optimized_fuel

        # Simulate recommendations
        recommendations = []
        if avg_speed_kmh > 75:
            recommendations.append("Consider slightly reducing average speed for optimal fuel efficiency.")
        if train_weight_tons > 10000:
            recommendations.append("High train weight. Ensure efficient loading and consider splitting heavy loads.")
        if weather_condition == 2:
            recommendations.append("Heavy wind conditions impact fuel. Adjust speed and consider route alternatives if possible.")
        if not recommendations:
            recommendations.append("Current parameters are generally efficient. Continue monitoring!")

        return jsonify({
            "predicted_fuel": f"{predicted_fuel:.2f}",
            "optimized_fuel": f"{optimized_fuel:.2f}",
            "potential_savings": f"{potential_savings:.2f}",
            "recommendations": recommendations
        })
    except ValueError as e:
        return jsonify({"error": f"Invalid input: {e}. Please check your numerical values."}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

if __name__ == '__main__':
    # Check if data and model exist, guide user if not
    if not os.path.exists(DATA_PATH):
        print(f"\n[!] WARNING: Historical data file '{DATA_PATH}' not found.")
        print("    Please run 'python src/data_generator.py' first to create it.")
    if not os.path.exists(MODEL_PATH):
        print(f"\n[!] WARNING: Model file '{MODEL_PATH}' not found.")
        print("    Please run 'python src/model_trainer.py' first to train the model.")

    print("\nStarting CPKC Fuel Efficiency Dashboard...")
    app.run(debug=True, host='0.0.0.0', port=5000) # debug=True for development, False for production