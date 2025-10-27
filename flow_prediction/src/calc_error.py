import pandas as pd
import numpy as np

def calculate_relative_errors(csv_file):
    """
    Calculate per-sample percentage errors and overall MAPE and relative RMSE.

    Parameters:
        csv_file (str): Path to CSV with columns 'actual_flow' and 'predicted_flow'

    Returns:
        dict: Mean Absolute Percentage Error (MAPE) and Relative RMSE (%)
        pd.DataFrame: Original CSV with extra column 'percent_error'
    """
    df = pd.read_csv(csv_file)
    
    y_true = df['actual_flow'].values
    y_pred = df['predicted_flow'].values
    
    # Avoid division by zero
    non_zero_mask = ~np.isclose(y_true, 0)
    y_true_nz = y_true[non_zero_mask]
    y_pred_nz = y_pred[non_zero_mask]
    
    # Per-sample absolute percentage error
    percent_errors = np.abs(y_pred_nz - y_true_nz) / y_true_nz * 100
    
    # Add percent error column to DataFrame (NaN for zero actuals)
    df['percent_error'] = np.nan
    df.loc[non_zero_mask, 'percent_error'] = percent_errors
    
    # Mean Absolute Percentage Error
    mape = percent_errors.mean()
    
    # Relative RMSE (%)
    rel_rmse = np.sqrt(np.mean(((y_pred_nz - y_true_nz) / y_true_nz) ** 2)) * 100
    
    results = {"MAPE(%)": mape, "Relative_RMSE(%)": rel_rmse}
    
    return results, df

# Example usage
if __name__ == "__main__":
    csv_file = "flow_prediction/results/predicted_vs_actual_robust.csv"
    errors, df_with_errors = calculate_relative_errors(csv_file)
    
    print("Errors:", errors)
    
    # Optionally, save the CSV with percent errors
    output_csv = "flow_prediction/results/predicted_vs_actual_with_errors.csv"
    df_with_errors.to_csv(output_csv, index=False)
    print(f"CSV with per-sample percent errors saved to {output_csv}")
