# CPKC_Fuel_Efficiency_Dashboard# CPKC Fuel Efficiency Dashboard: Optimizing Operations for Cost Savings

## Project Overview

For a large-scale railway company like **CPKC (Canadian Pacific Kansas City)**, fuel is one of the largest operating expenses. Even a small percentage of fuel savings can translate into millions of dollars in annual cost reductions. This project presents a **web-based dashboard** designed to predict train fuel consumption and provide optimization recommendations, directly contributing to significant operational cost savings.

This dashboard leverages simulated train operational data to:
1.  **Predict** fuel consumption based on various factors (distance, speed, weight, weather).
2.  **Simulate** potential fuel savings through optimized strategies.
3.  Provide **actionable recommendations** to train operators or dispatchers.
4.  **Visualize** historical fuel consumption trends for easy understanding.

This project demonstrates strong capabilities in **data science (predictive modeling), full-stack development (Flask web application), data visualization (Chart.js), and a clear understanding of business value creation (direct cost reduction)**. It's built to be accessible even to non-technical users, making data-driven decisions easy and intuitive.

![Project Screenshot](./images/screen.png)

## Key Features

* **Predictive Fuel Consumption Model**: A machine learning model (Random Forest Regressor) trained on simulated data to accurately predict fuel usage for a given train journey.
* **Interactive Web Dashboard (Flask)**: A user-friendly interface allowing users to input train parameters and instantly see predicted fuel consumption and potential savings.
* **Optimization Recommendations**: Provides practical suggestions to reduce fuel based on input conditions.
* **Historical Data Visualization (Chart.js)**: Displays monthly fuel consumption trends, offering insights into past performance and identifying areas for improvement.
* **Direct Cost Savings Focus**: Explicitly highlights potential fuel (and thus cost) savings, making the business impact clear.
* **Scalability**: The modular design allows for integration with real-time data sources and more complex optimization algorithms in the future.

## Project Structure

CPKC_Fuel_Efficiency_Dashboard/
├── src/
│   ├── app.py                  # Flask web application for the dashboard
│   ├── data_generator.py       # Script to generate simulated train fuel data
│   └── model_trainer.py        # Script to train and save the fuel prediction model
├── data/
│   ├── cpkc_train_fuel_data.csv# Simulated historical train operational data
│   └── fuel_model.pkl          # Trained machine learning model (saved)
├── templates/
│   └── index.html              # HTML template for the main dashboard page
├── static/
│   ├── css/
│   │   └── style.css           # CSS for styling the dashboard
│   └── js/
│       └── app.js              # JavaScript for chart rendering and API calls
├── reports/
│   └── (Optional: for additional reports or specific simulation outputs)
├── .gitignore                  # Specifies intentionally untracked files (e.g., generated data, virtual env)
├── requirements.txt            # Lists Python dependencies
└── README.md                   # Project description and instructions


## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

* **Python 3.x**: Download from [python.org](https://www.python.org/).
* **Git**: Download from [git-scm.com](https://git-scm.com/).
* **A GitHub Account**: For cloning this repository and showcasing your work.

### Installation and Execution

Follow these steps to set up and run the CPKC Fuel Efficiency Dashboard on your local machine:

1.  **Clone the Repository**:
    Open your terminal or command prompt, navigate to the directory where you want to store your project, and then clone this repository:
    ```bash
    git clone [https://github.com/enormous7/CPKC_Fuel_Efficiency_Dashboard.git](https://github.com/enormous7/CPKC_Fuel_Efficiency_Dashboard.git)
    cd CPKC_Fuel_Efficiency_Dashboard
    ```

2.  **Set Up a Virtual Environment (Highly Recommended)**:
    Create and activate a Python virtual environment to manage project dependencies cleanly:
    ```bash
    python3 -m venv venv
    # On Windows:
    # .\venv\Scripts\activate
    # On macOS/Linux:
    # source venv/bin/activate
    ```

3.  **Install Dependencies**:
    Install all required Python libraries specified in `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Generate Simulated Data**:
    The dashboard operates on simulated data. You need to generate this data first:
    ```bash
    python src/data_generator.py
    ```
    This command will create the `cpkc_train_fuel_data.csv` file in the `data/` directory. You will see output indicating data generation progress.

5.  **Train the Fuel Prediction Model**:
    Once the data is generated, train the machine learning model. This model will be used by the dashboard for predictions:
    ```bash
    python src/model_trainer.py
    ```
    This script will train a Random Forest Regressor and save the trained model as `fuel_model.pkl` in the `data/` directory. You will see model evaluation metrics printed to the console.

6.  **Run the Flask Web Application**:
    Start the Flask server to launch the web dashboard:
    ```bash
    python src/app.py
    ```
    The terminal will display a message indicating that the Flask development server is running, along with a URL (e.g., `http://127.0.0.1:5000/`).

7.  **Access the Dashboard**:
    Open your web browser and navigate to the URL provided in your terminal (e.g., `http://127.0.0.1:5000/`). You should now see the CPKC Fuel Efficiency Dashboard.

    * **Explore Historical Trends**: The top section and the chart will show historical fuel consumption insights.
    * **Predict & Optimize**: Use the "Predict Fuel Consumption & Get Recommendations" section to input hypothetical train parameters. Click "Predict Fuel & Optimize" to see predicted fuel usage, simulated optimized usage, potential savings, and relevant recommendations.

    To stop the Flask server, press `Ctrl+C` in your terminal.

## Data Schema (`cpkc_train_fuel_data.csv`)

The simulated data includes the following columns:

* `Timestamp`: Date and time of the train's operation.
* `Train_ID`: Unique identifier for the train.
* `Route`: The operational route (e.g., "Vancouver-Calgary").
* `Distance_km`: The distance covered by the train segment in kilometers.
* `Avg_Speed_kmh`: The average speed of the train during the segment in kilometers per hour.
* `Train_Weight_tons`: The total weight of the train (locomotives + cargo) in tons.
* `Weather_Condition`: Categorical representation of weather (0: Clear, 1: Rain/Snow, 2: Heavy Wind).
* `Fuel_Consumed_liters`: The total fuel consumed for that segment in liters (this is the target variable for prediction).

## Model & Optimization Logic

* **Model**: A `RandomForestRegressor` is used for its robustness and ability to capture non-linear relationships between input features and fuel consumption.
* **Prediction**: The model takes `Distance_km`, `Avg_Speed_kmh`, `Train_Weight_tons`, and `Weather_Condition` as inputs to predict `Fuel_Consumed_liters`.
* **Optimization Simulation**: The "Optimized Fuel" and "Potential Savings" values are currently a simplified simulation, demonstrating the concept of reduction. In a real-world scenario, this would involve:
    * More sophisticated optimization algorithms that consider dynamic factors (e.g., traffic, track grades, real-time weather forecasts).
    * Scenario analysis (e.g., "What if we reduce speed by 5 km/h?").
    * Integration with route planning to suggest the most fuel-efficient paths.
* **Recommendations**: The recommendations provided are based on simple rules derived from the input parameters (e.g., high speed, heavy weight, adverse weather). This can be expanded with more detailed rule-based systems or insights from advanced analytics.

## Potential Enhancements

This project is a strong foundation and can be significantly expanded to provide even greater value to CPKC:

* **Real-time Data Integration**: Connect to actual train telemetry, GPS data, and real-time weather APIs for live predictions and dynamic optimization.
* **Advanced Optimization Algorithms**: Implement more complex optimization models (e.g., genetic algorithms, reinforcement learning) to recommend precise speed profiles and routing changes for maximum fuel efficiency.
* **Geospatial Visualization**: Integrate with mapping libraries (e.g., Folium, Dash Leaflet) to visualize train routes, fuel consumption hotspots, and optimal paths on an interactive map.
* **Cost-Benefit Analysis**: Incorporate actual fuel prices to translate fuel savings directly into monetary savings and calculate ROI.
* **User Authentication & Roles**: Implement user login, role-based access control for dispatchers, operators, and analysts.
* **Alerting System**: Set up alerts for anomalous fuel consumption or deviations from optimized plans.
* **What-If Scenario Analysis**: Allow users to define complex "what-if" scenarios (e.g., "What if we increase train weight by 10% on route X?") and see the fuel impact.
* **Integration with Operations Systems**: Connect to existing CPKC operational systems for seamless data flow and implementation of recommendations.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/YourUsername/CPKC_Fuel_Efficiency_Dashboard/issues).

## License

This project is open-sourced under the MIT License. See the `LICENSE` file for more details.
