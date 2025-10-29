from prediction.src.utils.exportDf import *
from prediction.src.random_forest.predict import *
from prediction.src.utils.calcError import *

if __name__ == "__main__":
    # Export dataframe
    DF_INPUT_DIR = "perception/results"
    DF_OUTPUT_DIR = "flow_prediction/results/dataframe"
    export_df(input_dir=DF_INPUT_DIR, output_dir=DF_OUTPUT_DIR)
    
    # Export flow prediction
    PRED_INPUT_DIR = DF_OUTPUT_DIR
    PRED_OUTPUT_DIR = "flow_prediction/results/analysis"
    
    # Load data
    data = load_csv_from_dir(PRED_INPUT_DIR)
    
    # Train model
    model, predictions = train_random_forest(data, window=10)
    
    # Compute robust errors
    errors, predictions_with_errors = calculate_robust_errors(predictions, threshold=5)
    print("Robust Errors:", errors)
    
    write_predictions(predictions_with_errors, PRED_OUTPUT_DIR, filename="predicted_vs_actual.csv")
    
    ERR_INPUT_DIR = "flow_prediction/results/predicted_vs_actual.csv"
    errors, df_with_errors = calculate_relative_errors(ERR_INPUT_DIR)
    
    print("Errors:", errors)
    
    ERR_OUTPUT_DIR = "flow_prediction/results/predicted_vs_actual_with_errors.csv"
    df_with_errors.to_csv(output_csv, index=False)
    print(f"CSV with per-sample percent errors saved to {output_csv}")
