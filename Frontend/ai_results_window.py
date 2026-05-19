import tkinter as tk
from tkinter import ttk
import os
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_PATH = os.path.join(BASE_DIR, "Backend")

if BACKEND_PATH not in sys.path:
    sys.path.append(BACKEND_PATH)

from metrics_engine import get_model_metrics


def open_ai_results_window(parent, results):
    win = tk.Toplevel(parent)
    win.title("AI Load Match Results")
    win.geometry("1200x760")
    win.configure(bg="#f4f6f9")

    metrics = get_model_metrics()

    header = tk.Frame(win, bg="#111827", height=65)
    header.pack(fill="x")

    tk.Label(
        header,
        text="AI Load Match Dashboard",
        bg="#111827",
        fg="white",
        font=("Arial", 18, "bold")
    ).pack(side="left", padx=25, pady=18)

    tk.Label(
        header,
        text=f"Best Model: {metrics['best_model']}",
        bg="#111827",
        fg="#d1d5db",
        font=("Arial", 11, "bold")
    ).pack(side="right", padx=25)

    main = tk.Frame(win, bg="#f4f6f9")
    main.pack(fill="both", expand=True, padx=20, pady=15)

    left = tk.Frame(main, bg="#f4f6f9")
    left.pack(side="left", fill="both", expand=True)

    right = tk.Frame(main, bg="#f4f6f9", width=350)
    right.pack(side="right", fill="y", padx=(15, 0))

    # ================= RESULTS TABLE =================
    table_card = tk.Frame(left, bg="white", bd=1, relief="solid")
    table_card.pack(fill="both", expand=True)

    tk.Label(
        table_card,
        text="Top AI Recommended Loads",
        bg="white",
        fg="#111827",
        font=("Arial", 15, "bold")
    ).pack(anchor="w", padx=15, pady=(12, 5))

    columns = (
        "Rank",
        "Origin",
        "Destination",
        "Rate",
        "RPM",
        "Miles",
        "Truck",
        "Broker",
        "AI Score"
    )

    tree = ttk.Treeview(table_card, columns=columns, show="headings", height=15)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=105)

    tree.pack(fill="both", expand=True, padx=15, pady=10)

    clean_results = results.reset_index(drop=True)

    for idx, row in clean_results.iterrows():
        rpm = round(float(row["rate"]) / max(float(row["miles"]), 1), 2)
        score = round(float(row.get("ai_score_normalized", row.get("ai_score", 0))), 2)

        tree.insert("", "end", values=(
            idx + 1,
            row["origin_full"],
            row["destination_full"],
            f"${row['rate']}",
            f"${rpm}/mi",
            row["miles"],
            row["truck_type"],
            row.get("broker_name", "N/A"),
            f"{score}/100"
        ))

    # ================= LOAD DETAIL POPUP =================
    def show_load_details(event):
        selected = tree.focus()
        if not selected:
            return

        index = tree.index(selected)
        row = clean_results.iloc[index]

        detail = tk.Toplevel(win)
        detail.title("Recommended Load Details")
        detail.geometry("520x560")
        detail.configure(bg="#f4f6f9")

        h = tk.Frame(detail, bg="#111827", height=60)
        h.pack(fill="x")

        tk.Label(
            h,
            text="Recommended Load Details",
            bg="#111827",
            fg="white",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        card = tk.Frame(detail, bg="white", bd=1, relief="solid")
        card.pack(fill="both", expand=True, padx=20, pady=20)

        def title(text):
            tk.Label(card, text=text, bg="white", fg="#2563eb",
                     font=("Arial", 12, "bold")).pack(anchor="w", padx=20, pady=(12, 4))

        def line(label, value):
            f = tk.Frame(card, bg="white")
            f.pack(fill="x", padx=20, pady=3)

            tk.Label(f, text=label, bg="white", fg="#6b7280",
                     font=("Arial", 10, "bold"), width=18, anchor="w").pack(side="left")
            tk.Label(f, text=str(value), bg="white", fg="#111827",
                     font=("Arial", 10), anchor="w").pack(side="left")

        rpm = round(float(row["rate"]) / max(float(row["miles"]), 1), 2)

        title("Route")
        line("Origin:", row["origin_full"])
        line("Destination:", row["destination_full"])
        line("Miles:", row["miles"])

        title("Load")
        line("Rate:", f"${row['rate']}")
        line("RPM:", f"${rpm}/mi")
        line("Truck Type:", row["truck_type"])
        line("Weight:", f"{row['weight']} lbs")
        line("Origin DH:", f"{row['deadhead_origin']} mi")
        line("Destination DH:", f"{row['deadhead_destination']} mi")

        title("Broker")
        line("Broker Name:", row.get("broker_name", "N/A"))
        line("Broker Contact:", row.get("broker_contact", "N/A"))

        title("AI")
        line("AI Score:", f"{round(float(row.get('ai_score_normalized', 0)), 2)}/100")

        tk.Button(
            detail,
            text="Close",
            bg="#2563eb",
            fg="white",
            width=14,
            height=2,
            bd=0,
            font=("Arial", 10, "bold"),
            command=detail.destroy
        ).pack(pady=8)

    tree.bind("<Double-1>", show_load_details)

    # ================= METRICS PANEL =================
    metric_card = tk.Frame(right, bg="white", bd=1, relief="solid")
    metric_card.pack(fill="x", pady=(0, 15))

    tk.Label(
        metric_card,
        text="Model Performance",
        bg="white",
        fg="#111827",
        font=("Arial", 14, "bold")
    ).pack(anchor="w", padx=15, pady=(12, 8))

    def metric(label, value):
        box = tk.Frame(metric_card, bg="#f9fafb", bd=1, relief="solid")
        box.pack(fill="x", padx=15, pady=5)

        tk.Label(box, text=label, bg="#f9fafb", fg="#6b7280",
                 font=("Arial", 9, "bold")).pack(anchor="w", padx=10, pady=(6, 0))
        tk.Label(box, text=str(value), bg="#f9fafb", fg="#111827",
                 font=("Arial", 13, "bold")).pack(anchor="w", padx=10, pady=(0, 6))

    metric("Best Model", metrics["best_model"])
    metric("MAE", metrics["mae"])
    metric("R² Score", metrics["r2"])
    metric("Total Recommendations", len(results))

    # ================= GRAPH CARD =================
    graph_card = tk.Frame(right, bg="white", bd=1, relief="solid")
    graph_card.pack(fill="both", expand=True)

    tk.Label(
        graph_card,
        text="AI Score Graph",
        bg="white",
        fg="#111827",
        font=("Arial", 14, "bold")
    ).pack(anchor="w", padx=15, pady=(12, 8))

    fig, ax = plt.subplots(figsize=(4, 3))
    scores = [
        float(row.get("ai_score_normalized", row.get("ai_score", 0)))
        for _, row in clean_results.iterrows()
    ]

    ax.bar(range(1, len(scores) + 1), scores)
    ax.set_xlabel("Load Rank")
    ax.set_ylabel("AI Score")
    ax.set_title("Top Load Scores")
    ax.set_ylim(0, 100)

    canvas = FigureCanvasTkAgg(fig, master=graph_card)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)