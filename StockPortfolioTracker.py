import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt


# Store portfolio data
portfolio = []


# ---------------- ADD STOCK ----------------
def add_stock():

    symbol = symbol_entry.get().upper().strip()
    quantity = quantity_entry.get().strip()
    buy_price = buy_price_entry.get().strip()
    current_price = current_price_entry.get().strip()

    if symbol == "" or quantity == "" or buy_price == "" or current_price == "":
        messagebox.showerror("Error", "Please enter all details")
        return

    try:
        quantity = int(quantity)
        buy_price = float(buy_price)
        current_price = float(current_price)

        if quantity <= 0 or buy_price <= 0 or current_price <= 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Error",
            "Please enter valid numbers"
        )
        return

    investment = quantity * buy_price
    current_value = quantity * current_price
    profit_loss = current_value - investment

    portfolio.append({
        "symbol": symbol,
        "quantity": quantity,
        "buy_price": buy_price,
        "current_price": current_price,
        "investment": investment,
        "current_value": current_value,
        "profit_loss": profit_loss
    })

    # Clear input fields
    symbol_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    buy_price_entry.delete(0, tk.END)
    current_price_entry.delete(0, tk.END)

    display_portfolio()


# ---------------- DISPLAY PORTFOLIO ----------------
def display_portfolio():

    # Clear old table
    for row in table.get_children():
        table.delete(row)

    total_investment = 0
    total_value = 0
    total_profit_loss = 0

    for stock in portfolio:

        table.insert(
            "",
            tk.END,
            values=(
                stock["symbol"],
                stock["quantity"],
                f"₹{stock['buy_price']:.2f}",
                f"₹{stock['current_price']:.2f}",
                f"₹{stock['current_value']:.2f}",
                f"₹{stock['profit_loss']:.2f}"
            )
        )

        total_investment += stock["investment"]
        total_value += stock["current_value"]
        total_profit_loss += stock["profit_loss"]

    investment_label.config(
        text=f"Total Investment: ₹{total_investment:.2f}"
    )

    value_label.config(
        text=f"Current Value: ₹{total_value:.2f}"
    )

    profit_label.config(
        text=f"Total Profit/Loss: ₹{total_profit_loss:.2f}"
    )


# ---------------- DELETE STOCK ----------------
def delete_stock():

    selected = table.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a stock to delete"
        )
        return

    selected_item = table.item(selected[0])
    symbol = selected_item["values"][0]

    for stock in portfolio:
        if stock["symbol"] == symbol:
            portfolio.remove(stock)
            break

    display_portfolio()


# ---------------- SHOW CHART ----------------
def show_chart():

    if len(portfolio) == 0:
        messagebox.showwarning(
            "Warning",
            "Please add stocks first"
        )
        return

    symbols = []
    values = []

    for stock in portfolio:
        symbols.append(stock["symbol"])
        values.append(stock["current_value"])

    plt.figure(figsize=(8, 5))

    plt.bar(symbols, values)

    plt.title("Stock Portfolio Value")
    plt.xlabel("Stocks")
    plt.ylabel("Current Value (₹)")

    plt.tight_layout()
    plt.show()


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()

root.title("Stock Portfolio Tracker")

root.geometry("1000x650")


# Title
title = tk.Label(
    root,
    text="Stock Portfolio Tracker",
    font=("Arial", 24, "bold")
)

title.pack(pady=15)


# ---------------- INPUT FRAME ----------------

input_frame = tk.Frame(root)

input_frame.pack(pady=10)


# Stock Symbol
tk.Label(
    input_frame,
    text="Stock Symbol"
).grid(row=0, column=0, padx=8)

symbol_entry = tk.Entry(
    input_frame,
    width=15
)

symbol_entry.grid(row=1, column=0, padx=8)


# Quantity
tk.Label(
    input_frame,
    text="Quantity"
).grid(row=0, column=1, padx=8)

quantity_entry = tk.Entry(
    input_frame,
    width=15
)

quantity_entry.grid(row=1, column=1, padx=8)


# Buy Price
tk.Label(
    input_frame,
    text="Buy Price"
).grid(row=0, column=2, padx=8)

buy_price_entry = tk.Entry(
    input_frame,
    width=15
)

buy_price_entry.grid(row=1, column=2, padx=8)


# Current Price
tk.Label(
    input_frame,
    text="Current Price"
).grid(row=0, column=3, padx=8)

current_price_entry = tk.Entry(
    input_frame,
    width=15
)

current_price_entry.grid(row=1, column=3, padx=8)


# Add button
add_button = tk.Button(
    input_frame,
    text="Add Stock",
    command=add_stock
)

add_button.grid(
    row=1,
    column=4,
    padx=10
)


# ---------------- TABLE ----------------

columns = (
    "Symbol",
    "Quantity",
    "Buy Price",
    "Current Price",
    "Current Value",
    "Profit/Loss"
)

table = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=12
)

for column in columns:

    table.heading(
        column,
        text=column
    )

    table.column(
        column,
        width=140
    )

table.pack(pady=20)


# ---------------- SUMMARY ----------------

investment_label = tk.Label(
    root,
    text="Total Investment: ₹0.00",
    font=("Arial", 14, "bold")
)

investment_label.pack(pady=3)


value_label = tk.Label(
    root,
    text="Current Value: ₹0.00",
    font=("Arial", 14, "bold")
)

value_label.pack(pady=3)


profit_label = tk.Label(
    root,
    text="Total Profit/Loss: ₹0.00",
    font=("Arial", 14, "bold")
)

profit_label.pack(pady=3)


# ---------------- BUTTONS ----------------

button_frame = tk.Frame(root)

button_frame.pack(pady=15)


delete_button = tk.Button(
    button_frame,
    text="Delete Selected Stock",
    command=delete_stock
)

delete_button.grid(
    row=0,
    column=0,
    padx=10
)


chart_button = tk.Button(
    button_frame,
    text="View Portfolio Chart",
    command=show_chart
)

chart_button.grid(
    row=0,
    column=1,
    padx=10
)


# Start application
root.mainloop()