import copy
import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass
from typing import Dict, List, Callable


# -----------------------------
# Core Logic (Same as Before)
# -----------------------------

@dataclass
class Account:
    name: str
    balance: float
    annual_return: float

    def monthly_return(self):
        return (1 + self.annual_return) ** (1 / 12) - 1

    def apply_growth(self):
        self.balance *= (1 + self.monthly_return())

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount


class FinancialSimulation:
    def __init__(self, accounts: Dict[str, Account], months: int):
        self.accounts = accounts
        self.months = months
        self.history = []

    def run(self):
        for month in range(1, self.months + 1):
            for acc in self.accounts.values():
                acc.apply_growth()

            snapshot = {"Month": month}
            for name, acc in self.accounts.items():
                snapshot[name] = round(acc.balance, 2)
            snapshot["Total"] = round(sum(a.balance for a in self.accounts.values()), 2)

            self.history.append(snapshot)

        return self.history


# -----------------------------
# GUI
# -----------------------------

class FinanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Financial Simulation")
        self.geometry("700x500")

        self.accounts: Dict[str, Account] = {}

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(frame, text="Account Name").grid(row=0, column=0)
        ttk.Label(frame, text="Starting Balance").grid(row=0, column=1)
        ttk.Label(frame, text="Annual Return").grid(row=0, column=2)

        self.name_entry = ttk.Entry(frame)
        self.balance_entry = ttk.Entry(frame)
        self.return_entry = ttk.Entry(frame)

        self.name_entry.grid(row=1, column=0)
        self.balance_entry.grid(row=1, column=1)
        self.return_entry.grid(row=1, column=2)

        ttk.Button(frame, text="Add Account", command=self.add_account).grid(row=1, column=3)

        ttk.Label(frame, text="Months to Simulate").grid(row=2, column=0)
        self.months_entry = ttk.Entry(frame)
        self.months_entry.grid(row=2, column=1)

        ttk.Button(frame, text="Run Simulation", command=self.run_simulation).grid(row=2, column=3)

        self.output = tk.Text(self, height=20)
        self.output.pack(padx=10, pady=10, fill="both", expand=True)

    def add_account(self):
        try:
            name = self.name_entry.get().strip()  # Added .strip() to catch whitespace-only names

            # 1. Validate name first
            if not name:
                raise ValueError("Account name required")

            # 2. Convert numerical inputs
            balance = float(self.balance_entry.get())
            annual_return = float(self.return_entry.get())

            # 3. Create the account
            self.accounts[name] = Account(name, balance, annual_return)
            messagebox.showinfo("Success", f"Added account: {name}")

            # 4. Clear entries
            self.name_entry.delete(0, tk.END)
            self.balance_entry.delete(0, tk.END)
            self.return_entry.delete(0, tk.END)

        except ValueError as e:
            # This will now catch both empty names and non-numeric inputs
            error_msg = str(e) if str(e) else "Invalid input. Please enter numbers for balance and return."
            messagebox.showerror("Error", error_msg)


    def run_simulation(self):
        try:
            months = int(self.months_entry.get())

            # 🔐 Deep copy accounts so we don't mutate originals
            accounts_copy = {
                name: Account(acc.name, acc.balance, acc.annual_return)
                for name, acc in self.accounts.items()
            }

            sim = FinancialSimulation(accounts_copy, months)
            history = sim.run()

            self.output.delete("1.0", tk.END)
            for row in history:
                self.output.insert(tk.END, f"{row}\n")

        except ValueError:
            messagebox.showerror("Error", "Invalid months")


# -----------------------------
# Run App
# -----------------------------

if __name__ == "__main__":
    app = FinanceApp()
    app.mainloop()
