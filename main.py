import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3, os
from datetime import datetime

LOGIN_USER=os.getenv('LOGIN_USER','admin')
USER_ROLE=os.getenv('USER_ROLE','Admin')
DB='helpdesk.db'
conn=sqlite3.connect(DB)
cur=conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS tickets(id INTEGER PRIMARY KEY AUTOINCREMENT,date TEXT,name TEXT,issue TEXT,priority TEXT,engineer TEXT,status TEXT)')
conn.commit()

root=tk.Tk(); root.title('IT Helpdesk V14'); root.geometry('1300x760'); root.configure(bg='#0f172a')
left=tk.Frame(root,bg='#1e293b',padx=10,pady=10); left.pack(side='left',fill='y')
right=tk.Frame(root,bg='#0f172a'); right.pack(side='right',fill='both',expand=True)

for i,t in enumerate(['Name','Issue','Priority']): tk.Label(left,text=t,bg='#1e293b',fg='white').grid(row=i,column=0,sticky='w',pady=5)
name=tk.Entry(left,width=26); name.grid(row=0,column=1)
issue=ttk.Combobox(left,width=23,values=['Laptop','Printer','Network','VPN','Email']); issue.grid(row=1,column=1)
pri=ttk.Combobox(left,width=23,values=['Low','Medium','High']); pri.set('Medium'); pri.grid(row=2,column=1)

search=tk.Entry(right,width=28); search.pack(pady=8)
top=tk.Frame(right,bg='#0f172a'); top.pack()
cols=('ID','Date','Name','Issue','Priority','Engineer','Status')
tree=ttk.Treeview(right,columns=cols,show='headings')
for c in cols: tree.heading(c,text=c); tree.column(c,width=150)
tree.pack(fill='both',expand=True,padx=10,pady=10)

def load_data(key=''):
    for i in tree.get_children(): tree.delete(i)
    if USER_ROLE=='Engineer':
        q="select * from tickets where (engineer=? or engineer='' or engineer is null) and (name like ? or issue like ?) order by id desc"
        rows=cur.execute(q,(LOGIN_USER,f'%{key}%',f'%{key}%')).fetchall()
    else:
        q="select * from tickets where name like ? or issue like ? order by id desc"
        rows=cur.execute(q,(f'%{key}%',f'%{key}%')).fetchall()
    for r in rows: tree.insert('', 'end', values=r)

def submit():
    cur.execute('insert into tickets(date,name,issue,priority,engineer,status) values(?,?,?,?,?,?)',(
        datetime.now().strftime('%d-%m-%Y %H:%M'),name.get(),issue.get(),pri.get(),'','Open'))
    conn.commit(); load_data(); messagebox.showinfo('Done','Ticket Created')

def status(s):
    sel=tree.selection()
    if not sel:return
    tid=tree.item(sel[0])['values'][0]
    cur.execute('update tickets set status=? where id=?',(s,tid)); conn.commit(); load_data()

def assign_me():
    sel=tree.selection()
    if not sel:return
    tid=tree.item(sel[0])['values'][0]
    cur.execute('update tickets set engineer=? where id=?',(LOGIN_USER,tid)); conn.commit(); load_data()

def reassign():
    sel=tree.selection()
    if not sel:return
    tid=tree.item(sel[0])['values'][0]
    new='Rahul' if LOGIN_USER!='Rahul' else 'Ashu'
    cur.execute('update tickets set engineer=? where id=?',(new,tid)); conn.commit(); load_data()

tk.Button(left,text='Create Ticket',width=22,bg='#14b8a6',command=submit).grid(row=4,column=1,pady=10)
tk.Label(left,text=f'{LOGIN_USER} ({USER_ROLE})',bg='#1e293b',fg='yellow').grid(row=5,column=1,pady=5)

tk.Button(top,text='Search',command=lambda:load_data(search.get()),bg='#06b6d4').pack(side='left',padx=4)
tk.Button(top,text='Assign to Me',command=assign_me,bg='#10b981').pack(side='left',padx=4)
tk.Button(top,text='Reassign',command=reassign,bg='#f59e0b').pack(side='left',padx=4)
tk.Button(top,text='In Progress',command=lambda:status('In Progress'),bg='#facc15').pack(side='left',padx=4)
tk.Button(top,text='Closed',command=lambda:status('Closed'),bg='#ef4444').pack(side='left',padx=4)

load_data(); root.mainloop()
