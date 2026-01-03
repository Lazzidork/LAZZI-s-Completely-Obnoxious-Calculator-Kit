import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

root = tk.Tk()
root.title("Calculator Hub")

tabs = ttk.Notebook(root)
tabs.pack(expand=True, fill="both")

# Tab 1
sub_tab = ttk.Frame(tabs)
tabs.add(sub_tab, text="Anti Subscription Scam")

#***************************************************

#func goes here
#debug, delete later
def show():
    print(price_entry.get(), period.get())

#******************************

#func to get plan info from user
def add_plan():
    name = name_entry.get()
    raw_price = price_entry.get()
    selected_period = period.get()

    if name in ("", "NAME HERE"):
        messagebox.showerror("Error", "Enter a name")
        return

    if raw_price in ("", "PRICE HERE"):
        messagebox.showerror("Error", "Enter a price")
        return

    try:
        price = float(raw_price)
    except ValueError:
        messagebox.showerror("Error", "Price must be a number")
        return

    # normalize to yearly
    if selected_period == "daily":
        yearly = price * 365
    elif selected_period == "monthly":
        yearly = price * 12
    else:
        yearly = price

    monthly = yearly / 12
    daily = yearly / 365

    plans.append({
        "name": name,
        "daily": daily,
        "monthly": monthly,
        "yearly": yearly,
        "source": selected_period 
    })

    update_table()


#*******************************************

#for updating the display
def update_table():
    # clear table
    for row in table.get_children():
        table.delete(row)

    # sort by cheapest yearly
    sorted_plans = sorted(plans, key=lambda x: x["yearly"])

    # insert rows
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

        table.insert(
            "",
            "end",
            values=(i, plan["name"], daily, monthly, yearly),
            tags=tags
        )




#*******************************************************

#deleting crap
def delete_selected():
    selected = table.selection()

    if not selected:
        messagebox.showerror("Error", "No item selected")
        return

    # get rank from selected row (rank is first column)
    item = table.item(selected[0])
    rank = item["values"][0]  # 1-based rank

    # remove from plans (sorted order)
    sorted_plans = sorted(plans, key=lambda x: x["yearly"])
    plan_to_delete = sorted_plans[rank - 1]

    plans.remove(plan_to_delete)
    update_table()
    
def remove_all():
    if not plans:
        messagebox.showerror("Error", "Nothing to remove")
        return

    plans.clear()
    update_table()


#*************************************************
#input
#name entry
name_entry = tk.Entry(sub_tab, fg="gray")
name_entry.pack()

name_entry.insert(0, "NAME HERE")

def clear_name_placeholder(event):
    if name_entry.get() == "NAME HERE":
        name_entry.delete(0, tk.END)
        name_entry.config(fg="black")

def restore_name_placeholder(event):
    if not name_entry.get():
        name_entry.insert(0, "NAME HERE")
        name_entry.config(fg="gray")

name_entry.bind("<FocusIn>", clear_name_placeholder)
name_entry.bind("<FocusOut>", restore_name_placeholder)

#period entry
period = tk.StringVar(value="monthly")
tk.OptionMenu(sub_tab, period, "daily", "monthly", "yearly").pack()

#price entry

price_entry = tk.Entry(sub_tab, fg="gray")
price_entry.pack()

price_entry.insert(0, "PRICE HERE")

def clear_price_placeholder(event):
    if price_entry.get() == "PRICE HERE":
        price_entry.delete(0, tk.END)
        price_entry.config(fg="black")

def restore_price_placeholder(event):
    if not price_entry.get():
        price_entry.insert(0, "PRICE HERE")
        price_entry.config(fg="gray")

price_entry.bind("<FocusIn>", clear_price_placeholder)
price_entry.bind("<FocusOut>", restore_price_placeholder)

#******************************************************

#display
columns = ("rank", "name", "daily", "monthly", "yearly")

table = ttk.Treeview(sub_tab, columns=columns, show="headings")
table.pack(fill="both", expand=True)

table.heading("rank", text="Rank")
table.heading("name", text="Name")
table.heading("daily", text="Daily")
table.heading("monthly", text="Monthly")
table.heading("yearly", text="Yearly")
table.column("rank", width=50, anchor="center", stretch=False)
table.column("name", width=120, stretch=False)
table.column("daily", width=80, stretch=False)
table.column("monthly", width=80, stretch=False)
table.column("yearly", width=80, stretch=False)

#************************************************************

#dict for plan
plans = []

#******************************************

#the ever important 'add' button:
tk.Button(sub_tab, text="Add", command=add_plan).pack()

#the ever important 'delete item' button
tk.Button(sub_tab, text="Delete Selected", command=delete_selected).pack()
tk.Button(sub_tab, text="Remove All", command=remove_all).pack()

#*********************************

#highlight cheapest option
table.tag_configure(
    "cheapest",
    background="#d1fae5"
)

#original type
table.tag_configure("source_daily", background="#e0f2fe")
table.tag_configure("source_monthly", background="#fef3c7")
table.tag_configure("source_yearly", background="#ede9fe")



# Tab 2
date_tab = ttk.Frame(tabs)
tabs.add(date_tab, text="Dates")

tk.Label(date_tab, text="Date Calculator PLANNED").pack()

root.mainloop()
