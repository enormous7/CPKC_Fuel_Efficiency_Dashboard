import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib # To save/load model
import os

def train_fuel_model(data_path, model_output_path):
    """
    Loads the simulated fuel data, trains a RandomForestRegressor model,
    and saves the trained model.
    """
    print("Loading data for model training...")
    try:
        df = pd.read_csv(data_path)
        print(f"Data loaded. Shape: {df.shape}")
    except FileNotFoundError:
        print(f"Error: Data file '{data_path}' not found. Please run data_generator.py first.")
        return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

    # Define features (X) and target (y)
    features = ['Distance_km', 'Avg_Speed_kmh', 'Train_Weight_tons', 'Weather_Condition']
    target = 'Fuel_Consumed_liters'

    X = df[features]
    y = df[target]

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training RandomForestRegressor model...")
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    print("Model training complete.")

    # Evaluate the model
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Model Evaluation (on test set):")
    print(f"  Mean Absolute Error (MAE): {mae:.2f} liters")
    print(f"  R-squared (R2): {r2:.2f}")

    # Save the trained model
    os.makedirs(os.path.dirname(model_output_path), exist_ok=True)
    joblib.dump(model, model_output_path)
    print(f"Trained model saved to: {model_output_path}")
    return model

if __name__ == "__main__":
    data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'cpkc_train_fuel_data.csv')
    model_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'fuel_model.pkl')

    # Ensure data file exists before training
    if not os.path.exists(data_file):
        print("Data file not found. Generating data first...")
        from data_generator import generate_fuel_data
        df_generated = generate_fuel_data(5000)
        df_generated.to_csv(data_file, index=False)
        print(f"Data generated and saved to {data_file}")

    train_fuel_model(data_file, model_file)