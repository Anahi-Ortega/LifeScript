from dataclasses import dataclass
from typing import List, Dict, Callable

# -----------------------------
# Account Definition
# -----------------------------

@dataclass
class Account:
    name: str
    balance: float
    annual_return: float  # APY or expected market return (e.g. 0.03, 0.07)

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

            # Apply scheduled events
            for event in self.events:
                if event.month == month:
                    event.action(self.accounts)

            # Apply monthly growth
            for account in self.accounts.values():
                account.apply_growth()

            # Record snapshot
            snapshot = {"Month": month}
            for name, account in self.accounts.items():
                snapshot[name] = round(account.balance, 2)
            snapshot["Total"] = round(
                sum(acc.balance for acc in self.accounts.values()), 2
            )

            self.history.append(snapshot)

        return self.history


# -----------------------------
# Example Usage
# -----------------------------

if __name__ == "__main__":

    # ---- Accounts ----
    accounts = {
        "HYSA": Account("HYSA", 19965.12, 0.03),
        "Roth IRA": Account("Roth IRA", 2000.00, 0.07),
        "Brokerage": Account("Brokerage", 0.00, 0.07),
    }

    sim = FinancialSimulation(accounts, months=240)  # 20 years

    # ---- Monthly Contributions ----
    for m in range(1, 241):
        sim.add_event(Event(
            month=m,
            action=lambda accs: accs["HYSA"].deposit(1666.67),
            description="Monthly HYSA contribution"
        ))
        sim.add_event(Event(
            month=m,
            action=lambda accs: accs["Roth IRA"].deposit(1000),
            description="Monthly Roth contribution"
        ))
        sim.add_event(Event(
            month=m,
            action=lambda accs: accs["Brokerage"].deposit(333.33),
            description="Monthly Brokerage contribution"
        ))

    # ---- One-Time Predictable Expense ----
    sim.add_event(Event(
        month=24,  # Example: 2027-ish
        action=lambda accs: accs["HYSA"].withdraw(20000),
        description="Home purchase liquidity hit"
    ))

    # ---- APY Change Example ----
    sim.add_event(Event(
        month=36,
        action=lambda accs: setattr(accs["HYSA"], "annual_return", 0.04),
        description="HYSA rate increases"
    ))

    # ---- Run Simulation ----
    history = sim.run()

    # ---- Output (Yearly Snapshot) ----
    for row in history:
        if row["Month"] % 12 == 0:
            print(row)



"""How You Customize This (Safely)
🔧 Change starting balances
Account("HYSA", 50000, 0.035)

🔧 Add or remove account types

Just add/remove from the accounts dictionary:

"401k": Account("401k", 10000, 0.075)

🔧 Change APY at a future date
Event(
    month=60,
    action=lambda accs: setattr(accs["HYSA"], "annual_return", 0.025)
)

🔧 Add vacations, cars, emergencies
Event(
    month=48,
    action=lambda accs: accs["Brokerage"].withdraw(5000),
    description="Vacation"
)

🔧 Monthly vs Yearly Output

Monthly: print every row

Yearly: if row["Month"] % 12 == 0

You can also export history to CSV later if you want.
"""