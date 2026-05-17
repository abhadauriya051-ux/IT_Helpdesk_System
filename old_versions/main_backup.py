from flask import Flask, render_template, request, redirect, session
import sqlite3
import math
import smtplib

from email.mime.text import MIMEText

app = Flask(__name__)

app.secret_key = "helpdesk_secret"

DB = "helpdesk.db"


# =========================
# INIT DATABASE
# =========================
def init_db():

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS tickets(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_email TEXT,
        subject TEXT,
        message TEXT,
        priority TEXT DEFAULT 'Medium',
        status TEXT DEFAULT 'Open',
        engineer TEXT DEFAULT 'Unassigned',
        attachment TEXT

    )

    """)

    conn.commit()
    conn.close()


init_db()


# =========================
# LOGIN
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":

            session["user"] = username

            return redirect("/dashboard/open")

    return render_template("login.html")


# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# =========================
# DASHBOARD
# =========================
@app.route("/")
@app.route("/dashboard/<view>")
def dashboard(view="open"):

    if "user" not in session:
        return redirect("/login")

    search = request.args.get("search", "")

    page = request.args.get("page", 1, type=int)

    per_page = 5

    offset = (page - 1) * per_page

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    if view == "closed":

        query = """

        SELECT * FROM tickets
        WHERE status='Closed'

        """

    else:

        query = """

        SELECT * FROM tickets
        WHERE status='Open'

        """

    if search:

        query += """

        AND (

            CAST(id AS TEXT) LIKE ?
            OR sender_email LIKE ?
            OR subject LIKE ?

        )

        """

        params = (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        )

    else:

        params = ()

    count_query = query.replace(
        "SELECT *",
        "SELECT COUNT(*)"
    )

    cursor.execute(count_query, params)

    total = cursor.fetchone()[0]

    total_pages = math.ceil(total / per_page)

    query += " ORDER BY id DESC LIMIT ? OFFSET ?"

    params = params + (per_page, offset)

    cursor.execute(query, params)

    tickets = cursor.fetchall()

    conn.close()

    return render_template(

        "dashboard.html",
        tickets=tickets,
        view=view,
        page=page,
        total_pages=total_pages

    )


# =========================
# TICKET DETAILS
# =========================
@app.route("/ticket/<int:ticket_id>")
def ticket_details(ticket_id):

    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""

    SELECT * FROM tickets
    WHERE id=?

    """, (ticket_id,))

    ticket = cursor.fetchone()

    conn.close()

    return render_template(
        "ticket_details.html",
        ticket=ticket
    )


# =========================
# CLOSE TICKET
# =========================
@app.route("/close/<int:ticket_id>")
def close_ticket(ticket_id):

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""

    UPDATE tickets
    SET status='Closed'
    WHERE id=?

    """, (ticket_id,))

    conn.commit()
    conn.close()

    return redirect("/dashboard/closed")


# =========================
# REOPEN TICKET
# =========================
@app.route("/reopen/<int:ticket_id>")
def reopen_ticket(ticket_id):

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""

    UPDATE tickets
    SET status='Open'
    WHERE id=?

    """, (ticket_id,))

    conn.commit()
    conn.close()

    return redirect("/dashboard/open")


# =========================
# UPDATE PRIORITY
# =========================
@app.route("/priority/<int:ticket_id>", methods=["POST"])
def update_priority(ticket_id):

    priority = request.form["priority"]

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""

    UPDATE tickets
    SET priority=?
    WHERE id=?

    """, (priority, ticket_id))

    conn.commit()
    conn.close()

    return redirect(request.referrer)


# =========================
# ASSIGN ENGINEER
# =========================
@app.route("/assign/<int:ticket_id>", methods=["POST"])
def assign_engineer(ticket_id):

    engineer = request.form["engineer"]

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""

    UPDATE tickets
    SET engineer=?
    WHERE id=?

    """, (engineer, ticket_id))

    conn.commit()
    conn.close()

    return redirect(request.referrer)


# =========================
# REPLY SYSTEM
# =========================
@app.route("/reply/<int:ticket_id>", methods=["POST"])
def reply_ticket(ticket_id):

    reply_message = request.form["reply"]

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""

    SELECT * FROM tickets
    WHERE id=?

    """, (ticket_id,))

    ticket = cursor.fetchone()

    conn.close()

    sender_email = ticket[1]
    subject = ticket[2]

    try:

        msg = MIMEText(reply_message)

        msg["Subject"] = "Re: " + subject

        msg["From"] = "bashu6693@gmail.com"

        msg["To"] = sender_email

        server = smtplib.SMTP("smtp.gmail.com", 587)

        server.starttls()

        server.login(

            "bashu6693@gmail.com",
            "shjtxuowiwhcwvpn"

        )

        server.sendmail(

            "YOUR_GMAIL@gmail.com",
            sender_email,
            msg.as_string()

        )

        server.quit()

        print("Reply sent successfully")

    except Exception as e:

        print("Mail Error:", e)

    return redirect(f"/ticket/{ticket_id}")


# =========================
# DARK/LIGHT THEME
# =========================
@app.route("/toggle-theme")
def toggle_theme():

    current = session.get("theme", "dark")

    if current == "dark":

        session["theme"] = "light"

    else:

        session["theme"] = "dark"

    return redirect(request.referrer)


# =========================
# RUN APP
# =========================
if __name__ == "__main__":

    app.run(debug=True)



