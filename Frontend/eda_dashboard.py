import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")


def open_eda_dashboard(parent):
    win = tk.Toplevel(parent)
    win.title("EDA Dashboard")
    win.geometry("1100x720")
    win.configure(bg="#f4f6f9")

    header = tk.Frame(win, bg="#111827", height=65)
    header.pack(fill="x")

    tk.Label(
        header,
        text="EDA Dashboard - Freight Load Analysis",
        bg="#111827",
        fg="white",
        font=("Arial", 18, "bold")
    ).pack(side="left", padx=25, pady=18)

    notebook = ttk.Notebook(win)
    notebook.pack(fill="both", expand=True, padx=15, pady=15)

    images = [
        ("Rate Distribution", "rate_distribution.png"),
        ("RPM Distribution", "rpm_distribution.png"),
        ("Truck Type", "truck_type_distribution.png"),
        ("Miles vs Rate", "miles_vs_rate.png"),
        ("Rate by Truck", "rate_by_truck_type.png"),
        ("Correlation Heatmap", "correlation_heatmap.png"),
    ]

    image_refs = []

    def add_image_tab(title, filename):
        tab = tk.Frame(notebook, bg="white")
        notebook.add(tab, text=title)

        path = os.path.join(OUTPUTS_DIR, filename)

        if not os.path.exists(path):
            tk.Label(
                tab,
                text=f"Image not found:\n{path}\n\nGenerate this graph from your notebook first.",
                bg="white",
                fg="red",
                font=("Arial", 12, "bold")
            ).pack(expand=True)
            return

        img = Image.open(path)
        img.thumbnail((1000, 580))

        photo = ImageTk.PhotoImage(img)
        image_refs.append(photo)

        tk.Label(tab, image=photo, bg="white").pack(expand=True, padx=10, pady=10)

    for title, filename in images:
        add_image_tab(title, filename)

    win.image_refs = image_refs