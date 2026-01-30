import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass
from typing import Dict, List


# -----------------------------
# Core Logic
# -----------------------------

@dataclass
class Event:
    month: int
    type: str
    account: str
    amount: float = 0.0
    new_apy: float = 0.0
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
    def __init__(self, accounts: Dict[str, Account], months: int, events: List[Event]):
        self.accounts = accounts
        self.months = months
        self.events = events
        self.history = []

    def run(self):
        for month in range(1, self.months + 1):

            # 🔹 Apply events scheduled for this month
            for event in self.events:
                if event.month == month:
                    acc = self.accounts.get(event.account)

                    if not acc:
                        continue  # silently skip invalid accounts

                    if event.type == "deposit":
                        acc.deposit(event.amount)

                    elif event.type == "expense":
                        acc.withdraw(event.amount)

                    elif event.type == "apy_change":
                        acc.annual_return = event.new_apy

            # 🔹 Apply monthly growth
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
        self.events: List[Event] = []
        self.accounts: Dict[str, Account] = {}
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(padx=10, pady=10, fill="x")

        # =============================
        # Account Input Section
        # =============================
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
        ttk.Button(frame, text="Edit Account", command=self.edit_account).grid(row=1, column=4)
        ttk.Button(frame, text="Remove Account", command=self.remove_account).grid(row=1, column=5)

        # =============================
        # Account List Section
        # =============================
        ttk.Label(frame, text="Accounts").grid(row=2, column=0, pady=(10, 0))

        self.account_listbox = tk.Listbox(frame, height=6)
        self.account_listbox.grid(row=3, column=0, columnspan=3, sticky="ew")
        self.account_listbox.bind("<<ListboxSelect>>", self.load_account_for_edit)

        # =============================
        # Simulation Controls
        # =============================
        ttk.Label(frame, text="Months to Simulate").grid(row=4, column=0, pady=(10, 0))
        self.months_entry = ttk.Entry(frame)
        self.months_entry.grid(row=4, column=1)

        ttk.Button(frame, text="Run Simulation", command=self.run_simulation).grid(row=4, column=3)

        # =============================
        # Event Input Section
        # =============================
        ttk.Label(frame, text="Event Month").grid(row=5, column=0, pady=(10, 0))
        ttk.Label(frame, text="Event Type").grid(row=5, column=1, pady=(10, 0))
        ttk.Label(frame, text="Account").grid(row=5, column=2, pady=(10, 0))
        ttk.Label(frame, text="Amount / New APY").grid(row=5, column=3, pady=(10, 0))

        self.event_month_entry = ttk.Entry(frame, width=10)
        self.event_type_combo = ttk.Combobox(
            frame,
            values=["deposit", "expense", "apy_change"],
            state="readonly",
            width=12
        )
        self.event_account_entry = ttk.Entry(frame, width=15)
        self.event_value_entry = ttk.Entry(frame, width=15)

        self.event_month_entry.grid(row=6, column=0)
        self.event_type_combo.grid(row=6, column=1)
        self.event_account_entry.grid(row=6, column=2)
        self.event_value_entry.grid(row=6, column=3)

        ttk.Button(frame, text="Add Event", command=self.add_event).grid(row=6, column=4)
        ttk.Button(frame, text="Edit Event", command=self.edit_event).grid(row=6, column=5)
        ttk.Button(frame, text="Remove Event", command=self.remove_event).grid(row=6, column=6)

        # =============================
        # Event List Section
        # =============================
        ttk.Label(frame, text="Events").grid(row=7, column=0, pady=(10, 0))

        self.event_listbox = tk.Listbox(frame, height=6)
        self.event_listbox.grid(row=8, column=0, columnspan=6, sticky="ew")
        self.event_listbox.bind("<<ListboxSelect>>", self.load_event_for_edit)

        # =============================
        # Output Section
        # =============================
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

    def load_account_for_edit(self, event):
        selection = self.account_listbox.curselection()
        if not selection:
            return

        name = self.account_listbox.get(selection[0])
        account = self.accounts[name]

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, name)

        self.balance_entry.delete(0, tk.END)
        self.balance_entry.insert(0, account.balance)

        self.return_entry.delete(0, tk.END)
        self.return_entry.insert(0, account.annual_return)

    def edit_account(self):
        name = self.name_entry.get().strip()

        if name not in self.accounts:
            messagebox.showerror("Error", "Select an existing account to edit")
            return

        try:
            self.accounts[name].balance = float(self.balance_entry.get())
            self.accounts[name].annual_return = float(self.return_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid account values")
            return

        self.refresh_account_list()
        messagebox.showinfo("Updated", f"Account '{name}' updated")

    def remove_account(self):
        selection = self.account_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Select an account to remove")
            return

        name = self.account_listbox.get(selection[0])

        confirm = messagebox.askyesno(
            "Confirm",
            f"Remove account '{name}' and all its events?"
        )

        if not confirm:
            return

        del self.accounts[name]
        self.events = [e for e in self.events if e.account != name]

        self.refresh_account_list()
        self.refresh_event_list()

    def refresh_account_list(self):
        self.account_listbox.delete(0, tk.END)
        for name in self.accounts:
            self.account_listbox.insert(tk.END, name)

    def add_event(self):
        try:
            month = int(self.event_month_entry.get())
            event_type = self.event_type_combo.get()
            account = self.event_account_entry.get().strip()

            if not account:
                raise ValueError("Account name required")

            if event_type not in ["deposit", "expense", "apy_change"]:
                raise ValueError("Invalid event type")

            if event_type == "apy_change":
                new_apy = float(self.event_value_entry.get())
                event = Event(month, event_type, account, new_apy=new_apy)
            else:
                amount = float(self.event_value_entry.get())
                event = Event(month, event_type, account, amount=amount)

            self.events.append(event)
            messagebox.showinfo("Success", f"Event added for month {month}")

            # Clear inputs
            self.event_month_entry.delete(0, tk.END)
            self.event_account_entry.delete(0, tk.END)
            self.event_value_entry.delete(0, tk.END)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def refresh_event_list(self):
        self.event_listbox.delete(0, tk.END)
        for i, e in enumerate(self.events):
            label = f"{e.month}: {e.description} ({e.account}, {e.amount})"
            self.event_listbox.insert(tk.END, label)

    def edit_event(self):
        selection = self.event_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Select an event to edit")
            return

        try:
            idx = selection[0]
            self.events[idx].month = int(self.event_month_entry.get())
            self.events[idx].amount = float(self.event_amount_entry.get())
            self.events[idx].account = self.event_account_entry.get()
            self.events[idx].description = self.event_desc_entry.get()
        except ValueError:
            messagebox.showerror("Error", "Invalid event values")
            return

        self.refresh_event_list()
        messagebox.showinfo("Updated", "Event updated")

    def remove_event(self):
        selection = self.event_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Select an event to remove")
            return

        index = selection[0]
        del self.events[index]

        self.refresh_event_list()

    def load_event_for_edit(self, event):
        selection = self.event_listbox.curselection()
        if not selection:
            return

        e = self.events[selection[0]]

        self.event_month_entry.delete(0, tk.END)
        self.event_month_entry.insert(0, e.month)

        self.event_amount_entry.delete(0, tk.END)
        self.event_amount_entry.insert(0, e.amount)

        self.event_account_entry.delete(0, tk.END)
        self.event_account_entry.insert(0, e.account)

        self.event_desc_entry.delete(0, tk.END)
        self.event_desc_entry.insert(0, e.description)

    def run_simulation(self):
        try:
            months = int(self.months_entry.get())

            # 🔐 Deep copy accounts so we don't mutate originals
            accounts_copy = {
                name: Account(acc.name, acc.balance, acc.annual_return)
                for name, acc in self.accounts.items()
            }

            sim = FinancialSimulation(accounts_copy, months, self.events)

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
