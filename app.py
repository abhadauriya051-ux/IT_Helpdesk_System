from flask import Flask, render_template, request, redirect, url_for
import csv
import os
from datetime import datetime

app = Flask(__name__)
FILE = 'tickets.csv'


# Create CSV if not exists
def init_file():
    if not os.path.exists(FILE):
        with open(FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Ticket ID',
                'Date',
                'Name',
                'Email',
                'Department',
                'Issue',
                'Priority',
                'Description',
                'Status'
            ])


# Get all rows
def get_rows():
    init_file()
    with open(FILE, newline='') as f:
        return list(csv.reader(f))[1:]


# Generate next Ticket ID
def next_id():
    rows = get_rows()

    if not rows:
        return "TKT001"

    last = int(rows[-1][0].replace("TKT", ""))
    return f"TKT{last+1:03}"


# Home Page
@app.route('/')
def home():
    rows = get_rows()
    return render_template("index.html", tickets=rows)


# Add Ticket
@app.route('/add', methods=['POST'])
def add():
    ticket_id = next_id()
    date = datetime.now().strftime("%d-%m-%Y %H:%M")

    data = [
        ticket_id,
        date,
        request.form['name'],
        request.form['email'],
        request.form['department'],
        request.form['issue'],
        request.form['priority'],
        request.form['description'],
        "Open"
    ]

    with open(FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)

    return redirect(url_for('home'))


# Close Ticket
@app.route('/close', methods=['POST'])
def close():
    ticket_id = request.form['ticket_id']

    rows = get_rows()

    for row in rows:
        if row[0] == ticket_id:
            row[8] = "Closed"

    with open(FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Ticket ID',
            'Date',
            'Name',
            'Email',
            'Department',
            'Issue',
            'Priority',
            'Description',
            'Status'
        ])
        writer.writerows(rows)

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)