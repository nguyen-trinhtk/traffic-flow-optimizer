import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt

def build_features(data, window=5):
    df = data.copy().sort_values('frame_index')

    for lag in range(1, window + 1):
        df[f'flow_lag_{lag}'] = df['flow'].shift(lag)
        if 'density' in df.columns:
            df[f'density_lag_{lag}'] = df['density'].shift(lag)
        if 'avg_speed' in df.columns:
            df[f'speed_lag_{lag}'] = df['avg_speed'].shift(lag)

    df = df.dropna().reset_index(drop=True)
    return df


def train_random_forest(df, window=5, test_size=0.2, random_state=42):
    df_features = build_features(df, window)

    feature_cols = [c for c in df_features.columns if 'lag_' in c]
    target_col = 'flow'

    X = df_features[feature_cols]
    y = df_features[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, shuffle=False
    )

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=8,
        random_state=random_state,
        n_jobs=-1
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Evaluate
    mae = mean_absolute_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred)

    results = pd.DataFrame({
        "frame_index": df_features.loc[y_test.index, "frame_index"],
        "actual_flow": y_test,
        "predicted_flow": y_pred
    })

    plt.figure(figsize=(8, 4))
    plt.plot(results["frame_index"], results["actual_flow"], label="Actual")
    plt.plot(results["frame_index"], results["predicted_flow"], label="Predicted")
    plt.xlabel("Frame Index")
    plt.ylabel("Flow")
    plt.title("Traffic Flow Prediction")
    plt.legend()
    plt.tight_layout()
    plt.show()

    return {
        "model": model,
        "predictions": results,
        "metrics": {"MAE": mae, "RMSE": rmse}
    }


if __name__ == "__main__":
    data = pd.DataFrame({
        "frame_index": np.arange(1, 501),
        "flow": np.random.normal(20, 5, 500).clip(0),  # example flow data
        "density": np.random.uniform(5, 15, 500),
        "avg_speed": np.random.uniform(10, 30, 500)
    })

    results = train_random_forest(data, window=5)
    print("Metrics:", results["metrics"])
