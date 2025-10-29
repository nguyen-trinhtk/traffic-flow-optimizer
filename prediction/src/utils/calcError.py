import pandas as pd
import numpy as np

def calculate_relative_errors(csv_file):
    df = pd.read_csv(csv_file)
    
    y_true = df['actual_flow'].values
    y_pred = df['predicted_flow'].values
    
    non_zero_mask = ~np.isclose(y_true, 0)
    y_true_nz = y_true[non_zero_mask]
    y_pred_nz = y_pred[non_zero_mask]
    
    percent_errors = np.abs(y_pred_nz - y_true_nz) / y_true_nz * 100
    
    df['percent_error'] = np.nan
    df.loc[non_zero_mask, 'percent_error'] = percent_errors
    
    mape = percent_errors.mean()
    
    rel_rmse = np.sqrt(np.mean(((y_pred_nz - y_true_nz) / y_true_nz) ** 2)) * 100
    
    results = {"MAPE(%)": mape, "Relative_RMSE(%)": rel_rmse}
    
    return results, df

if __name__ == "__main__":
    csv_file = "flow_prediction/results/predicted_vs_actual_robust.csv"
    errors, df_with_errors = calculate_relative_errors(csv_file)
    
    print("Errors:", errors)
    
    output_csv = "flow_prediction/results/predicted_vs_actual_with_errors.csv"
    df_with_errors.to_csv(output_csv, index=False)
    print(f"CSV with per-sample percent errors saved to {output_csv}")
