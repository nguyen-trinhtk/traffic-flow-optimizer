import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# -------------------------------
# Feature Engineering
# -------------------------------
def build_features(data, window=10):
    df = data.copy().sort_values('frame_index')
    
    # Lag features
    for lag in range(1, window + 1):
        df[f'flow_lag_{lag}'] = df['flow'].shift(lag)
        if 'density' in df.columns:
            df[f'density_lag_{lag}'] = df['density'].shift(lag)
        if 'avg_speed' in df.columns:
            df[f'speed_lag_{lag}'] = df['avg_speed'].shift(lag)
    
    # Trend features
    df['flow_diff_1'] = df['flow'] - df['flow_lag_1']
    df['flow_ma_3'] = df['flow'].rolling(3).mean().shift(1)
    
    # Time features
    df['hour'] = df['frame_index'] // 60 % 24
    df['weekday'] = df['frame_index'] // (60*24) % 7
    
    df = df.dropna().reset_index(drop=True)
    return df

# -------------------------------
# Train Model
# -------------------------------
def train_random_forest(df, window=10, test_size=0.2, random_state=42):
    df_features = build_features(df, window)
    
    feature_cols = [c for c in df_features.columns if c not in ['frame_index', 'flow']]
    target_col = 'flow'
    
    X = df_features[feature_cols]
    y = df_features[target_col]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, shuffle=False
    )
    
    # Random Forest with deeper trees and more estimators
    model = RandomForestRegressor(
        n_estimators=500,
        max_depth=None,
        min_samples_leaf=5,
        random_state=random_state,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    results = pd.DataFrame({
        "frame_index": df_features.loc[y_test.index, "frame_index"],
        "actual_flow": y_test,
        "predicted_flow": y_pred
    })
    
    return model, results

# -------------------------------
# Robust Error Calculation
# -------------------------------
def calculate_robust_errors(results, threshold=5):
    y_true = results['actual_flow'].values
    y_pred = results['predicted_flow'].values
    
    mask = y_true >= threshold
    y_true_valid = y_true[mask]
    y_pred_valid = y_pred[mask]
    
    percent_errors = np.abs(y_pred_valid - y_true_valid) / y_true_valid * 100
    
    results['percent_error'] = np.nan
    results.loc[mask, 'percent_error'] = percent_errors
    
    robust_mape = percent_errors.mean()
    robust_rel_rmse = np.sqrt(np.mean(((y_pred_valid - y_true_valid) / y_true_valid) ** 2)) * 100
    
    return {"Robust_MAPE(%)": robust_mape, "Robust_Relative_RMSE(%)": robust_rel_rmse}, results

# -------------------------------
# Load CSVs
# -------------------------------
def load_csv_from_dir(directory):
    all_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.csv')]
    df_list = []
    frame_counter = 0
    for file in all_files:
        df = pd.read_csv(file)
        df['frame_index'] = np.arange(frame_counter, frame_counter + len(df))
        frame_counter += len(df)
        df_list.append(df)
    combined_df = pd.concat(df_list, ignore_index=True)
    return combined_df

# -------------------------------
# Write predictions
# -------------------------------
def write_predictions(results, directory, filename="predicted_vs_actual.csv"):
    output_file = os.path.join(directory, filename)
    results.to_csv(output_file, index=False)
    print(f"Predicted vs actual flow written to {output_file}")

# -------------------------------
# Main pipeline
# -------------------------------
if __name__ == "__main__":
    data_dir = "flow_prediction/results/df"
    output_dir = "flow_prediction/results/"
    
    # Load data
    data = load_csv_from_dir(data_dir)
    
    # Train model
    model, predictions = train_random_forest(data, window=10)
    
    # Compute robust errors
    errors, predictions_with_errors = calculate_robust_errors(predictions, threshold=5)
    print("Robust Errors:", errors)
    
    # Save predictions with per-frame % errors
    write_predictions(predictions_with_errors, output_dir, filename="predicted_vs_actual_robust.csv")
