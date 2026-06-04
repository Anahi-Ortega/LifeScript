# Financial Simulation GUI

A desktop application for modeling personal finances, investment growth, savings goals, recurring contributions, and future financial events.

## Features

- Create and manage multiple financial accounts
- Assign individual annual return rates (APY or expected market return)
- Set recurring monthly contributions for each account
- Schedule future financial events:
  - Deposits
  - Expenses/Withdrawals
  - APY Changes
- Simulate account growth over a custom time period
- View account balances month-by-month
- Visualize growth with charts
- Edit and remove accounts or events at any time

---

# Getting Started

## Creating an Account

1. Enter an **Account Name**
   - Example: HYSA, Roth IRA, Brokerage

2. Enter the **Starting Balance**
   - Current value of the account

3. Enter the **Annual Return**
   - Expressed as a decimal
   - Examples:
     - 3% APY = `0.03`
     - 7% expected market return = `0.07`
     - 10% expected market return = `0.10`

4. Enter the **Monthly Contribution**
   - Amount automatically added every month during the simulation
   - Example: `500`

5. Click **Add Account**

The account will appear in the Accounts list.

---

# Editing an Account

1. Select an account from the Accounts list.
2. The account information will populate the input fields.
3. Modify any values.
4. Click **Edit Account**.

Changes will immediately update the stored account.

---

# Removing an Account

1. Select an account from the Accounts list.
2. Click **Remove Account**.
3. Confirm the deletion.

All events associated with that account will also be removed.

---

# Setting the Simulation Length

Enter the number of months to simulate.

Examples:

| Goal | Months |
|--------|--------|
| 1 Year | 12 |
| 5 Years | 60 |
| 10 Years | 120 |
| 20 Years | 240 |

---

# Creating Events

Events allow future changes to be scheduled.

## Deposit Event

Adds money to an account on a specific month.

Example:

| Field | Value |
|---------|---------|
| Month | 6 |
| Type | deposit |
| Account | Brokerage |
| Amount | 5000 |

Adds $5,000 during Month 6.

---

## Expense Event

Removes money from an account on a specific month.

Example:

| Field | Value |
|---------|---------|
| Month | 18 |
| Type | expense |
| Account | HYSA |
| Amount | 20000 |

Useful for:

- Home down payments
- Vacations
- Vehicle purchases
- Major expenses

---

## APY Change Event

Changes an account's annual return beginning in a specific month.

Example:

| Field | Value |
|---------|---------|
| Month | 24 |
| Type | apy_change |
| Account | HYSA |
| New APY | 0.04 |

Changes the account to a 4% APY starting in Month 24.

---

# Event Validation

The application validates:

- Account existence
- Valid month range
- Positive deposit amounts
- Positive expense amounts
- APY values between 0 and 1
- Available balance for withdrawals

Invalid entries will generate a popup message explaining the issue.

---

# Running a Simulation

1. Create one or more accounts.
2. Set the simulation length.
3. Add any future events.
4. Click **Run Simulation**.

The application will:

- Apply recurring contributions
- Apply scheduled events
- Apply monthly growth
- Calculate balances for each month
- Display results
- Generate charts

---

# Understanding Results

Each row represents one month.

Example:

```text
{'Month': 12,
 'HYSA': 45231.12,
 'Brokerage': 18522.88,
 'Roth IRA': 16490.22,
 'Total': 80244.22}
