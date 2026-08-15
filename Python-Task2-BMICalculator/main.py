import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt


# ============================================================
# DATABASE
# ============================================================

DB_NAME = "bmi.db"


def create_database():
    """Create the BMI records table if it does not exist."""

    try:
        connection = sqlite3.connect(DB_NAME)

        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                bmi REAL NOT NULL,
                category TEXT NOT NULL,
                recorded_at TEXT NOT NULL
            )
        """)

        connection.commit()
        connection.close()

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not create database:\n{error}"
        )


# ============================================================
# BMI CALCULATION
# ============================================================

def calculate_bmi(weight, height):
    """Calculate BMI using weight in kg and height in meters."""

    return weight / (height ** 2)


def get_category(bmi):
    """Return BMI category."""

    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Normal"

    elif bmi < 30:
        return "Overweight"

    else:
        return "Obese"


# ============================================================
# INPUT VALIDATION
# ============================================================

def validate_inputs():
    """Validate user inputs."""

    name = name_entry.get().strip()
    weight_text = weight_entry.get().strip()
    height_text = height_entry.get().strip()

    if not name:
        messagebox.showwarning(
            "Input Error",
            "Please enter a user name."
        )
        return None

    if not weight_text or not height_text:
        messagebox.showwarning(
            "Input Error",
            "Please enter both weight and height."
        )
        return None

    try:
        weight = float(weight_text)
        height = float(height_text)

    except ValueError:
        messagebox.showwarning(
            "Input Error",
            "Weight and height must be numeric values."
        )
        return None

    if weight <= 0:
        messagebox.showwarning(
            "Input Error",
            "Weight must be greater than zero."
        )
        return None

    if height <= 0:
        messagebox.showwarning(
            "Input Error",
            "Height must be greater than zero."
        )
        return None

    if height > 3:
        messagebox.showwarning(
            "Input Error",
            "Please enter height in meters.\n"
            "Example: 1.65"
        )
        return None

    return name, weight, height


# ============================================================
# SAVE RECORD
# ============================================================

def save_record(name, weight, height, bmi, category):
    """Save BMI record into SQLite database."""

    try:
        connection = sqlite3.connect(DB_NAME)

        cursor = connection.cursor()

        recorded_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor.execute("""
            INSERT INTO bmi_records
            (user_name, weight, height, bmi, category, recorded_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            weight,
            height,
            bmi,
            category,
            recorded_at
        ))

        connection.commit()
        connection.close()

        return True

    except sqlite3.Error as error:

        messagebox.showerror(
            "Database Error",
            f"Could not save BMI record:\n{error}"
        )

        return False


# ============================================================
# CALCULATE BUTTON
# ============================================================

def calculate():

    values = validate_inputs()

    if values is None:
        return

    name, weight, height = values

    bmi = calculate_bmi(
        weight,
        height
    )

    category = get_category(
        bmi
    )

    result_label.config(
        text=f"BMI: {bmi:.2f}\nCategory: {category}"
    )

    # Change result appearance
    if category == "Underweight":

        result_label.config(
            background="#fff3cd",
            foreground="#856404"
        )

    elif category == "Normal":

        result_label.config(
            background="#d4edda",
            foreground="#155724"
        )

    elif category == "Overweight":

        result_label.config(
            background="#ffe5b4",
            foreground="#8a4b08"
        )

    else:

        result_label.config(
            background="#f8d7da",
            foreground="#721c24"
        )

    saved = save_record(
        name,
        weight,
        height,
        bmi,
        category
    )

    if saved:

        status_label.config(
            text="BMI calculated and record saved successfully."
        )


# ============================================================
# SHOW HISTORY
# ============================================================

def show_history():

    name = name_entry.get().strip()

    if not name:

        messagebox.showwarning(
            "Input Error",
            "Enter a user name to view history."
        )

        return

    try:

        connection = sqlite3.connect(
            DB_NAME
        )

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                recorded_at,
                weight,
                height,
                bmi,
                category
            FROM bmi_records
            WHERE user_name = ?
            ORDER BY recorded_at DESC
        """, (name,))

        records = cursor.fetchall()

        connection.close()

    except sqlite3.Error as error:

        messagebox.showerror(
            "Database Error",
            f"Could not read BMI history:\n{error}"
        )

        return

    history_window = tk.Toplevel(root)

    history_window.title(
        f"BMI History - {name}"
    )

    history_window.geometry(
        "700x450"
    )

    history_window.configure(
        bg="#f5f7fa"
    )

    title = tk.Label(
        history_window,
        text=f"BMI History - {name}",
        font=("Segoe UI", 18, "bold"),
        bg="#f5f7fa"
    )

    title.pack(
        pady=15
    )

    if not records:

        tk.Label(
            history_window,
            text="No BMI records found for this user.",
            font=("Segoe UI", 12),
            bg="#f5f7fa"
        ).pack(
            pady=30
        )

        return

    columns = (
        "Date",
        "Weight",
        "Height",
        "BMI",
        "Category"
    )

    tree = ttk.Treeview(
        history_window,
        columns=columns,
        show="headings",
        height=14
    )

    for column in columns:

        tree.heading(
            column,
            text=column
        )

        tree.column(
            column,
            width=120,
            anchor="center"
        )

    for record in records:

        tree.insert(
            "",
            tk.END,
            values=(
                record[0],
                f"{record[1]:.1f} kg",
                f"{record[2]:.2f} m",
                f"{record[3]:.2f}",
                record[4]
            )
        )

    tree.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )


# ============================================================
# BMI TREND GRAPH
# ============================================================

def show_graph():

    name = name_entry.get().strip()

    if not name:

        messagebox.showwarning(
            "Input Error",
            "Enter a user name to view the BMI trend."
        )

        return

    try:

        connection = sqlite3.connect(
            DB_NAME
        )

        cursor = connection.cursor()

        cursor.execute("""
            SELECT recorded_at, bmi
            FROM bmi_records
            WHERE user_name = ?
            ORDER BY recorded_at
        """, (name,))

        records = cursor.fetchall()

        connection.close()

    except sqlite3.Error as error:

        messagebox.showerror(
            "Database Error",
            f"Could not read BMI records:\n{error}"
        )

        return

    if not records:

        messagebox.showinfo(
            "No Data",
            "No BMI records found for this user."
        )

        return

    dates = [
        record[0]
        for record in records
    ]

    bmi_values = [
        record[1]
        for record in records
    ]

    plt.figure(
        figsize=(9, 5)
    )

    plt.plot(
        dates,
        bmi_values,
        marker="o"
    )

    plt.axhline(
        18.5,
        linestyle="--",
        label="Underweight limit"
    )

    plt.axhline(
        24.9,
        linestyle="--",
        label="Normal upper limit"
    )

    plt.axhline(
        29.9,
        linestyle="--",
        label="Overweight upper limit"
    )

    plt.title(
        f"BMI Trend - {name}"
    )

    plt.xlabel(
        "Date"
    )

    plt.ylabel(
        "BMI"
    )

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.legend()

    plt.tight_layout()

    plt.show()


# ============================================================
# CLEAR FORM
# ============================================================

def clear_form():

    name_entry.delete(
        0,
        tk.END
    )

    weight_entry.delete(
        0,
        tk.END
    )

    height_entry.delete(
        0,
        tk.END
    )

    result_label.config(
        text="BMI: --\nCategory: --",
        background="#f1f3f5",
        foreground="#333333"
    )

    status_label.config(
        text=""
    )


# ============================================================
# MAIN WINDOW
# ============================================================

create_database()

root = tk.Tk()

root.title(
    "BMI Calculator"
)

root.geometry(
    "650x650"
)

root.minsize(
    600,
    600
)

root.configure(
    bg="#f5f7fa"
)


# ============================================================
# HEADER
# ============================================================

header_frame = tk.Frame(
    root,
    bg="#343a40",
    height=100
)

header_frame.pack(
    fill="x"
)

header_frame.pack_propagate(
    False
)

title_label = tk.Label(
    header_frame,
    text="BMI CALCULATOR",
    font=("Segoe UI", 25, "bold"),
    bg="#343a40",
    fg="white"
)

title_label.pack(
    pady=(15, 0)
)

subtitle_label = tk.Label(
    header_frame,
    text="Track your Body Mass Index",
    font=("Segoe UI", 11),
    bg="#343a40",
    fg="#dddddd"
)

subtitle_label.pack()


# ============================================================
# FORM FRAME
# ============================================================

form_frame = tk.Frame(
    root,
    bg="#f5f7fa"
)

form_frame.pack(
    pady=30
)


# Name

tk.Label(
    form_frame,
    text="User Name",
    font=("Segoe UI", 12, "bold"),
    bg="#f5f7fa"
).grid(
    row=0,
    column=0,
    sticky="w",
    padx=10,
    pady=10
)

name_entry = ttk.Entry(
    form_frame,
    width=30,
    font=("Segoe UI", 12)
)

name_entry.grid(
    row=0,
    column=1,
    padx=10,
    pady=10
)


# Weight

tk.Label(
    form_frame,
    text="Weight (kg)",
    font=("Segoe UI", 12, "bold"),
    bg="#f5f7fa"
).grid(
    row=1,
    column=0,
    sticky="w",
    padx=10,
    pady=10
)

weight_entry = ttk.Entry(
    form_frame,
    width=30,
    font=("Segoe UI", 12)
)

weight_entry.grid(
    row=1,
    column=1,
    padx=10,
    pady=10
)


# Height

tk.Label(
    form_frame,
    text="Height (m)",
    font=("Segoe UI", 12, "bold"),
    bg="#f5f7fa"
).grid(
    row=2,
    column=0,
    sticky="w",
    padx=10,
    pady=10
)

height_entry = ttk.Entry(
    form_frame,
    width=30,
    font=("Segoe UI", 12)
)

height_entry.grid(
    row=2,
    column=1,
    padx=10,
    pady=10
)


# ============================================================
# CALCULATE BUTTON
# ============================================================

calculate_button = tk.Button(
    root,
    text="Calculate BMI",
    command=calculate,
    font=("Segoe UI", 12, "bold"),
    bg="#343a40",
    fg="white",
    activebackground="#495057",
    activeforeground="white",
    padx=25,
    pady=10,
    cursor="hand2"
)

calculate_button.pack(
    pady=10
)


# ============================================================
# RESULT
# ============================================================

result_label = tk.Label(
    root,
    text="BMI: --\nCategory: --",
    font=("Segoe UI", 18, "bold"),
    bg="#f1f3f5",
    fg="#333333",
    width=35,
    height=3
)

result_label.pack(
    pady=15
)


# ============================================================
# STATUS
# ============================================================

status_label = tk.Label(
    root,
    text="",
    font=("Segoe UI", 10),
    bg="#f5f7fa",
    fg="#555555"
)

status_label.pack()


# ============================================================
# ACTION BUTTONS
# ============================================================

button_frame = tk.Frame(
    root,
    bg="#f5f7fa"
)

button_frame.pack(
    pady=20
)


history_button = tk.Button(
    button_frame,
    text="View History",
    command=show_history,
    font=("Segoe UI", 10, "bold"),
    padx=15,
    pady=8,
    cursor="hand2"
)

history_button.grid(
    row=0,
    column=0,
    padx=5
)


graph_button = tk.Button(
    button_frame,
    text="BMI Trend",
    command=show_graph,
    font=("Segoe UI", 10, "bold"),
    padx=15,
    pady=8,
    cursor="hand2"
)

graph_button.grid(
    row=0,
    column=1,
    padx=5
)


clear_button = tk.Button(
    button_frame,
    text="Clear",
    command=clear_form,
    font=("Segoe UI", 10, "bold"),
    padx=15,
    pady=8,
    cursor="hand2"
)

clear_button.grid(
    row=0,
    column=2,
    padx=5
)


# ============================================================
# FOOTER
# ============================================================

footer_label = tk.Label(
    root,
    text="OASIS INFOBYTE | Python Programming Task 2",
    font=("Segoe UI", 9),
    bg="#f5f7fa",
    fg="#777777"
)

footer_label.pack(
    side="bottom",
    pady=10
)


# ============================================================
# START APPLICATION
# ============================================================

root.mainloop()