import tkinter as tk
from tkinter import ttk
import pandas as pd
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BACKEND_PATH = os.path.join(BASE_DIR, "Backend")

if BACKEND_PATH not in sys.path:
    sys.path.append(BACKEND_PATH)

from ai_engine import get_ai_matches
from ai_results_window import open_ai_results_window


def open_ai_window(parent):

    ai_win = tk.Toplevel(parent)
    ai_win.title("AI Load Matching")
    ai_win.geometry("950x650")
    ai_win.configure(bg="#f4f6f9")

    # =========================
    # LOAD DATASET
    # =========================
    file_path = os.path.join(
        BASE_DIR,
        "dataset",
        "loads_50000_realistic.csv"
    )

    df = pd.read_csv(file_path)

    origin_locations = sorted(
        df["origin_full"].dropna().unique()
    )

    destination_locations = sorted(
        df["destination_full"].dropna().unique()
    )

    # =========================
    # FILTER COMBO
    # =========================
    def filter_combo(event, combo, values):
        typed = combo.get().lower()

        combo["values"] = [
            item for item in values
            if typed in item.lower()
        ][:10]

    # =========================
    # HEADER
    # =========================
    topbar = tk.Frame(
        ai_win,
        bg="#111827",
        height=60
    )

    topbar.pack(fill="x")

    tk.Label(
        topbar,
        text="EZ LOGISTICS AI",
        bg="#111827",
        fg="white",
        font=("Arial", 18, "bold")
    ).pack(side="left", padx=25, pady=15)

    tk.Label(
        topbar,
        text="AI Dispatch Matching",
        bg="#111827",
        fg="#d1d5db",
        font=("Arial", 11, "bold")
    ).pack(side="right", padx=25)

    # =========================
    # MAIN CARD
    # =========================
    main = tk.Frame(ai_win, bg="#f4f6f9")
    main.pack(fill="both", expand=True, padx=25, pady=20)

    card = tk.Frame(main, bg="white", bd=1, relief="solid")
    card.pack(fill="x")

    tk.Label(
        card,
        text="AI Driver Search",
        bg="white",
        fg="#111827",
        font=("Arial", 16, "bold")
    ).grid(
        row=0,
        column=0,
        columnspan=4,
        sticky="w",
        padx=20,
        pady=(18, 8)
    )

    # =========================
    # LABEL HELPER
    # =========================
    def label(text, row, col):
        tk.Label(
            card,
            text=text,
            bg="white",
            fg="#374151",
            font=("Arial", 9, "bold")
        ).grid(
            row=row,
            column=col,
            sticky="w",
            padx=20,
            pady=(6, 2)
        )

    # =========================
    # ENTRY HELPER
    # =========================
    def entry(row, col, width=24):
        e = tk.Entry(
            card,
            width=width,
            font=("Arial", 11),
            bd=1,
            relief="solid"
        )

        e.grid(
            row=row,
            column=col,
            padx=20,
            pady=(0, 12),
            ipady=5
        )

        return e

    # =========================
    # COMBO HELPER
    # =========================
    def combo(row, col, values, width=22):

        c = ttk.Combobox(
            card,
            values=values,
            width=width,
            font=("Arial", 10)
        )

        c.grid(
            row=row,
            column=col,
            padx=20,
            pady=(0, 12),
            ipady=4
        )

        return c

    # =========================
    # FIELDS
    # =========================
    label("Driver Name", 1, 0)
    driver_name = entry(2, 0)

    label("Truck Type", 1, 1)
    truck_type = combo(
        2,
        1,
        ["Dry Van", "Reefer", "Flatbed", "Step Deck"]
    )

    truck_type.set("Dry Van")

    label("Driver Origin", 1, 2)
    origin_box = combo(
        2,
        2,
        origin_locations
    )

    origin_box.bind(
        "<KeyRelease>",
        lambda e: filter_combo(
            e,
            origin_box,
            origin_locations
        )
    )

    label("Preferred Destination", 1, 3)
    destination_box = combo(
        2,
        3,
        destination_locations
    )

    destination_box.bind(
        "<KeyRelease>",
        lambda e: filter_combo(
            e,
            destination_box,
            destination_locations
        )
    )

    label("Max Deadhead", 3, 0)
    deadhead = combo(
        4,
        0,
        ["50", "100", "150", "200"]
    )

    deadhead.set("100")

    label("Minimum Price", 3, 1)
    min_price = entry(4, 1)

    label("Top Results", 3, 2)
    top_results = combo(
        4,
        2,
        ["5", "10", "15", "20"]
    )

    top_results.set("10")

    # =========================
    # RESULT BOX
    # =========================
    result_card = tk.Frame(
        main,
        bg="white",
        bd=1,
        relief="solid"
    )

    result_card.pack(
        fill="both",
        expand=True,
        pady=20
    )

    tk.Label(
        result_card,
        text="AI Status",
        bg="white",
        fg="#111827",
        font=("Arial", 14, "bold")
    ).pack(anchor="w", padx=20, pady=(12, 5))

    result_box = tk.Text(
        result_card,
        height=10,
        bg="#f9fafb",
        fg="#111827",
        font=("Arial", 10),
        bd=0
    )

    result_box.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    # =========================
    # RUN AI
    # =========================
    def run_ai():

        result_box.delete("1.0", tk.END)

        result_box.insert(
            tk.END,
            "Running AI matching engine...\n"
        )

        try:

            results = get_ai_matches(
                origin=origin_box.get(),
                destination=destination_box.get(),
                truck=truck_type.get(),
                max_deadhead=float(deadhead.get()),
                min_price=float(min_price.get() or 0),
                top_n=int(top_results.get())
            )

            if results is None or len(results) == 0:

                result_box.insert(
                    tk.END,
                    "No matching loads found.\n"
                )

                return

            result_box.insert(
                tk.END,
                f"Found {len(results)} AI matches.\n"
            )

            result_box.insert(
                tk.END,
                "Opening AI dashboard...\n"
            )

            open_ai_results_window(
                ai_win,
                results
            )

        except Exception as e:

            result_box.insert(
                tk.END,
                f"\nERROR:\n{str(e)}"
            )

    # =========================
    # BUTTONS
    # =========================
    btn_frame = tk.Frame(card, bg="white")

    btn_frame.grid(
        row=5,
        column=0,
        columnspan=4,
        sticky="e",
        padx=20,
        pady=15
    )

    tk.Button(
        btn_frame,
        text="Run AI Match",
        bg="#2563eb",
        fg="white",
        width=18,
        height=2,
        bd=0,
        font=("Arial", 10, "bold"),
        command=run_ai
    ).pack(side="right", padx=6)

    tk.Button(
        btn_frame,
        text="Close",
        bg="#6b7280",
        fg="white",
        width=12,
        height=2,
        bd=0,
        font=("Arial", 10, "bold"),
        command=ai_win.destroy
    ).pack(side="right", padx=6)