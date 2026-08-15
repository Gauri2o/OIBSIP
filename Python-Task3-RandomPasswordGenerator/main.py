import tkinter as tk
from tkinter import ttk, messagebox
import secrets
import string
import pyperclip


class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Password Generator")
        self.root.geometry("650x850")
        self.root.resizable(False, False)

        self.history = []

        # Variables
        self.length_var = tk.IntVar(value=16)
        self.uppercase_var = tk.BooleanVar(value=True)
        self.lowercase_var = tk.BooleanVar(value=True)
        self.numbers_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.ambiguous_var = tk.BooleanVar(value=False)

        self.create_widgets()

    # ---------------------------------------------------------
    # GUI
    # ---------------------------------------------------------

    def create_widgets(self):

        title = tk.Label(
            self.root,
            text="🔐 Secure Password Generator",
            font=("Segoe UI", 22, "bold")
        )
        title.pack(pady=(20, 5))

        subtitle = tk.Label(
            self.root,
            text="Generate strong and cryptographically secure passwords",
            font=("Segoe UI", 10)
        )
        subtitle.pack(pady=(0, 20))

        # Password display
        password_frame = tk.Frame(self.root)
        password_frame.pack(fill="x", padx=40)

        self.password_entry = tk.Entry(
            password_frame,
            font=("Consolas", 16),
            justify="center",
            state="readonly"
        )
        self.password_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=8
        )

        copy_button = tk.Button(
            password_frame,
            text="Copy",
            command=self.copy_password,
            font=("Segoe UI", 10, "bold"),
            padx=12
        )
        copy_button.pack(side="right", padx=(8, 0), ipady=7)

        # Strength
        self.strength_label = tk.Label(
            self.root,
            text="Strength: —",
            font=("Segoe UI", 12, "bold")
        )
        self.strength_label.pack(pady=15)

        # Length
        length_frame = tk.LabelFrame(
            self.root,
            text="Password Length",
            font=("Segoe UI", 11, "bold"),
            padx=15,
            pady=10
        )
        length_frame.pack(fill="x", padx=40, pady=10)

        self.length_scale = tk.Scale(
            length_frame,
            from_=8,
            to=64,
            orient="horizontal",
            variable=self.length_var,
            command=self.update_length_label
        )
        self.length_scale.pack(fill="x")

        self.length_label = tk.Label(
            length_frame,
            text="Length: 16",
            font=("Segoe UI", 10)
        )
        self.length_label.pack()

        # Character types
        types_frame = tk.LabelFrame(
            self.root,
            text="Character Types",
            font=("Segoe UI", 11, "bold"),
            padx=15,
            pady=10
        )
        types_frame.pack(fill="x", padx=40, pady=10)

        tk.Checkbutton(
            types_frame,
            text="Uppercase (A-Z)",
            variable=self.uppercase_var
        ).pack(anchor="w")

        tk.Checkbutton(
            types_frame,
            text="Lowercase (a-z)",
            variable=self.lowercase_var
        ).pack(anchor="w")

        tk.Checkbutton(
            types_frame,
            text="Numbers (0-9)",
            variable=self.numbers_var
        ).pack(anchor="w")

        tk.Checkbutton(
            types_frame,
            text="Symbols (!@#$...)",
            variable=self.symbols_var
        ).pack(anchor="w")

        # Ambiguous characters
        tk.Checkbutton(
            self.root,
            text="Exclude ambiguous characters (0, O, l, 1)",
            variable=self.ambiguous_var
        ).pack(pady=10)

        # Generate button
        generate_button = tk.Button(
            self.root,
            text="🔑 Generate Secure Password",
            command=self.generate_password,
            font=("Segoe UI", 12, "bold"),
            padx=20,
            pady=10
        )
        generate_button.pack(pady=10)

        # History
        history_frame = tk.LabelFrame(
            self.root,
            text="Last 5 Generated Passwords (Session Only)",
            font=("Segoe UI", 11, "bold"),
            padx=10,
            pady=10
        )
        history_frame.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=(5, 20)
        )

        self.history_listbox = tk.Listbox(
            history_frame,
            font=("Consolas", 10),
            height=5
        )
        self.history_listbox.pack(
            fill="both",
            expand=True
        )

    # ---------------------------------------------------------
    # Length label
    # ---------------------------------------------------------

    def update_length_label(self, value):
        self.length_label.config(
            text=f"Length: {int(float(value))}"
        )

    # ---------------------------------------------------------
    # Character pool
    # ---------------------------------------------------------

    def get_character_sets(self):

        sets = []

        uppercase = string.ascii_uppercase
        lowercase = string.ascii_lowercase
        numbers = string.digits
        symbols = string.punctuation

        if self.ambiguous_var.get():

            ambiguous = "0Ol1"

            uppercase = "".join(
                char for char in uppercase
                if char not in ambiguous
            )

            lowercase = "".join(
                char for char in lowercase
                if char not in ambiguous
            )

            numbers = "".join(
                char for char in numbers
                if char not in ambiguous
            )

        if self.uppercase_var.get():
            sets.append(uppercase)

        if self.lowercase_var.get():
            sets.append(lowercase)

        if self.numbers_var.get():
            sets.append(numbers)

        if self.symbols_var.get():
            sets.append(symbols)

        return sets

    # ---------------------------------------------------------
    # Generate password
    # ---------------------------------------------------------

    def generate_password(self):

        length = self.length_var.get()

        # Minimum length
        if length < 8:
            messagebox.showerror(
                "Invalid Length",
                "Password length must be at least 8 characters."
            )
            return

        selected_types = sum([
            self.uppercase_var.get(),
            self.lowercase_var.get(),
            self.numbers_var.get(),
            self.symbols_var.get()
        ])

        # At least two character types
        if selected_types < 2:
            messagebox.showerror(
                "Invalid Selection",
                "Please select at least two character types."
            )
            return

        character_sets = self.get_character_sets()

        if length < len(character_sets):
            messagebox.showerror(
                "Invalid Length",
                "Password length is too short for the selected character types."
            )
            return

        # Make sure every selected type appears at least once
        password_characters = [
            secrets.choice(char_set)
            for char_set in character_sets
        ]

        # Combined pool
        pool = "".join(character_sets)

        remaining_length = length - len(password_characters)

        password_characters.extend(
            secrets.choice(pool)
            for _ in range(remaining_length)
        )

        # Cryptographically secure shuffle
        for i in range(len(password_characters) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            password_characters[i], password_characters[j] = (
                password_characters[j],
                password_characters[i]
            )

        password = "".join(password_characters)

        self.display_password(password)
        self.update_strength(password)
        self.add_to_history(password)

        # Automatically copy
        try:
            pyperclip.copy(password)
        except Exception:
            pass

    # ---------------------------------------------------------
    # Display password
    # ---------------------------------------------------------

    def display_password(self, password):

        self.password_entry.config(state="normal")
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        self.password_entry.config(state="readonly")

    # ---------------------------------------------------------
    # Copy password
    # ---------------------------------------------------------

    def copy_password(self):

        password = self.password_entry.get()

        if not password:
            messagebox.showwarning(
                "No Password",
                "Please generate a password first."
            )
            return

        try:
            pyperclip.copy(password)

            messagebox.showinfo(
                "Copied",
                "Password copied to clipboard."
            )

        except Exception as error:
            messagebox.showerror(
                "Clipboard Error",
                f"Could not copy password.\n\n{error}"
            )

    # ---------------------------------------------------------
    # Password strength
    # ---------------------------------------------------------

    def update_strength(self, password):

        score = 0

        length = len(password)

        if length >= 8:
            score += 1

        if length >= 12:
            score += 1

        if length >= 16:
            score += 1

        if any(char.isupper() for char in password):
            score += 1

        if any(char.islower() for char in password):
            score += 1

        if any(char.isdigit() for char in password):
            score += 1

        if any(char in string.punctuation for char in password):
            score += 1

        if score <= 3:
            strength = "Weak"
        elif score <= 5:
            strength = "Medium"
        else:
            strength = "Strong"

        self.strength_label.config(
            text=f"Strength: {strength}"
        )

    # ---------------------------------------------------------
    # History
    # ---------------------------------------------------------

    def add_to_history(self, password):

        self.history.insert(0, password)

        # Keep only last 5
        self.history = self.history[:5]

        self.history_listbox.delete(0, tk.END)

        for item in self.history:
            self.history_listbox.insert(tk.END, item)


# -------------------------------------------------------------
# Application
# -------------------------------------------------------------

if __name__ == "__main__":

    root = tk.Tk()

    app = PasswordGenerator(root)

    root.mainloop()