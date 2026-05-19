import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_PATH = os.path.join(BASE_DIR, "Backend", "model_results.csv")


def get_model_metrics():
    if not os.path.exists(RESULTS_PATH):
        return {
            "best_model": "Not trained",
            "mae": "N/A",
            "r2": "N/A",
            "models": []
        }

    df = pd.read_csv(RESULTS_PATH)

    best = df.sort_values(by="R2", ascending=False).iloc[0]

    return {
        "best_model": best["model"],
        "mae": best["MAE"],
        "r2": best["R2"],
        "models": df.to_dict("records")
    }