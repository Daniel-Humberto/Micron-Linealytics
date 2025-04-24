import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
import joblib

def prepare_dataset(xls):
    demand_df = pd.read_excel(xls, sheet_name="Supply_Demand")
    yield_df = pd.read_excel(xls, sheet_name="Yield")
    density_df = pd.read_excel(xls, sheet_name="Density per Wafer")
    wafer_df = pd.read_excel(xls, sheet_name="Wafer Plan")

    for df in [demand_df, yield_df, wafer_df]:
        df["Year"] = df["Year"].astype(int)
        df["Month"] = df["Month"].astype(int)

    df = demand_df.merge(yield_df, on=["Product", "Year", "Month"], how="left")
    df = df.merge(density_df, on="Product", how="left")
    df = df.merge(wafer_df, on=["Product", "Year", "Month"], how="left")
    df = df.dropna()

    return df

def train_xgboost_model(df):
    le = LabelEncoder()
    df["Product"] = le.fit_transform(df["Product"])

    X = df[["Product", "Year", "Month", "Yield", "Density", "Wafer Plan"]]
    y = df["Demand"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = XGBRegressor(objective="reg:squarederror", n_estimators=100, learning_rate=0.1, max_depth=5)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred, squared=False)

    # Guardar modelo y codificador para uso futuro
    joblib.dump(model, "xgb_model.pkl")
    joblib.dump(le, "product_encoder.pkl")

    return model, le, rmse

def predict_demand(product_name, year, month, yield_val, density, wafer_plan):
    """
    Predice la demanda de un producto en tiempo real.
    """
    model = joblib.load("xgb_model.pkl")
    le = joblib.load("product_encoder.pkl")

    # Codificar producto
    try:
        product_encoded = le.transform([product_name])[0]
    except ValueError:
        raise ValueError(f"Producto '{product_name}' no reconocido en el modelo.")

    # Construir DataFrame de entrada
    input_df = pd.DataFrame([{
        "Product": product_encoded,
        "Year": year,
        "Month": month,
        "Yield": yield_val,
        "Density": density,
        "Wafer Plan": wafer_plan
    }])

    predicted_demand = model.predict(input_df)[0]
    return predicted_demand

# Ejemplo de uso de predicción:
if __name__ == "__main__":
    # Entrenamiento inicial (si no lo has hecho ya)
    xls = pd.ExcelFile("Hackaton_DB_Final.xlsx")
    df = prepare_dataset(xls)
    model, encoder, error = train_xgboost_model(df)
    print(f"Modelo entrenado con RMSE: {error:.2f}")

    # Predicción en tiempo real
    try:
        pred = predict_demand("Product A", 2025, 5, yield_val=0.85, density=0.9, wafer_plan=300)
        print(f"Demanda estimada para 'Product A': {pred:.2f}")
    except ValueError as ve:
        print(ve)
