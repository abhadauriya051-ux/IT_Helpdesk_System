from database.db import connect_db

def get_all_tickets():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM tickets
    ORDER BY id DESC
    """)

    tickets = cursor.fetchall()

    conn.close()

    return tickets

