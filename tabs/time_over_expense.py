import tkinter as tk
from tkinter import ttk, messagebox

class TimeOverExpense(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # ---------- INPUT ------------
        self.period = tk.StringVar(value="monthly")
        tk.OptionMenu(self, self.period, "hourly", "monthly", "yearly").pack()

        self.income_entry = tk.Entry(self, fg="gray")
        self.income_entry.pack()
        self.income_entry.insert(0, "INCOME HERE")

        self.income_entry.bind("<FocusIn>", self.clear_income)
        self.income_entry.bind("<FocusOut>", self.restore_income)

        self.price_entry = tk.Entry(self, fg="gray")
        self.price_entry.pack()
        self.price_entry.insert(0, "PRICE HERE")

        self.price_entry.bind("<FocusIn>", self.clear_price)
        self.price_entry.bind("<FocusOut>", self.restore_price)

        # ---------- BUTTONS ----------------
        tk.Button(self, text="Calculate!", command=self.do_shit).pack()

        # ------------OUTPUT BOX--------------
        self.output_box = tk.Text(self, height=10, width=40, font=('arial', 14))
        self.output_box.pack(fill='both', expand=True)

    # -------- PLACEHOLDERS ---------
    def clear_income(self, _):
        if self.income_entry.get() == "INCOME HERE":
            self.income_entry.delete(0, tk.END)
            self.income_entry.config(fg="black")

    def restore_income(self, _):
        if not self.income_entry.get():
            self.income_entry.insert(0, "INCOME HERE")
            self.income_entry.config(fg="gray")

    def clear_price(self, _):
        if self.price_entry.get() == "PRICE HERE":
            self.price_entry.delete(0, tk.END)
            self.price_entry.config(fg="black")

    def restore_price(self, _):
        if not self.price_entry.get():
            self.price_entry.insert(0, "PRICE HERE")
            self.price_entry.config(fg="gray")

    #------------ LOGIC ----------------
    def do_shit(self):
        raw_income = self.income_entry.get()
        raw_price = self.price_entry.get()
        period = self.period.get()

        try:
            income = float(raw_income)
        except ValueError:
            messagebox.showerror("Error", "Income must be a number")
            return

        try:
            price = float(raw_price)
        except ValueError:
            messagebox.showerror("Error", "Price must be a number")
            return

        if income == 0:
            messagebox.showerror("Error", "User do not have income")
            return

        if price == 0:
            messagebox.showerror("Error", "Price cannot be zero")

    #-------------Converting data ----------
        if period == "monthly":
            hours_per_period = 174
        elif period == "yearly":
            hours_per_period = 174 * 12  # 2088
        elif period == "hourly":
            hours_per_period = 1
        else:
            messagebox.showerror("Error", f"Unknown period: {period}")
            return

        hourly = income / hours_per_period
        total_hours = price / hourly

        # --- Split into hours + leftover minutes ---
        hours_int = int(total_hours)
        minutes_int = round((total_hours - hours_int) * 60)

        rounded_hourly = round(hourly, 2)




        #print(f"you make {rounded_hourly} hourly, and it will cost you {rounded_hours} hours")

        self.output_box.delete('1.0', tk.END)  # clear old stuff

        # --- Build output message ---
        if hours_int >= 1:
            msg = f"You make {rounded_hourly} hourly, and it will cost you {hours_int} hour"
            if hours_int != 1:
                msg += "s"
            if minutes_int > 0:
                msg += f" and {minutes_int} minute{'s' if minutes_int != 1 else ''}"
        else:
            msg = f"You make {rounded_hourly} hourly, and it will cost you {minutes_int} minute{'s' if minutes_int != 1 else ''}"

        self.output_box.insert(tk.END, msg)