# IT Helpdesk System V16 (GUI + User Management + SQLite)
# Author: ChatGPT
# Features:
# - Tkinter GUI
# - Login system
# - Admin/User roles
# - Create Users (Admin)
# - Create Tickets
# - View Tickets
# - SQLite database (persistent)

import tkinter as tk
from tkinter import messagebox
import sqlite3
import datetime

# ---------------- DATABASE SETUP ----------------
conn = sqlite3.connect("helpdesk_v16.db")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT,
    role TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_by TEXT,
    title TEXT,
    status TEXT,
    created_at TEXT
)''')

# default admin/user
cursor.execute("INSERT OR IGNORE INTO users VALUES ('admin','admin123','admin')")
cursor.execute("INSERT OR IGNORE INTO users VALUES ('user1','user123','user')")
conn.commit()

current_user = None

# ---------------- LOGIN ----------------
def login():
    global current_user
    u = entry_user.get()
    p = entry_pass.get()

    cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (u,p))
    data = cursor.fetchone()

    if data:
        current_user = u
        messagebox.showinfo("Login", f"Welcome {u}")
        login_window.destroy()
        open_dashboard(data[0])
    else:
        messagebox.showerror("Error", "Invalid credentials")

# ---------------- DASHBOARD ----------------
def open_dashboard(role):
    dash = tk.Tk()
    dash.title("IT Helpdesk V16")
    dash.geometry("400x400")

    tk.Label(dash, text=f"Logged in as: {current_user} ({role})", font=("Arial",12)).pack(pady=10)

    tk.Button(dash, text="Create Ticket", command=create_ticket).pack(pady=5)
    tk.Button(dash, text="View My Tickets", command=view_tickets).pack(pady=5)

    if role == "admin":
        tk.Button(dash, text="Create User", command=create_user).pack(pady=5)
        tk.Button(dash, text="View All Tickets", command=view_all_tickets).pack(pady=5)

    dash.mainloop()

# ---------------- CREATE USER ----------------
def create_user():
    win = tk.Toplevel()
    win.title("Create User")

    tk.Label(win, text="Username").pack()
    u = tk.Entry(win)
    u.pack()

    tk.Label(win, text="Password").pack()
    p = tk.Entry(win)
    p.pack()

    tk.Label(win, text="Role (admin/user)").pack()
    r = tk.Entry(win)
    r.pack()

    def save():
        cursor.execute("INSERT INTO users VALUES (?,?,?)", (u.get(), p.get(), r.get()))
        conn.commit()
        messagebox.showinfo("Success","User created")
        win.destroy()

    tk.Button(win, text="Save", command=save).pack()

# ---------------- CREATE TICKET ----------------
def create_ticket():
    win = tk.Toplevel()
    win.title("Create Ticket")

    tk.Label(win, text="Issue Title").pack()
    t = tk.Entry(win)
    t.pack()

    def save():
        cursor.execute("INSERT INTO tickets (created_by,title,status,created_at) VALUES (?,?,?,?)",
                       (current_user, t.get(), "Open", str(datetime.datetime.now())))
        conn.commit()
        messagebox.showinfo("Success","Ticket Created")
        win.destroy()

    tk.Button(win, text="Submit", command=save).pack()

# ---------------- VIEW TICKETS ----------------
def view_tickets():
    win = tk.Toplevel()
    win.title("My Tickets")

    cursor.execute("SELECT * FROM tickets WHERE created_by=?", (current_user,))
    rows = cursor.fetchall()

    for r in rows:
        tk.Label(win, text=str(r)).pack()

# ---------------- VIEW ALL ----------------
def view_all_tickets():
    win = tk.Toplevel()
    win.title("All Tickets")

    cursor.execute("SELECT * FROM tickets")
    rows = cursor.fetchall()

    for r in rows:
        tk.Label(win, text=str(r)).pack()

# ---------------- LOGIN WINDOW ----------------
login_window = tk.Tk()
login_window.title("Login V16")

entry_user = tk.Entry(login_window)
entry_user.pack()
entry_user.insert(0,"Username")

entry_pass = tk.Entry(login_window, show="*")
entry_pass.pack()
entry_pass.insert(0,"Password")

tk.Button(login_window, text="Login", command=login).pack()

login_window.mainloop()
