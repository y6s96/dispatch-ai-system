import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

from xgboost import XGBRegressor

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "loads_50000_realistic.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "Backend",
    "dispatch_model.pkl"
)

RESULTS_PATH = os.path.join(
    BASE_DIR,
    "Backend",
    "model_results.csv"
)


# =========================
# LOAD DATA
# =========================
def load_data():
    df = pd.read_csv(DATA_PATH)

    if "deadhead_destination" not in df.columns:
        df["deadhead_destination"] = df["deadhead_origin"] * 0.5

    numeric_cols = [
        "miles",
        "rate",
        "deadhead_origin",
        "deadhead_destination",
        "weight"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna()

    # =========================
    # FEATURE ENGINEERING
    # =========================
    df["rate_per_mile"] = df["rate"] / df["miles"]

    df["total_deadhead"] = (
        df["deadhead_origin"] +
        df["deadhead_destination"]
    )

    df["efficiency"] = (
        df["rate"] /
        (df["miles"] + df["total_deadhead"])
    )

    df["profit_estimate"] = (
        df["rate"] -
        (df["total_deadhead"] * 2)
    )

    # =========================
    # TARGET SCORE
    # =========================
    df["load_score"] = (
        (df["rate_per_mile"] * 15)
        + (df["rate"] / 800)
        - (df["total_deadhead"] * 0.05)
        - (df["weight"] / 120000)
        + (df["efficiency"] * 10)
    )

    return df


# =========================
# TRAIN
# =========================
def train():
    df = load_data()

    features = [
        "miles",
        "rate",
        "deadhead_origin",
        "deadhead_destination",
        "weight",
        "rate_per_mile",
        "total_deadhead",
        "efficiency",
        "profit_estimate",
        "truck_type",
        "origin_full",
        "destination_full"
    ]

    target = "load_score"

    X = df[features]
    y = df[target]

    numeric_features = [
        "miles",
        "rate",
        "deadhead_origin",
        "deadhead_destination",
        "weight",
        "rate_per_mile",
        "total_deadhead",
        "efficiency",
        "profit_estimate"
    ]

    categorical_features = [
        "truck_type",
        "origin_full",
        "destination_full"
    ]

    preprocessor = ColumnTransformer([
        (
            "num",
            StandardScaler(),
            numeric_features
        ),
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ])

    models = {
        "Linear Regression": LinearRegression(),

        "Decision Tree": DecisionTreeRegressor(),

        "Random Forest": RandomForestRegressor(
            n_estimators=200,
            max_depth=12,
            random_state=42
        ),

        "XGBoost": XGBRegressor(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=8,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1
        )
    }

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    best_model = None
    best_r2 = -999

    results = []

    print("\nMODEL RESULTS\n")

    for name, model in models.items():

        pipe = Pipeline([
            ("preprocessor", preprocessor),
            ("model", model)
        ])

        pipe.fit(X_train, y_train)

        preds = pipe.predict(X_test)

        mae = mean_absolute_error(y_test, preds)
        r2 = r2_score(y_test, preds)

        print(f"{name}")
        print(f"MAE: {round(mae, 3)}")
        print(f"R2 : {round(r2, 3)}")
        print("-------------------")

        results.append({
            "model": name,
            "MAE": round(mae, 3),
            "R2": round(r2, 3)
        })

        if r2 > best_r2:
            best_r2 = r2
            best_model = pipe

    results_df = pd.DataFrame(results)

    results_df.to_csv(
        RESULTS_PATH,
        index=False
    )

    joblib.dump(
        best_model,
        MODEL_PATH
    )

    print("\nBEST MODEL SAVED")
    print(MODEL_PATH)


if __name__ == "__main__":
    train()