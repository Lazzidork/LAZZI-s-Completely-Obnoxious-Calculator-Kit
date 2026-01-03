import tkinter as tk
from tkinter import ttk
from tabs.anti_subscription import AntiSubscriptionTab
from tabs.time_over_expense import TimeOverExpense

__version__ = "1.0.0"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator Hub")

        tabs = ttk.Notebook(self)
        tabs.pack(expand=True, fill="both")

        tabs.add(AntiSubscriptionTab(tabs), text="Anti Subscription Scam")

        tabs.add(TimeOverExpense(tabs), text="Time Over Expense")