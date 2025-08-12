import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.base import clone
import joblib

# Constants
MODEL_DIR = "models"
MODEL_PICKLE_PATH = os.path.join(MODEL_DIR, "model.pkl")
ALL_MODELS_PATH = os.path.join(MODEL_DIR, "all_models.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")

def clean_dataset(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()

    numeric_cols = [
        "Units Sold", "Manufacturing Price", "Sale Price", "Gross Sales",
        "Discounts", "Sales", "COGS", "Profit"
    ]

    for col in numeric_cols:
        df[col] = (
            df[col].astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("$", "", regex=False)
            .str.strip()
            .str.replace(r"^\((.*)\)$", r"-\1", regex=True)
        )
        df[col] = df[col].replace("-", np.nan).astype(float)

    # Debug: Check for NaN values
    print(f"NaN counts:\n{df[numeric_cols].isna().sum()}")
    df.dropna(subset=numeric_cols, inplace=True)

    # Debug: Verify Sales = Gross Sales - Discounts, Profit = Sales - COGS
    df["Calculated_Sales"] = df["Gross Sales"] - df["Discounts"]
    df["Calculated_Profit"] = df["Sales"] - df["COGS"]
    print(f"Data validation:\n{df[['Sales', 'Calculated_Sales', 'Profit', 'Calculated_Profit']].head()}")

    # Use IQR for outlier removal
    for col in ["Sales", "Profit"]:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        df = df[(df[col] >= Q1 - 1.5 * IQR) & (df[col] <= Q3 + 1.5 * IQR)]

    return df

def train_and_compare_models(df: pd.DataFrame):
    features = ["Year", "Month Number", "Units Sold", "Sale Price", "COGS"]
    target_sales = "Sales"
    target_profit = "Profit"

    X = df[features]
    y_sales = df[target_sales]
    y_profit = df[target_profit]

    # Scale features
    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=features)
    joblib.dump(scaler, SCALER_PATH)  # Save scaler

    X_train, X_test, y_train_sales, y_test_sales = train_test_split(X_scaled, y_sales, test_size=0.2, random_state=42)
    _, _, y_train_profit, y_test_profit = train_test_split(X_scaled, y_profit, test_size=0.2, random_state=42)

    model_map = {
        1: ("LinearRegression", LinearRegression()),
        2: ("RandomForest", RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)),
        3: ("GradientBoosting", GradientBoostingRegressor(n_estimators=100, max_depth=3, random_state=42)),
        4: ("KNeighbors", KNeighborsRegressor(n_neighbors=5))
    }

    results = {}
    all_models = {}

    for number, (name, model) in model_map.items():
        model_sales = clone(model)
        model_profit = clone(model)

        model_sales.fit(X_train, y_train_sales)
        model_profit.fit(X_train, y_train_profit)

        y_pred_sales = model_sales.predict(X_test)
        y_pred_profit = model_profit.predict(X_test)

        mse_sales = mean_squared_error(y_test_sales, y_pred_sales)
        mse_profit = mean_squared_error(y_test_profit, y_pred_profit)
        r2_sales = r2_score(y_test_sales, y_pred_sales)
        r2_profit = r2_score(y_test_profit, y_pred_profit)

        results[number] = {
            "name": name,
            "sales_mse": round(mse_sales, 2),
            "profit_mse": round(mse_profit, 2),
            "sales_accuracy": f"{round(r2_sales * 100, 2)}%",
            "profit_accuracy": f"{round(r2_profit * 100, 2)}%"
        }

        all_models[number] = {
            "sales_model": model_sales,
            "profit_model": model_profit
        }

        # Debug: Feature importance for RandomForest
        if name == "RandomForest":
            print(f"Feature importance (Sales):\n{pd.DataFrame({'Feature': features, 'Importance': model_sales.feature_importances_})}")

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(all_models, ALL_MODELS_PATH)

    return results

def evaluate_model(y_true, y_pred, label):
    print(f"\nEvaluation Metrics for {label} Prediction")
    print(f"MAE: {mean_absolute_error(y_true, y_pred):.2f}")
    print(f"MSE: {mean_squared_error(y_true, y_pred):.2f}")
    print(f"RMSE: {np.sqrt(mean_squared_error(y_true, y_pred)):.2f}")
    print(f"R2 Score: {r2_score(y_true, y_pred):.2f}")
    print("-" * 40)

def save_selected_model(model_number: int):
    all_models = joblib.load(ALL_MODELS_PATH)
    selected_model = all_models.get(model_number)
    if not selected_model:
        raise ValueError(f"Invalid model number: {model_number}")
    joblib.dump(selected_model, MODEL_PICKLE_PATH)

def load_model():
    if not os.path.exists(MODEL_PICKLE_PATH):
        raise FileNotFoundError("Model not trained yet.")
    return joblib.load(MODEL_PICKLE_PATH)

def predict(model_dict, input_data: pd.DataFrame):
    expected_columns = ["Year", "Month Number", "Units Sold", "Sale Price", "COGS"]
    if not all(col in input_data.columns for col in expected_columns):
        raise ValueError(f"Input data must contain columns: {expected_columns}")
    if input_data[expected_columns].isna().any().any():
        raise ValueError("Input data contains NaN values")

    input_data = input_data[expected_columns].astype(float)
    print("Input data:\n", input_data)

    scaler = joblib.load(SCALER_PATH)
    input_data_scaled = pd.DataFrame(scaler.transform(input_data), columns=expected_columns)
    print("Scaled input data:\n", input_data_scaled)

    sales = model_dict["sales_model"].predict(input_data_scaled)
    profit = model_dict["profit_model"].predict(input_data_scaled)
    print(f"Predictions - Sales: {sales}, Profit: {profit}")

    return sales, profit

# Example usage
if __name__ == "__main__":
    # Clean and train
    df = clean_dataset("Financials_synthetic_5000.csv")
    results = train_and_compare_models(df)
    print("Model Results:")
    for number, result in results.items():
        print(f"Model {number}: {result}")

    # Save RandomForest model (example)
    save_selected_model(2)

    # Test prediction
    input_data = pd.DataFrame({
        "Year": [2018],
        "Month Number": [6],
        "Units Sold": [500.0],
        "Sale Price": [50.0],
        "COGS": [20000.0]
    })
    model_dict = load_model()
    sales, profit = predict(model_dict, input_data)
    print(f"Final Predictions - Sales: {sales[0]:.2f}, Profit: {profit[0]:.2f}")