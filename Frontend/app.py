import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import pandas as pd
import os
from ai_window import open_ai_window
from eda_dashboard import open_eda_dashboard

# =========================
# LOAD DATASET
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, "dataset", "loads_50000_realistic.csv")

df = pd.read_csv(file_path)

df["pickup_date"] = pd.to_datetime(df["pickup_date"], errors="coerce")
df["delivery_date"] = pd.to_datetime(df["delivery_date"], errors="coerce")

if "broker_name" not in df.columns:
    df["broker_name"] = "N/A"

if "broker_contact" not in df.columns:
    df["broker_contact"] = "N/A"

if "deadhead_destination" not in df.columns:
    df["deadhead_destination"] = 0


# =========================
# MAIN APP
# =========================
class LoadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hamza Logistics Load Board")
        self.root.geometry("1280x720")
        self.root.configure(bg="#f4f6f9")

        self.frames = {}

        for F in (WelcomePage, SearchPage):
            frame = F(self.root, self)
            self.frames[F] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame(WelcomePage)

    def show_frame(self, page):
        self.frames[page].tkraise()


# =========================
# HEADER
# =========================
def create_header(parent, title):
    header = tk.Frame(parent, bg="#111827", height=65)
    header.pack(fill="x")

    tk.Label(
        header,
        text=title,
        fg="white",
        bg="#111827",
        font=("Arial", 18, "bold")
    ).pack(side="left", padx=30, pady=18)

    tk.Label(
        header,
        text="AI Powered Dispatch System",
        fg="#d1d5db",
        bg="#111827",
        font=("Arial", 11, "bold")
    ).pack(side="right", padx=30)


# =========================
# WELCOME PAGE
# =========================
class WelcomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f4f6f9")

        create_header(self, "Hamza's LoadBoard")

        container = tk.Frame(self, bg="#f4f6f9")
        container.pack(expand=True)

        tk.Label(
            container,
            text="Welcome to Hamza's Loadboard",
            font=("Arial", 26, "bold"),
            bg="#f4f6f9",
            fg="#111827"
        ).pack(pady=15)

        tk.Label(
            container,
            text="Ease your logistics partner with smart load search and AI matching.",
            font=("Arial", 12),
            bg="#f4f6f9",
            fg="#6b7280"
        ).pack(pady=5)

        tk.Button(
            container,
            text="Search Loads",
            bg="#2563eb",
            fg="white",
            width=28,
            height=2,
            font=("Arial", 12, "bold"),
            bd=0,
            command=lambda: controller.show_frame(SearchPage)
        ).pack(pady=12)

        tk.Button(
            container,
            text="AI Load Match",
            bg="#10b981",
            fg="white",
            width=28,
            height=2,
            font=("Arial", 12, "bold"),
            bd=0,
            command=lambda: open_ai_window(controller.root)
        ).pack(pady=12)

        tk.Button(
            container,
            text="EDA Dashboard",
            bg="#7c3aed",
            fg="white",
            width=28,
            height=2,
            font=("Arial", 12, "bold"),
            bd=0,
            command=lambda: open_eda_dashboard(controller.root)
        ).pack(pady=12)


# =========================
# SEARCH PAGE
# =========================
class SearchPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f4f6f9")

        self.current_data = pd.DataFrame()

        create_header(self, "Search Loads")

        card = tk.Frame(self, bg="white", bd=1, relief="solid")
        card.pack(padx=25, pady=20, fill="x")

        tk.Label(
            card,
            text="Load Search",
            bg="white",
            fg="#111827",
            font=("Arial", 16, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))

        input_frame = tk.Frame(card, bg="white")
        input_frame.pack(pady=15)

        tk.Label(input_frame, text="Origin", bg="white", fg="#374151",
                 font=("Arial", 9, "bold")).grid(row=0, column=0, sticky="w")
        self.origin_var = tk.StringVar()
        self.origin_box = ttk.Combobox(input_frame, textvariable=self.origin_var, width=25)
        self.origin_box["values"] = sorted(df["origin_full"].dropna().unique())
        self.origin_box.grid(row=1, column=0, padx=6, ipady=4)

        tk.Label(input_frame, text="Destination", bg="white", fg="#374151",
                 font=("Arial", 9, "bold")).grid(row=0, column=1, sticky="w")
        self.dest_var = tk.StringVar()
        self.dest_box = ttk.Combobox(input_frame, textvariable=self.dest_var, width=25)
        self.dest_box["values"] = sorted(df["destination_full"].dropna().unique())
        self.dest_box.grid(row=1, column=1, padx=6, ipady=4)

        tk.Label(input_frame, text="Pickup From", bg="white", fg="#374151",
                 font=("Arial", 9, "bold")).grid(row=0, column=2, sticky="w")
        self.date_from = DateEntry(input_frame, width=12, date_pattern="yyyy-mm-dd")
        self.date_from.grid(row=1, column=2, padx=6, ipady=4)

        tk.Label(input_frame, text="Pickup To", bg="white", fg="#374151",
                 font=("Arial", 9, "bold")).grid(row=0, column=3, sticky="w")
        self.date_to = DateEntry(input_frame, width=12, date_pattern="yyyy-mm-dd")
        self.date_to.grid(row=1, column=3, padx=6, ipady=4)

        tk.Label(input_frame, text="Max Deadhead", bg="white", fg="#374151",
                 font=("Arial", 9, "bold")).grid(row=0, column=4, sticky="w")
        self.deadhead_var = tk.StringVar(value="100")
        self.deadhead_box = ttk.Combobox(
            input_frame,
            textvariable=self.deadhead_var,
            values=["50", "100", "150", "200", "250"],
            state="readonly",
            width=12
        )
        self.deadhead_box.grid(row=1, column=4, padx=6, ipady=4)

        tk.Label(input_frame, text="Truck Type", bg="white", fg="#374151",
                 font=("Arial", 9, "bold")).grid(row=0, column=5, sticky="w")
        self.truck_var = tk.StringVar()
        self.truck_box = ttk.Combobox(
            input_frame,
            textvariable=self.truck_var,
            values=["", "Dry Van", "Reefer", "Flatbed", "Step Deck"],
            width=12
        )
        self.truck_box.grid(row=1, column=5, padx=6, ipady=4)

        tk.Button(
            input_frame,
            text="Search",
            bg="#2563eb",
            fg="white",
            width=10,
            bd=0,
            font=("Arial", 10, "bold"),
            command=self.search
        ).grid(row=1, column=6, padx=6, ipady=5)

        tk.Button(
            input_frame,
            text="AI",
            bg="#10b981",
            fg="white",
            width=8,
            bd=0,
            font=("Arial", 10, "bold"),
            command=lambda: open_ai_window(controller.root)
        ).grid(row=1, column=7, padx=6, ipady=5)

        tk.Button(
            input_frame,
            text="Back",
            bg="#6b7280",
            fg="white",
            width=8,
            bd=0,
            font=("Arial", 10, "bold"),
            command=lambda: controller.show_frame(WelcomePage)
        ).grid(row=1, column=8, padx=6, ipady=5)

        table_frame = tk.Frame(self, bg="white")
        table_frame.pack(fill="both", expand=True, padx=25, pady=10)

        columns = (
            "Origin", "Destination", "Pickup", "Delivery", "Miles",
            "Deadhead", "Rate", "RPM", "Truck", "Weight", "Broker"
        )

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#e5e7eb")
        style.configure("Treeview", rowheight=30, font=("Arial", 10))

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=105)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self.show_load_details)

    def search(self):
        origin_input = self.origin_var.get().strip().lower()
        dest_input = self.dest_var.get().strip().lower()
        truck_input = self.truck_var.get().strip().lower()
        max_deadhead = int(self.deadhead_var.get())

        date_from = pd.to_datetime(self.date_from.get_date())
        date_to = pd.to_datetime(self.date_to.get_date())

        filtered = df.copy()

        if origin_input:
            filtered = filtered[
                filtered["origin_full"].str.lower().str.contains(origin_input, na=False)
            ]

        if dest_input:
            filtered = filtered[
                filtered["destination_full"].str.lower().str.contains(dest_input, na=False)
            ]

        if truck_input:
            filtered = filtered[
                filtered["truck_type"].str.lower().str.contains(truck_input, na=False)
            ]

        filtered = filtered[filtered["deadhead_origin"] <= max_deadhead]

        filtered = filtered[
            (filtered["pickup_date"] >= date_from) &
            (filtered["pickup_date"] <= date_to)
        ]

        self.current_data = filtered.head(200).reset_index(drop=True)
        self.show_results(self.current_data)

    def show_results(self, data):
        self.tree.delete(*self.tree.get_children())

        for _, row in data.iterrows():
            miles = max(float(row["miles"]), 1)
            rpm = round(float(row["rate"]) / miles, 2)

            pickup = row["pickup_date"].strftime("%Y-%m-%d") if pd.notna(row["pickup_date"]) else "N/A"
            delivery = row["delivery_date"].strftime("%Y-%m-%d") if pd.notna(row["delivery_date"]) else "N/A"

            self.tree.insert("", "end", values=(
                row["origin_full"],
                row["destination_full"],
                pickup,
                delivery,
                row["miles"],
                row["deadhead_origin"],
                f"${row['rate']}",
                f"${rpm}/mi",
                row["truck_type"],
                row["weight"],
                row["broker_name"]
            ))

    def show_load_details(self, event):
        selected = self.tree.focus()

        if not selected:
            return

        index = self.tree.index(selected)

        if self.current_data.empty or index >= len(self.current_data):
            return

        row = self.current_data.iloc[index]

        detail_win = tk.Toplevel(self)
        detail_win.title("Load Details")
        detail_win.geometry("560x620")
        detail_win.configure(bg="#f4f6f9")

        header = tk.Frame(detail_win, bg="#111827", height=60)
        header.pack(fill="x")

        tk.Label(
            header,
            text="Load Details",
            bg="#111827",
            fg="white",
            font=("Arial", 17, "bold")
        ).pack(pady=15)

        card = tk.Frame(detail_win, bg="white", bd=1, relief="solid")
        card.pack(padx=20, pady=20, fill="both", expand=True)

        miles = max(float(row["miles"]), 1)
        rpm = round(float(row["rate"]) / miles, 2)

        pickup = row["pickup_date"].strftime("%Y-%m-%d") if pd.notna(row["pickup_date"]) else "N/A"
        delivery = row["delivery_date"].strftime("%Y-%m-%d") if pd.notna(row["delivery_date"]) else "N/A"

        def section_title(text):
            tk.Label(card, text=text, bg="white", fg="#2563eb",
                     font=("Arial", 12, "bold")).pack(anchor="w", padx=20, pady=(14, 5))

        def row_text(label, value):
            row_frame = tk.Frame(card, bg="white")
            row_frame.pack(fill="x", padx=20, pady=3)

            tk.Label(row_frame, text=label, bg="white", fg="#6b7280",
                     font=("Arial", 10, "bold"), width=20, anchor="w").pack(side="left")

            tk.Label(row_frame, text=str(value), bg="white", fg="#111827",
                     font=("Arial", 10), anchor="w").pack(side="left")

        section_title("Route Information")
        row_text("Origin:", row["origin_full"])
        row_text("Destination:", row["destination_full"])
        row_text("Pickup Date:", pickup)
        row_text("Delivery Date:", delivery)

        section_title("Load Information")
        row_text("Miles:", row["miles"])
        row_text("Rate:", f"${row['rate']}")
        row_text("RPM:", f"${rpm}/mi")
        row_text("Truck Type:", row["truck_type"])
        row_text("Weight:", f"{row['weight']} lbs")
        row_text("Origin Deadhead:", f"{row['deadhead_origin']} mi")
        row_text("Destination DH:", f"{row['deadhead_destination']} mi")

        section_title("Broker Information")
        row_text("Broker Name:", row["broker_name"])
        row_text("Broker Contact:", row["broker_contact"])

        tk.Button(
            detail_win,
            text="Close",
            bg="#2563eb",
            fg="white",
            width=16,
            height=2,
            bd=0,
            font=("Arial", 10, "bold"),
            command=detail_win.destroy
        ).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = LoadApp(root)
    root.mainloop()