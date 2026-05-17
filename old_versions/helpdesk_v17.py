import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3, datetime

DB='helpdesk_v17.db'
conn=sqlite3.connect(DB)
cur=conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY,password TEXT,role TEXT)')
cur.execute('CREATE TABLE IF NOT EXISTS tickets(id INTEGER PRIMARY KEY AUTOINCREMENT,created_by TEXT,title TEXT,status TEXT,created_at TEXT)')
cur.execute("INSERT OR IGNORE INTO users VALUES('admin','admin123','admin')")
cur.execute("INSERT OR IGNORE INTO users VALUES('user1','user123','user')")
conn.commit()

current_user=None
current_role=None

root=tk.Tk()
root.title('IT Helpdesk V17')
root.geometry('900x600')
root.configure(bg='#1e1e1e')

style=ttk.Style()
style.theme_use('clam')
style.configure('TButton',padding=8)
style.configure('TLabel',background='#1e1e1e',foreground='white',font=('Arial',11))

main=tk.Frame(root,bg='#1e1e1e')
main.pack(fill='both',expand=True)


def clear():
    for w in main.winfo_children(): w.destroy()


def login_screen():
    clear()
    box=tk.Frame(main,bg='#2b2b2b',padx=20,pady=20)
    box.place(relx=.5,rely=.5,anchor='center')
    tk.Label(box,text='IT Helpdesk Login',bg='#2b2b2b',fg='white',font=('Arial',16,'bold')).pack(pady=10)
    u=tk.Entry(box,width=30)
    u.pack(pady=5)
    u.insert(0,'admin')
    p=tk.Entry(box,width=30,show='*')
    p.pack(pady=5)
    p.insert(0,'admin123')
    def do_login():
        global current_user,current_role
        cur.execute('SELECT role FROM users WHERE username=? AND password=?',(u.get(),p.get()))
        r=cur.fetchone()
        if r:
            current_user=u.get(); current_role=r[0]; dashboard()
        else:
            messagebox.showerror('Error','Invalid credentials')
    ttk.Button(box,text='Login',command=do_login).pack(pady=10)


def create_ticket():
    win=tk.Toplevel(root)
    win.title('Create Ticket')
    tk.Label(win,text='Issue Title').pack(pady=5)
    e=tk.Entry(win,width=40)
    e.pack(pady=5)
    def save():
        cur.execute('INSERT INTO tickets(created_by,title,status,created_at) VALUES(?,?,?,?)',(current_user,e.get(),'Open',str(datetime.datetime.now())[:19]))
        conn.commit(); messagebox.showinfo('Done','Ticket created'); win.destroy(); refresh_table(False)
    ttk.Button(win,text='Submit',command=save).pack(pady=8)


def create_user():
    win=tk.Toplevel(root)
    win.title('Create User')
    vals={}
    for lbl in ['Username','Password','Role(user/admin)']:
        tk.Label(win,text=lbl).pack()
        ent=tk.Entry(win,width=30)
        ent.pack(pady=3)
        vals[lbl]=ent
    def save():
        role=vals['Role(user/admin)'].get().strip().lower()
        if role not in ('user','admin'): role='user'
        try:
            cur.execute('INSERT INTO users VALUES(?,?,?)',(vals['Username'].get(),vals['Password'].get(),role))
            conn.commit(); messagebox.showinfo('Done','User created'); win.destroy()
        except Exception as ex:
            messagebox.showerror('Error',str(ex))
    ttk.Button(win,text='Save',command=save).pack(pady=8)


def update_status(ticket_id,status):
    cur.execute('UPDATE tickets SET status=? WHERE id=?',(status,ticket_id)); conn.commit(); refresh_table(current_role=='admin')


def refresh_table(all_view):
    for i in table.get_children(): table.delete(i)
    if all_view:
        cur.execute('SELECT * FROM tickets ORDER BY id DESC')
    else:
        cur.execute('SELECT * FROM tickets WHERE created_by=? ORDER BY id DESC',(current_user,))
    for r in cur.fetchall(): table.insert('', 'end', values=r)


def dashboard():
    clear()
    top=tk.Frame(main,bg='#1e1e1e'); top.pack(fill='x',pady=10)
    tk.Label(top,text=f'Logged in as {current_user} ({current_role})',bg='#1e1e1e',fg='cyan',font=('Arial',14,'bold')).pack(side='left',padx=10)
    ttk.Button(top,text='Logout',command=login_screen).pack(side='right',padx=10)
    btns=tk.Frame(main,bg='#1e1e1e'); btns.pack(fill='x')
    ttk.Button(btns,text='Create Ticket',command=create_ticket).pack(side='left',padx=5)
    ttk.Button(btns,text='My Tickets',command=lambda: refresh_table(False)).pack(side='left',padx=5)
    if current_role=='admin':
        ttk.Button(btns,text='Create User',command=create_user).pack(side='left',padx=5)
        ttk.Button(btns,text='All Tickets',command=lambda: refresh_table(True)).pack(side='left',padx=5)
        ttk.Button(btns,text='Mark In Progress',command=lambda: selected_status('In Progress')).pack(side='left',padx=5)
        ttk.Button(btns,text='Mark Closed',command=lambda: selected_status('Closed')).pack(side='left',padx=5)
    global table
    cols=('ID','Created By','Title','Status','Created At')
    table=ttk.Treeview(main,columns=cols,show='headings',height=20)
    for c in cols:
        table.heading(c,text=c); table.column(c,width=160)
    table.pack(fill='both',expand=True,padx=10,pady=10)
    refresh_table(current_role=='admin')


def selected_status(status):
    sel=table.selection()
    if not sel: return
    vals=table.item(sel[0])['values']
    update_status(vals[0],status)

login_screen()
root.mainloop()
