import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
import os

# ---------------- Window ----------------
root = tk.Tk()
root.title("IT Helpdesk Ticketing Tool")
root.geometry("900x650")
root.config(bg="#1e1e1e")

# ---------------- Title ----------------
title = tk.Label(
    root,
    text="IT Helpdesk Ticketing Tool",
    font=("Arial", 22, "bold"),
    bg="#1e1e1e",
    fg="white"
)
title.pack(pady=20)

# ---------------- Main Frame ----------------
frame = tk.Frame(root, bg="#2b2b2b", bd=2, relief="ridge")
frame.pack(pady=10, padx=20, fill="both", expand=True)

# ---------------- Labels + Entries ----------------
def make_label(text, row):
    tk.Label(
        frame,
        text=text,
        font=("Arial", 11, "bold"),
        bg="#2b2b2b",
        fg="white"
    ).grid(row=row, column=0, sticky="w", padx=15, pady=10)

# Name
make_label("Employee Name:", 0)
name_entry = tk.Entry(frame, width=35, font=("Arial", 11))
name_entry.grid(row=0, column=1, padx=10)

# Email
make_label("Email ID:", 1)
email_entry = tk.Entry(frame, width=35, font=("Arial", 11))
email_entry.grid(row=1, column=1, padx=10)

# Department
make_label("Department:", 2)
dept_entry = tk.Entry(frame, width=35, font=("Arial", 11))
dept_entry.grid(row=2, column=1, padx=10)

# Issue Type
make_label("Issue Type:", 3)
issue_combo = ttk.Combobox(
    frame,
    width=32,
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
issue_combo.grid(row=3, column=1, padx=10)

# Priority
make_label("Priority:", 4)
priority_combo = ttk.Combobox(
    frame,
    width=32,
    values=["Low", "Medium", "High", "Critical"]
)
priority_combo.grid(row=4, column=1, padx=10)

# Issue Description
make_label("Issue Description:", 5)
desc_text = tk.Text(frame, width=45, height=8, font=("Arial", 10))
desc_text.grid(row=5, column=1, padx=10, pady=10)

# ---------------- Submit Function ----------------
def submit_ticket():
    name = name_entry.get()
    email = email_entry.get()
    dept = dept_entry.get()
    issue = issue_combo.get()
    priority = priority_combo.get()
    desc = desc_text.get("1.0", tk.END).strip()

    if name == "" or email == "" or issue == "":
        messagebox.showerror("Error", "Please fill all required fields")
        return

    file_exists = os.path.isfile("tickets.csv")

    with open("tickets.csv", "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Name",
                "Email",
                "Department",
                "Issue Type",
                "Priority",
                "Description"
            ])

        writer.writerow([
            name,
            email,
            dept,
            issue,
            priority,
            desc
        ])

    messagebox.showinfo("Success", "Ticket Submitted Successfully!")

    # Clear Fields
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    dept_entry.delete(0, tk.END)
    issue_combo.set("")
    priority_combo.set("")
    desc_text.delete("1.0", tk.END)

# ---------------- Button ----------------
submit_btn = tk.Button(
    frame,
    text="Submit Ticket",
    font=("Arial", 12, "bold"),
    bg="#00b894",
    fg="white",
    width=20,
    command=submit_ticket
)
submit_btn.grid(row=6, column=1, pady=20)

# ---------------- Footer ----------------
footer = tk.Label(
    root,
    text="Developed by Ashu",
    bg="#1e1e1e",
    fg="gray",
    font=("Arial", 10)
)
footer.pack(pady=10)

root.mainloop()