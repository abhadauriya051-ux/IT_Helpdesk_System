import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime

# ---------------- WINDOW ----------------
root = tk.Tk()
root.title("IT Helpdesk Ticketing Tool - Version 4")
root.geometry("1250x720")
root.config(bg="#1e1e1e")

FILE_NAME = "tickets.csv"

# ---------------- TITLE ----------------
title = tk.Label(
    root,
    text="IT Helpdesk Ticketing Tool - Admin Dashboard",
    font=("Arial", 22, "bold"),
    bg="#1e1e1e",
    fg="white"
)
title.pack(pady=10)

# ---------------- TOP SEARCH FRAME ----------------
top_frame = tk.Frame(root, bg="#1e1e1e")
top_frame.pack(fill="x", padx=15)

tk.Label(
    top_frame,
    text="Search Ticket:",
    bg="#1e1e1e",
    fg="white",
    font=("Arial", 11, "bold")
).pack(side="left", padx=5)

search_entry = tk.Entry(top_frame, width=35)
search_entry.pack(side="left", padx=5)

# ---------------- MAIN FRAME ----------------
main_frame = tk.Frame(root, bg="#1e1e1e")
main_frame.pack(fill="both", expand=True, padx=15, pady=10)

# LEFT SIDE FORM
form_frame = tk.Frame(main_frame, bg="#2b2b2b", padx=15, pady=15)
form_frame.pack(side="left", fill="y", padx=10)

# RIGHT SIDE TABLE
table_frame = tk.Frame(main_frame, bg="#2b2b2b")
table_frame.pack(side="right", fill="both", expand=True)

# ---------------- LABEL FUNCTION ----------------
def make_label(text, row):
    tk.Label(
        form_frame,
        text=text,
        bg="#2b2b2b",
        fg="white",
        font=("Arial", 10, "bold")
    ).grid(row=row, column=0, sticky="w", pady=8)

# ---------------- FORM ----------------
make_label("Employee Name:", 0)
name_entry = tk.Entry(form_frame, width=28)
name_entry.grid(row=0, column=1)

make_label("Email:", 1)
email_entry = tk.Entry(form_frame, width=28)
email_entry.grid(row=1, column=1)

make_label("Department:", 2)
dept_entry = tk.Entry(form_frame, width=28)
dept_entry.grid(row=2, column=1)

make_label("Issue Type:", 3)
issue_combo = ttk.Combobox(
    form_frame,
    width=25,
    state="readonly",
    values=[
        "Laptop Issue",
        "Printer Issue",
        "Network Issue",
        "Email Issue",
        "Software Issue",
        "VPN Issue",
        "Other"
    ]
)
issue_combo.grid(row=3, column=1)

make_label("Priority:", 4)
priority_combo = ttk.Combobox(
    form_frame,
    width=25,
    state="readonly",
    values=["Low", "Medium", "High", "Critical"]
)
priority_combo.set("Medium")
priority_combo.grid(row=4, column=1)

make_label("Description:", 5)
desc_text = tk.Text(form_frame, width=28, height=6)
desc_text.grid(row=5, column=1)

# ---------------- TABLE ----------------
columns = (
    "Ticket ID",
    "Date",
    "Name",
    "Issue",
    "Priority",
    "Status"
)

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=28
)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=130)

tree.pack(fill="both", expand=True)

# ---------------- FUNCTIONS ----------------
def generate_ticket_id():
    if not os.path.exists(FILE_NAME):
        return "TKT001"

    with open(FILE_NAME, "r") as file:
        rows = list(csv.reader(file))

    if len(rows) <= 1:
        return "TKT001"

    last_id = rows[-1][0]
    num = int(last_id.replace("TKT", ""))
    return f"TKT{num+1:03}"

def load_tickets(keyword=""):
    for row in tree.get_children():
        tree.delete(row)

    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            next(reader, None)

            for row in reader:
                data = " ".join(row).lower()
                if keyword.lower() in data:
                    tree.insert("", "end", values=[
                        row[0],
                        row[1],
                        row[2],
                        row[5],
                        row[6],
                        row[8]
                    ])

def submit_ticket():
    name = name_entry.get()
    email = email_entry.get()
    dept = dept_entry.get()
    issue = issue_combo.get()
    priority = priority_combo.get()
    desc = desc_text.get("1.0", tk.END).strip()

    if name == "" or email == "" or issue == "":
        messagebox.showerror("Error", "Please fill required fields")
        return

    ticket_id = generate_ticket_id()
    date = datetime.now().strftime("%d-%m-%Y %H:%M")
    status = "Open"

    file_exists = os.path.isfile(FILE_NAME)

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Ticket ID",
                "Date",
                "Name",
                "Email",
                "Department",
                "Issue",
                "Priority",
                "Description",
                "Status"
            ])

        writer.writerow([
            ticket_id,
            date,
            name,
            email,
            dept,
            issue,
            priority,
            desc,
            status
        ])

    messagebox.showinfo("Success", f"{ticket_id} Submitted")

    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    dept_entry.delete(0, tk.END)
    issue_combo.set("")
    priority_combo.set("Medium")
    desc_text.delete("1.0", tk.END)

    load_tickets()

def search_ticket():
    keyword = search_entry.get()
    load_tickets(keyword)

def close_ticket():
    selected = tree.selection()

    if not selected:
        messagebox.showerror("Error", "Select a ticket first")
        return

    item = tree.item(selected[0])
    ticket_id = item["values"][0]

    rows = []

    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        rows = list(reader)

    for row in rows:
        if row[0] == ticket_id:
            row[8] = "Closed"

    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    messagebox.showinfo("Updated", f"{ticket_id} Closed")
    load_tickets()

# ---------------- BUTTONS ----------------
submit_btn = tk.Button(
    form_frame,
    text="Submit Ticket",
    width=20,
    bg="#00b894",
    fg="white",
    font=("Arial", 11, "bold"),
    command=submit_ticket
)
submit_btn.grid(row=6, column=1, pady=10)

search_btn = tk.Button(
    top_frame,
    text="Search",
    bg="#0984e3",
    fg="white",
    command=search_ticket
)
search_btn.pack(side="left", padx=5)

close_btn = tk.Button(
    top_frame,
    text="Close Ticket",
    bg="#d63031",
    fg="white",
    command=close_ticket
)
close_btn.pack(side="right", padx=5)

# ---------------- FOOTER ----------------
footer = tk.Label(
    root,
    text="Developed by Ashu | Version 4",
    bg="#1e1e1e",
    fg="gray"
)
footer.pack(pady=5)

load_tickets()
root.mainloop()