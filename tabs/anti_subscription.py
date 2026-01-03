import tkinter as tk
from tkinter import ttk, messagebox

class AntiSubscriptionTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.plans = []

        # ---------- INPUT ------------
        self.name_entry = tk.Entry(self, fg="gray")
        self.name_entry.pack()
        self.name_entry.insert(0, "NAME HERE")

        self.name_entry.bind("<FocusIn>", self.clear_name)
        self.name_entry.bind("<FocusOut>", self.restore_name)

        self.period = tk.StringVar(value="monthly")
        tk.OptionMenu(self, self.period, "daily", "monthly", "yearly").pack()

        self.price_entry = tk.Entry(self, fg="gray")
        self.price_entry.pack()
        self.price_entry.insert(0, "PRICE HERE")

        self.price_entry.bind("<FocusIn>", self.clear_price)
        self.price_entry.bind("<FocusOut>", self.restore_price)

        # --------- TABLE -----------
        columns = ("rank", "name", "daily", "monthly", "yearly")
        self.table = ttk.Treeview(self, columns=columns, show="headings")
        self.table.pack(fill="both", expand=True)

        for col in columns:
            self.table.heading(col, text=col.capitalize())

        self.table.column("rank", width=50, anchor="center", stretch=False)

        # -------- TAGS ---------
        self.table.tag_configure("cheapest", background="#d1fae5")

        # ---------- BUTTONS --------------
        tk.Button(self, text="Add", command=self.add_plan).pack()
        tk.Button(self, text="Delete Selected", command=self.delete_selected).pack()
        tk.Button(self, text="Remove All", command=self.remove_all).pack()

    # -------- PLACEHOLDERS ---------
    def clear_name(self, _):
        if self.name_entry.get() == "NAME HERE":
            self.name_entry.delete(0, tk.END)
            self.name_entry.config(fg="black")

    def restore_name(self, _):
        if not self.name_entry.get():
            self.name_entry.insert(0, "NAME HERE")
            self.name_entry.config(fg="gray")

    def clear_price(self, _):
        if self.price_entry.get() == "PRICE HERE":
            self.price_entry.delete(0, tk.END)
            self.price_entry.config(fg="black")

    def restore_price(self, _):
        if not self.price_entry.get():
            self.price_entry.insert(0, "PRICE HERE")
            self.price_entry.config(fg="gray")

    # ----------- LOGIC -------------
    def add_plan(self):
        name = self.name_entry.get()
        raw_price = self.price_entry.get()
        period = self.period.get()

        if name in ("", "NAME HERE"):
            messagebox.showerror("Error", "Enter a name")
            return

        try:
            price = float(raw_price)
        except ValueError:
            messagebox.showerror("Error", "Price must be a number")
            return

        yearly = price * (365 if period == "daily" else 12 if period == "monthly" else 1)

        self.plans.append({
            "name": name,
            "daily": yearly / 365,
            "monthly": yearly / 12,
            "yearly": yearly,
            "source": period
        })

        self.update_table()

    def update_table(self):
        self.table.delete(*self.table.get_children())
        sorted_plans = sorted(self.plans, key=lambda x: x["yearly"])

        for i, plan in enumerate(sorted_plans, start=1):

            daily = f"{plan['daily']:.2f}"

            monthly = f"{plan['monthly']:.2f}"

            yearly = f"{plan['yearly']:.2f}"

            if plan["source"] == "daily":

                daily = "⭐ " + daily

            elif plan["source"] == "monthly":

                monthly = "⭐ " + monthly

            else:

                yearly = "⭐ " + yearly

            tags = ("cheapest",) if i == 1 else ()

            self.table.insert(

                "",

                "end",

                values=(i, plan["name"], daily, monthly, yearly),

                tags=tags

            )

    def delete_selected(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showerror("Error", "No item selected")
            return

        rank = self.table.item(selected[0])["values"][0]
        plan = sorted(self.plans, key=lambda x: x["yearly"])[rank - 1]
        self.plans.remove(plan)
        self.update_table()

    def remove_all(self):
        self.plans.clear()
        self.update_table()
