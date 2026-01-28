from dataclasses import dataclass
from typing import Dict, Callable, List


# -----------------------------
# Account Definition
# -----------------------------

@dataclass
class Account:
    name: str
    balance: float
    annual_return: float

    def monthly_return(self) -> float:
        return (1 + self.annual_return) ** (1 / 12) - 1

    def apply_growth(self):
        self.balance *= (1 + self.monthly_return())

    def deposit(self, amount: float):
        self.balance += amount

    def withdraw(self, amount: float):
        self.balance -= amount


# -----------------------------
# Event Definition
# -----------------------------

@dataclass
class Event:
    month: int
    action: Callable[[Dict[str, Account]], None]
    description: str = ""


# -----------------------------
# Simulation Engine
# -----------------------------

class FinancialSimulation:
    def __init__(self, accounts: Dict[str, Account], months: int):
        self.accounts = accounts
        self.months = months
        self.events: List[Event] = []
        self.history: List[Dict[str, float]] = []

    def add_event(self, event: Event):
        self.events.append(event)

    def run(self):
        for month in range(1, self.months + 1):

            # Apply events
            for event in self.events:
                if event.month == month:
                    event.action(self.accounts)

            # Apply growth
            for account in self.accounts.values():
                account.apply_growth()

            # Snapshot
            snapshot = {"Month": month}
            for name, acc in self.accounts.items():
                snapshot[name] = round(acc.balance, 2)
            snapshot["Total"] = round(sum(a.balance for a in self.accounts.values()), 2)

            self.history.append(snapshot)

        return self.history


# -----------------------------
# Console Input Helpers
# -----------------------------

def get_float(prompt: str) -> float:
    return float(input(prompt))


def get_int(prompt: str) -> int:
    return int(input(prompt))


# -----------------------------
# Main Program
# -----------------------------

if __name__ == "__main__":

    print("\n=== Financial Simulation Setup ===\n")

    # ---- Timeline ----
    months = get_int("How many months do you want to simulate? ")

    # ---- Accounts ----
    accounts: Dict[str, Account] = {}
    num_accounts = get_int("\nHow many accounts do you want to model? ")

    for i in range(num_accounts):
        print(f"\nAccount #{i + 1}")
        name = input("Account name: ")
        balance = get_float("Starting balance: ")
        annual_return = get_float("Annual return / APY (e.g. 0.03, 0.07): ")
        accounts[name] = Account(name, balance, annual_return)

    sim = FinancialSimulation(accounts, months)

    # ---- Monthly Contributions ----
    print("\n=== Monthly Contributions ===")
    for name in accounts:
        amount = get_float(f"Monthly contribution to {name} (0 if none): ")
        if amount > 0:
            for m in range(1, months + 1):
                sim.add_event(Event(
                    month=m,
                    action=lambda accs, n=name, a=amount: accs[n].deposit(a),
                    description=f"Monthly contribution to {name}"
                ))

    # ---- Predictable Expenses ----
    print("\n=== Predictable One-Time Expenses ===")
    add_expenses = input("Do you want to add predictable expenses? (y/n): ").lower()

    while add_expenses == "y":
        exp_month = get_int("Expense month number: ")
        exp_amount = get_float("Expense amount: ")
        exp_account = input("Which account should it come from? ")

        sim.add_event(Event(
            month=exp_month,
            action=lambda accs, n=exp_account, a=exp_amount: accs[n].withdraw(a),
            description="Predictable expense"
        ))

        add_expenses = input("Add another expense? (y/n): ").lower()

    # ---- APY / Return Changes ----
    print("\n=== Return Changes ===")
    add_changes = input("Do you want to schedule APY/return changes? (y/n): ").lower()

    while add_changes == "y":
        change_month = get_int("Month of change: ")
        acct = input("Account name: ")
        new_rate = get_float("New annual return/APY: ")

        sim.add_event(Event(
            month=change_month,
            action=lambda accs, n=acct, r=new_rate: setattr(accs[n], "annual_return", r),
            description="Return change"
        ))

        add_changes = input("Add another rate change? (y/n): ").lower()

    # ---- Output Preference ----
    print("\n=== Output Preference ===")
    output_mode = input("Output monthly or yearly? (m/y): ").lower()

    # ---- Run ----
    history = sim.run()

    print("\n=== Simulation Results ===\n")
    for row in history:
        if output_mode == "m" or row["Month"] % 12 == 0:
            print(row)
