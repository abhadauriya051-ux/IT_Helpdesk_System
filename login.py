import tkinter as tk
from tkinter import messagebox
import json, os, random, subprocess, sys

USERS_FILE='roles_users.json'
APP_FILE='main.py'
if not os.path.exists(USERS_FILE):
    data={'users':[{'username':'admin','password':'admin123','role':'Admin'}]}
    with open(USERS_FILE,'w') as f: json.dump(data,f,indent=2)

def load_users():
    with open(USERS_FILE,'r') as f:
        return json.load(f)['users']

def save_users(users):
    with open(USERS_FILE,'w') as f:
        json.dump({'users':users},f,indent=2)

root=tk.Tk(); root.title('IT Helpdesk Login V10'); root.geometry('560x520'); root.configure(bg='#0f172a')
frm=tk.Frame(root,bg='#1e293b',padx=25,pady=20); frm.place(relx=0.5,rely=0.5,anchor='center')

tk.Label(frm,text='IT Helpdesk Secure Login',font=('Arial',18,'bold'),bg='#1e293b',fg='white').pack(pady=8)
tk.Label(frm,text='Username',bg='#1e293b',fg='white').pack(anchor='w')
user=tk.Entry(frm,width=32); user.pack(pady=4)
tk.Label(frm,text='Password',bg='#1e293b',fg='white').pack(anchor='w')
pwd=tk.Entry(frm,width=32,show='*'); pwd.pack(pady=4)

def login():
    for u in load_users():
        if user.get()==u['username'] and pwd.get()==u['password']:
            messagebox.showinfo('Success',f"Welcome {u['username']}")
            root.destroy(); subprocess.Popen([sys.executable, APP_FILE]); return
    messagebox.showerror('Error','Invalid Username or Password')

def forgot_password():
    win=tk.Toplevel(root); win.title('Forgot Password'); win.geometry('420x360'); win.configure(bg='#111827')
    otp=str(random.randint(100000,999999))
    tk.Label(win,text='Forgot Password',font=('Arial',16,'bold'),bg='#111827',fg='white').pack(pady=10)
    tk.Label(win,text='Username',bg='#111827',fg='white').pack(); fu=tk.Entry(win,width=28); fu.pack(pady=4)
    tk.Label(win,text='OTP (demo shown below)',bg='#111827',fg='white').pack(); fo=tk.Entry(win,width=28); fo.pack(pady=4)
    tk.Label(win,text='New Password',bg='#111827',fg='white').pack(); fn=tk.Entry(win,width=28,show='*'); fn.pack(pady=4)
    tk.Label(win,text=f'Demo OTP: {otp}',bg='#111827',fg='yellow').pack(pady=6)
    def reset_pass():
        users=load_users(); found=False
        for u in users:
            if u['username']==fu.get():
                found=True
                if fo.get()!=otp:
                    messagebox.showerror('Error','Invalid OTP'); return
                u['password']=fn.get()
                save_users(users)
                messagebox.showinfo('Success','Password Reset Successful')
                win.destroy(); return
        if not found:
            messagebox.showerror('Error','User not found')
    tk.Button(win,text='Reset Password',width=22,bg='#14b8a6',command=reset_pass).pack(pady=12)

btn=tk.Button(frm,text='Login',width=28,bg='#14b8a6',command=login); btn.pack(pady=10)
tk.Button(frm,text='Forgot Password',width=28,bg='#f59e0b',command=forgot_password).pack(pady=5)
root.mainloop()