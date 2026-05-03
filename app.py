from flask import Flask, render_template_string, request, redirect, url_for
import csv, os
from datetime import datetime

app = Flask(__name__)
FILE = 'tickets.csv'

# Create file if not exists
def init_file():
    if not os.path.exists(FILE):
        with open(FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Ticket ID','Date','Name','Email','Department','Issue','Priority','Description','Status'])

# Get all rows
def get_rows():
    init_file()
    with open(FILE) as f:
        return list(csv.reader(f))[1:]

# Generate Ticket ID
def next_id():
    rows = get_rows()
    if not rows:
        return "TKT001"
    last = int(rows[-1][0].replace("TKT",""))
    return f"TKT{last+1:03}"

# HTML UI
HTML = """
<!doctype html>
<html>
<head>
    <title>IT Helpdesk</title>
    <style>
        body {font-family: Arial; background:#121212; color:white; padding:20px;}
        table {width:100%; border-collapse: collapse; background:white; color:black;}
        th, td {padding:10px; border:1px solid #ccc; text-align:center;}
        th {background:#333; color:white;}
        input, select, textarea {width:100%; padding:5px; margin:5px 0;}
        button {padding:8px 12px; cursor:pointer;}
    </style>
</head>
<body>

<h2>IT Helpdesk Ticketing Tool</h2>

<form method="POST" action="/add">
    <input name="name" placeholder="Name" required>
    <input name="email" placeholder="Email" required>
    <input name="department" placeholder="Department" required>
    <input name="issue" placeholder="Issue" required>

    <select name="priority">
        <option>Low</option>
        <option>Medium</option>
        <option>High</option>
    </select>

    <textarea name="description" placeholder="Description"></textarea>

    <button type="submit">Submit Ticket</button>
</form>

<br>

<table>
<tr>
    <th>ID</th>
    <th>Date</th>
    <th>Name</th>
    <th>Issue</th>
    <th>Priority</th>
    <th>Status</th>
    <th>Action</th>
</tr>

{% for row in rows %}
<tr>
    <td>{{ row[0] }}</td>
    <td>{{ row[1] }}</td>
    <td>{{ row[2] }}</td>
    <td>{{ row[5] }}</td>
    <td>{{ row[6] }}</td>
    <td>{{ row[8] }}</td>

    <td>
        {% if row[8] != "Closed" %}
        <form method="POST" action="/close">
            <input type="hidden" name="ticket_id" value="{{ row[0] }}">
            <button type="submit">Close</button>
        </form>
        {% else %}
        Closed
        {% endif %}
    </td>
</tr>
{% endfor %}

</table>

</body>
</html>
"""

# Home
@app.route('/')
def home():
    return render_template_string(HTML, rows=get_rows())

# Add Ticket
@app.route('/add', methods=['POST'])
def add():
    row = [
        next_id(),
        datetime.now().strftime('%d-%m-%Y %H:%M'),
        request.form['name'],
        request.form['email'],
        request.form['department'],
        request.form['issue'],
        request.form['priority'],
        request.form['description'],
        "Open"
    ]
    with open(FILE, 'a', newline='') as f:
        csv.writer(f).writerow(row)
    return redirect(url_for('home'))

# Close Ticket
@app.route('/close', methods=['POST'])
def close_ticket():
    ticket_id = request.form['ticket_id']

    rows = []
    with open(FILE, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)

        for row in reader:
            if row[0] == ticket_id:
                row[8] = "Closed"
            rows.append(row)

    with open(FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    return redirect(url_for('home'))

# Run
if __name__ == "__main__":
    app.run(debug=True)