import os
import pandas as pd
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "dataset", "loads_50000_realistic.csv")
MODEL_PATH = os.path.join(BASE_DIR, "Backend", "dispatch_model.pkl")


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

    df = df.dropna(subset=numeric_cols)

    # Feature engineering — MUST match train_model.py
    df["rate_per_mile"] = df["rate"] / df["miles"]
    df["total_deadhead"] = df["deadhead_origin"] + df["deadhead_destination"]

    df["efficiency"] = df["rate"] / (
        df["miles"] + df["total_deadhead"]
    )

    df["profit_estimate"] = (
        df["rate"] - (df["total_deadhead"] * 2)
    )

    return df


def get_ai_matches(
    origin="",
    destination="",
    truck="",
    max_deadhead=100,
    min_price=0,
    top_n=10
):
    df = load_data()

    if not os.path.exists(MODEL_PATH):
        raise Exception("Model not found. Run Backend/train_model.py first.")

    model = joblib.load(MODEL_PATH)

    filtered = df.copy()

    # Origin filter
    if origin:
        origin_city = origin.lower().split(",")[0].strip()
        filtered = filtered[
            filtered["origin_full"]
            .astype(str)
            .str.lower()
            .str.contains(origin_city, na=False)
        ]

    # Destination filter
    if destination:
        destination_city = destination.lower().split(",")[0].strip()
        filtered = filtered[
            filtered["destination_full"]
            .astype(str)
            .str.lower()
            .str.contains(destination_city, na=False)
        ]

    # Truck filter
    if truck:
        filtered = filtered[
            filtered["truck_type"]
            .astype(str)
            .str.lower()
            .str.contains(truck.lower(), na=False)
        ]

    # Deadhead + price filter
    filtered = filtered[
        (filtered["deadhead_origin"] <= float(max_deadhead)) &
        (filtered["rate"] >= float(min_price))
    ]

    # Fallback if too strict
    if filtered.empty:
        relaxed = df.copy()

        if origin:
            origin_city = origin.lower().split(",")[0].strip()
            relaxed = relaxed[
                relaxed["origin_full"]
                .astype(str)
                .str.lower()
                .str.contains(origin_city, na=False)
            ]

        relaxed = relaxed[
            relaxed["deadhead_origin"] <= float(max_deadhead) * 2
        ]

        filtered = relaxed

    # Final fallback
    if filtered.empty:
        filtered = df.copy()

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

    filtered["ai_score"] = model.predict(filtered[features])

    # Optional: convert score to 0–100 for nicer UI
    min_score = filtered["ai_score"].min()
    max_score = filtered["ai_score"].max()

    if max_score != min_score:
        filtered["ai_score_normalized"] = (
            (filtered["ai_score"] - min_score) /
            (max_score - min_score)
        ) * 100
    else:
        filtered["ai_score_normalized"] = 100

    best = filtered.sort_values(
        by="ai_score_normalized",
        ascending=False
    ).head(top_n)

    return best[
        [
            "origin_full",
            "destination_full",
            "rate",
            "miles",
            "deadhead_origin",
            "deadhead_destination",
            "rate_per_mile",
            "truck_type",
            "weight",
            "broker_name",
            "broker_contact",
            "ai_score",
            "ai_score_normalized"
        ]
    ]